"""
app.py - CampusMart Full-Stack Flask Web Application
Semester 5 Information Technology Mini Project
Features: Products CRUD, Search/Filter, User Auth, Wishlist, Dashboards, CSRF protection, and file uploads.
"""

import os
import re
import secrets
from functools import wraps
from flask import (
    Flask, render_template, request, redirect, url_for,
    flash, session, send_from_directory, abort
)
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

import database as db

# Application Setup
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'campusmart-secret-key-sem5-project')
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB max image upload
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize database schema and default records
db.init_db()


# ================= SECURITY & CSRF HELPERS =================

def generate_csrf_token():
    """Generate and store CSRF token in session."""
    if '_csrf_token' not in session:
        session['_csrf_token'] = secrets.token_hex(16)
    return session['_csrf_token']

app.jinja_env.globals['csrf_token'] = generate_csrf_token


@app.before_request
def csrf_protect():
    """Verify CSRF token on mutating HTTP methods."""
    if request.method in ("POST", "PUT", "DELETE", "PATCH"):
        # Allow test client or form token check
        token = request.form.get('csrf_token') or request.headers.get('X-CSRFToken')
        session_token = session.get('_csrf_token')
        if not session_token or token != session_token:
            # If token is missing during standard test or missing form CSRF
            # We enforce CSRF validation
            if not app.config.get('TESTING', False):
                abort(403, description="CSRF token validation failed. Please refresh and try again.")


def allowed_file(filename):
    """Validate allowed image file extensions."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def login_required(f):
    """Decorator to protect routes requiring user authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            flash("Please log in to access this feature.", "warning")
            return redirect(url_for('login', next=request.path))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Decorator to protect routes requiring administrator privileges."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            flash("Please log in with administrator credentials.", "warning")
            return redirect(url_for('login', next=request.path))
        if session.get('user_role') != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


# ================= CONTEXT PROCESSOR =================

@app.context_processor
def inject_common_variables():
    """Make categories and conditions globally accessible in Jinja templates."""
    return {
        'categories': db.CATEGORIES,
        'conditions': db.CONDITIONS
    }


# ================= STATIC / UPLOADED FILES =================

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded images securely."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# ================= PUBLIC ROUTES =================

@app.route('/')
def index():
    """Landing Home Page with hero, categories, stats, and featured listings."""
    stats = db.get_marketplace_stats()
    # Fetch recent 8 products
    all_prods = db.get_products(sort_by="newest")
    featured_products = all_prods[:8]
    return render_template('index.html', stats=stats, featured_products=featured_products)


@app.route('/products')
def browse_products():
    """Browse, search, and filter marketplace products."""
    search_query = request.args.get('q', '').strip()
    category = request.args.get('category', 'All')
    condition = request.args.get('condition', 'All')
    min_price = request.args.get('min_price', None)
    max_price = request.args.get('max_price', None)
    sort_by = request.args.get('sort', 'newest')

    products = db.get_products(
        search=search_query,
        category=category,
        condition=condition,
        min_price=min_price,
        max_price=max_price,
        sort_by=sort_by
    )

    return render_template(
        'products.html',
        products=products,
        search_query=search_query,
        selected_category=category,
        selected_condition=condition
    )


@app.route('/products/<int:product_id>')
def product_detail(product_id):
    """Display comprehensive details for a single product."""
    product = db.get_product_by_id(product_id)
    if not product:
        abort(404)

    in_wishlist = False
    if session.get('user_id'):
        in_wishlist = db.is_in_wishlist(session['user_id'], product_id)

    return render_template('product_detail.html', product=product, in_wishlist=in_wishlist)


# ================= PRODUCT CRUD OPERATIONS =================

@app.route('/sell', methods=['GET', 'POST'])
@login_required
def sell_product():
    """Post a new student listing."""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        category = request.form.get('category', 'Other')
        condition = request.form.get('condition', 'Good')
        price_str = request.form.get('price', '0')
        seller_name = request.form.get('seller_name', '').strip()
        seller_contact = request.form.get('seller_contact', '').strip()
        status = request.form.get('status', 'Available')

        # Form Validation
        if not name or not seller_name or not seller_contact:
            flash("Product title, seller name, and contact details are required.", "danger")
            return redirect(url_for('sell_product'))

        try:
            price = float(price_str)
            if price < 0:
                flash("Price cannot be a negative value.", "danger")
                return redirect(url_for('sell_product'))
        except ValueError:
            flash("Please enter a valid numeric price.", "danger")
            return redirect(url_for('sell_product'))

        # Safe File Upload Handling
        image_filename = "placeholder.svg"
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '':
                if allowed_file(file.filename):
                    ext = file.filename.rsplit('.', 1)[1].lower()
                    random_prefix = secrets.token_hex(8)
                    filename = secure_filename(f"{random_prefix}.{ext}")
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    image_filename = filename
                else:
                    flash("Invalid image format! Only JPG, PNG, and WEBP are supported.", "danger")
                    return redirect(url_for('sell_product'))

        # Save to database
        prod_id = db.add_product(
            user_id=session['user_id'],
            name=name,
            description=description,
            category=category,
            price=price,
            condition=condition,
            image_filename=image_filename,
            seller_name=seller_name,
            seller_contact=seller_contact,
            status=status
        )

        flash(f"Listing '{name}' posted successfully! (Item ID #{prod_id})", "success")
        return redirect(url_for('product_detail', product_id=prod_id))

    return render_template('sell_product.html')


@app.route('/products/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    """Edit existing product listing with ownership check."""
    product = db.get_product_by_id(product_id)
    if not product:
        abort(404)

    # Authorization Check: only owner or admin can edit
    if product['user_id'] != session.get('user_id') and session.get('user_role') != 'admin':
        abort(403)

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        category = request.form.get('category', product['category'])
        condition = request.form.get('condition', product['condition'])
        price_str = request.form.get('price', str(product['price']))
        seller_name = request.form.get('seller_name', '').strip()
        seller_contact = request.form.get('seller_contact', '').strip()
        status = request.form.get('status', product['status'])

        if not name or not seller_name or not seller_contact:
            flash("Product title, seller name, and contact details are required.", "danger")
            return redirect(url_for('edit_product', product_id=product_id))

        try:
            price = float(price_str)
            if price < 0:
                flash("Price cannot be negative.", "danger")
                return redirect(url_for('edit_product', product_id=product_id))
        except ValueError:
            flash("Please enter a valid numeric price.", "danger")
            return redirect(url_for('edit_product', product_id=product_id))

        # Check for image replacement
        image_filename = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '':
                if allowed_file(file.filename):
                    ext = file.filename.rsplit('.', 1)[1].lower()
                    random_prefix = secrets.token_hex(8)
                    filename = secure_filename(f"{random_prefix}.{ext}")
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    image_filename = filename
                else:
                    flash("Invalid image format! Only JPG, PNG, and WEBP are supported.", "danger")
                    return redirect(url_for('edit_product', product_id=product_id))

        db.update_product(
            product_id=product_id,
            name=name,
            description=description,
            category=category,
            price=price,
            condition=condition,
            seller_name=seller_name,
            seller_contact=seller_contact,
            status=status,
            image_filename=image_filename
        )

        flash("Listing updated successfully!", "success")
        return redirect(url_for('product_detail', product_id=product_id))

    return render_template('edit_product.html', product=product)


@app.route('/products/<int:product_id>/toggle-status', methods=['POST'])
@login_required
def toggle_status(product_id):
    """Quickly toggle between Available and Sold statuses."""
    product = db.get_product_by_id(product_id)
    if not product:
        abort(404)

    if product['user_id'] != session.get('user_id') and session.get('user_role') != 'admin':
        abort(403)

    new_status = "Sold" if product['status'] == "Available" else "Available"
    db.update_product_status(product_id, new_status)
    flash(f"Listing status changed to '{new_status}'!", "success")
    return redirect(request.referrer or url_for('seller_dashboard'))


@app.route('/products/<int:product_id>/delete', methods=['POST'])
@login_required
def delete_product(product_id):
    """Delete a listing after ownership verification."""
    product = db.get_product_by_id(product_id)
    if not product:
        abort(404)

    if product['user_id'] != session.get('user_id') and session.get('user_role') != 'admin':
        abort(403)

    db.delete_product(product_id)
    flash("Listing deleted successfully.", "info")
    return redirect(url_for('seller_dashboard'))


# ================= WISHLIST =================

@app.route('/wishlist')
@login_required
def wishlist():
    """View saved products for the logged in user."""
    wishlist_items = db.get_user_wishlist(session['user_id'])
    return render_template('wishlist.html', wishlist_items=wishlist_items)


@app.route('/wishlist/<int:product_id>/toggle', methods=['POST'])
@login_required
def toggle_wishlist(product_id):
    """Add or remove an item from user's wishlist."""
    product = db.get_product_by_id(product_id)
    if not product:
        abort(404)

    user_id = session['user_id']
    if db.is_in_wishlist(user_id, product_id):
        db.remove_from_wishlist(user_id, product_id)
        flash("Item removed from your wishlist.", "info")
    else:
        success, msg = db.add_to_wishlist(user_id, product_id)
        if success:
            flash("Item added to your wishlist!", "success")
        else:
            flash(msg, "warning")

    return redirect(request.referrer or url_for('browse_products'))


# ================= DASHBOARDS =================

@app.route('/dashboard')
@login_required
def seller_dashboard():
    """Personal seller dashboard showing metrics and listed items."""
    user_id = session['user_id']
    products = db.get_user_products(user_id)
    stats = db.get_seller_stats(user_id)
    return render_template('seller_dashboard.html', products=products, stats=stats)


@app.route('/admin')
@admin_required
def admin_dashboard():
    """Administrator oversight dashboard with analytics and user moderation."""
    stats = db.get_marketplace_stats()
    all_products = db.get_products(sort_by="newest")
    users = db.get_all_users()
    return render_template('admin_dashboard.html', stats=stats, all_products=all_products, users=users)


@app.route('/admin/reset-data', methods=['POST'])
@admin_required
def admin_reset_data():
    """Developer/viva option to reset to default demonstration data."""
    db.reset_to_demo_data()
    flash("Database successfully reset to demonstration data!", "success")
    return redirect(url_for('admin_dashboard'))


# ================= USER AUTHENTICATION =================

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register a new student account."""
    if session.get('user_id'):
        return redirect(url_for('index'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Server-side validation
        if not name or not email or not password:
            flash("All fields are required.", "danger")
            return redirect(url_for('register'))

        email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if not re.match(email_pattern, email):
            flash("Please enter a valid email address.", "danger")
            return redirect(url_for('register'))

        if len(password) < 6:
            flash("Password must be at least 6 characters long.", "danger")
            return redirect(url_for('register'))

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for('register'))

        user_id, err = db.create_user(name=name, email=email, password=password, role="student")
        if err:
            flash(err, "danger")
            return redirect(url_for('register'))

        # Auto login upon successful registration
        session['user_id'] = user_id
        session['user_name'] = name
        session['user_email'] = email.lower()
        session['user_role'] = 'student'

        flash(f"Welcome to CampusMart, {name}! Your student account is active.", "success")
        return redirect(url_for('index'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Student and Administrator login."""
    if session.get('user_id'):
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        next_url = request.form.get('next', '')

        if not email or not password:
            flash("Please provide both email and password.", "danger")
            return redirect(url_for('login'))

        user = db.get_user_by_email(email)
        if not user or not check_password_hash(user['password_hash'], password):
            flash("Invalid email or password. Please try again.", "danger")
            return redirect(url_for('login'))

        # Set session
        session['user_id'] = user['id']
        session['user_name'] = user['name']
        session['user_email'] = user['email']
        session['user_role'] = user['role']

        flash(f"Welcome back, {user['name']}!", "success")

        # Safe redirect check
        if next_url and next_url.startswith('/'):
            return redirect(next_url)
        return redirect(url_for('index'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    """Clear session and log out."""
    session.clear()
    flash("You have been logged out successfully.", "info")
    return redirect(url_for('index'))


# ================= ERROR HANDLERS =================

@app.errorhandler(403)
def forbidden_error(error):
    return render_template('403.html'), 403


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    # Run locally on port 5000
    print("Starting CampusMart Flask Web Server on http://127.0.0.1:5000 ...")
    app.run(host='127.0.0.1', port=5000, debug=True)
