"""
database.py - SQLite Database Management for CampusMart
Supports schema creation, migrations, parameterized queries, and seeding.
"""

import sqlite3
import os
from datetime import datetime
from werkzeug.security import generate_password_hash

DB_NAME = "campusmart.db"

CATEGORIES = [
    "Textbooks",
    "Calculators",
    "Electronics",
    "Stationery",
    "Lab Equipment",
    "Other"
]

CONDITIONS = [
    "New",
    "Like New",
    "Good",
    "Used"
]


def get_connection():
    """Establish and return SQLite connection with row_factory enabled and foreign keys on."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """
    Initialize SQLite database schema.
    Safely migrates existing 'products' table if needed, creates 'users' and 'wishlist',
    and seeds demo users and products.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'student',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 2. Check if products table exists and has user_id, condition, image_filename, updated_at
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='products'")
    products_table_exists = cursor.fetchone() is not None

    if not products_table_exists:
        cursor.execute("""
            CREATE TABLE products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                name TEXT NOT NULL,
                description TEXT,
                category TEXT NOT NULL,
                price REAL NOT NULL,
                condition TEXT DEFAULT 'Good',
                image_filename TEXT DEFAULT 'placeholder.svg',
                seller_name TEXT NOT NULL,
                seller_contact TEXT NOT NULL,
                status TEXT DEFAULT 'Available',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
    else:
        # Check columns and perform migration if columns missing
        cursor.execute("PRAGMA table_info(products)")
        columns = [row["name"] for row in cursor.fetchall()]
        if "user_id" not in columns:
            cursor.execute("ALTER TABLE products ADD COLUMN user_id INTEGER")
        if "condition" not in columns:
            cursor.execute("ALTER TABLE products ADD COLUMN condition TEXT DEFAULT 'Good'")
        if "image_filename" not in columns:
            cursor.execute("ALTER TABLE products ADD COLUMN image_filename TEXT DEFAULT 'placeholder.svg'")
        if "updated_at" not in columns:
            cursor.execute("ALTER TABLE products ADD COLUMN updated_at TIMESTAMP")
            cursor.execute("UPDATE products SET updated_at = created_at WHERE updated_at IS NULL")

    # 3. Wishlist Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS wishlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, product_id),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
        )
    """)
    conn.commit()

    # 4. Seed default admin & student accounts if users table empty
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    if user_count == 0:
        seed_users(conn)

    # 5. Seed default demo products if products table empty
    cursor.execute("SELECT COUNT(*) FROM products")
    prod_count = cursor.fetchone()[0]
    if prod_count == 0:
        seed_demo_products(conn)
    else:
        # If products already exist without user_id, link them to the demo student account (user_id=2)
        cursor.execute("UPDATE products SET user_id = 2 WHERE user_id IS NULL")
        conn.commit()

    conn.close()


def seed_users(conn):
    """Seed administrator and demo student user accounts."""
    cursor = conn.cursor()
    # Admin Account: admin@campusmart.edu / admin123
    admin_pw = generate_password_hash("admin123")
    cursor.execute("""
        INSERT INTO users (name, email, password_hash, role)
        VALUES (?, ?, ?, ?)
    """, ("CampusMart Admin", "admin@campusmart.edu", admin_pw, "admin"))

    # Demo Student: Rahul Sharma / student@campusmart.edu / student123
    student_pw = generate_password_hash("student123")
    cursor.execute("""
        INSERT INTO users (name, email, password_hash, role)
        VALUES (?, ?, ?, ?)
    """, ("Rahul Sharma", "student@campusmart.edu", student_pw, "student"))

    # Demo Student 2: Priya Patel / priya@campusmart.edu / priya123
    priya_pw = generate_password_hash("priya123")
    cursor.execute("""
        INSERT INTO users (name, email, password_hash, role)
        VALUES (?, ?, ?, ?)
    """, ("Priya Patel", "priya@campusmart.edu", priya_pw, "student"))

    conn.commit()


def seed_demo_products(conn):
    """Seed comprehensive demo products with user ownership."""
    cursor = conn.cursor()
    demo_items = [
        (
            2, # Rahul Sharma
            "Higher Engineering Mathematics (43rd Ed)",
            "Comprehensive textbook by B.S. Grewal. In good condition with minimal pencil annotations. Covers all Semester 1 to 4 syllabus.",
            "Textbooks",
            450.0,
            "Good",
            "placeholder.svg",
            "Rahul Sharma",
            "student@campusmart.edu | 9876543210",
            "Available"
        ),
        (
            3, # Priya Patel
            "Casio fx-991EX ClassWiz Calculator",
            "Original scientific calculator with 552 functions. High resolution natural display, solar plus battery powered. In mint condition with slide-on case.",
            "Calculators",
            750.0,
            "Like New",
            "placeholder.svg",
            "Priya Patel",
            "priya@campusmart.edu | 9811223344",
            "Available"
        ),
        (
            2, # Rahul Sharma
            "Data Structures & Algorithms in C",
            "Standard prescribed reference book by Reema Thareja (Oxford). Crisp pages, zero torn leaves. Crucial for 3rd semester IT core exam.",
            "Textbooks",
            380.0,
            "Like New",
            "placeholder.svg",
            "Rahul Sharma",
            "student@campusmart.edu | 9876543210",
            "Available"
        ),
        (
            3, # Priya Patel
            "Engineering Mini Drafter & Drawing Kit",
            "Complete engineering graphics set: Omega mini-drafter, sheet holder canister, set squares, clips, and stainless steel scale.",
            "Stationery",
            520.0,
            "Good",
            "placeholder.svg",
            "Priya Patel",
            "priya@campusmart.edu | 9811223344",
            "Sold"
        ),
        (
            2, # Rahul Sharma
            "Basic Electronics Lab Kit with Breadboard",
            "Includes breadboard, jumper wire bundle, 555 timers, LM741 op-amps, assorted LEDs, resistors, capacitors, and multimeter probes.",
            "Lab Equipment",
            590.0,
            "Good",
            "placeholder.svg",
            "Rahul Sharma",
            "student@campusmart.edu | 9876543210",
            "Available"
        ),
        (
            3, # Priya Patel
            "Arduino Uno R3 Microcontroller Board",
            "Original ATmega328P microcontroller board with USB-B interface cable. Tested and completely functional for IoT and embedded projects.",
            "Electronics",
            480.0,
            "Like New",
            "placeholder.svg",
            "Priya Patel",
            "priya@campusmart.edu | 9811223344",
            "Available"
        ),
        (
            2, # Rahul Sharma
            "Ergonomic Wireless Optical Mouse",
            "Logitech 2.4GHz wireless mouse with nano USB receiver. Smooth tracking on any surface, battery included.",
            "Other",
            320.0,
            "Used",
            "placeholder.svg",
            "Rahul Sharma",
            "student@campusmart.edu | 9876543210",
            "Available"
        )
    ]

    for item in demo_items:
        cursor.execute("""
            INSERT INTO products (
                user_id, name, description, category, price, condition,
                image_filename, seller_name, seller_contact, status, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item[0], item[1], item[2], item[3], item[4], item[5],
            item[6], item[7], item[8], item[9],
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
    conn.commit()


def reset_to_demo_data():
    """Reset database cleanly to default demo users and products."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM wishlist")
    cursor.execute("DELETE FROM products")
    cursor.execute("DELETE FROM users")
    conn.commit()
    seed_users(conn)
    seed_demo_products(conn)
    conn.close()


# ================= USER OPERATIONS =================

def create_user(name, email, password, role="student"):
    """Register a new user with hashed password."""
    conn = get_connection()
    cursor = conn.cursor()
    pw_hash = generate_password_hash(password)
    try:
        cursor.execute("""
            INSERT INTO users (name, email, password_hash, role)
            VALUES (?, ?, ?, ?)
        """, (name.strip(), email.strip().lower(), pw_hash, role))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return user_id, None
    except sqlite3.IntegrityError:
        conn.close()
        return None, "Email address is already registered."
    except Exception as e:
        conn.close()
        return None, str(e)


def get_user_by_email(email):
    """Retrieve user record by email."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE LOWER(email) = ?", (email.strip().lower(),))
    user = cursor.fetchone()
    conn.close()
    return user


def get_user_by_id(user_id):
    """Retrieve user record by user_id."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user


def get_all_users():
    """Retrieve all registered users (for admin dashboard)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, role, created_at FROM users ORDER BY id DESC")
    users = cursor.fetchall()
    conn.close()
    return users


# ================= PRODUCT CRUD OPERATIONS =================

def add_product(user_id, name, description, category, price, condition, image_filename, seller_name, seller_contact, status="Available"):
    """Create a new product listing."""
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO products (
            user_id, name, description, category, price, condition,
            image_filename, seller_name, seller_contact, status, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        name.strip(),
        description.strip(),
        category,
        float(price),
        condition,
        image_filename or "placeholder.svg",
        seller_name.strip(),
        seller_contact.strip(),
        status,
        now,
        now
    ))
    conn.commit()
    prod_id = cursor.lastrowid
    conn.close()
    return prod_id


def get_products(search="", category="All", condition="All", min_price=None, max_price=None, sort_by="newest"):
    """
    Search and filter products with dynamic parameterized SQL queries.
    Supports search query, category, condition, price range, and sorting.
    """
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM products WHERE 1=1"
    params = []

    if search and search.strip():
        query += " AND (name LIKE ? OR description LIKE ?)"
        pattern = f"%{search.strip()}%"
        params.extend([pattern, pattern])

    if category and category != "All":
        query += " AND category = ?"
        params.append(category)

    if condition and condition != "All":
        query += " AND condition = ?"
        params.append(condition)

    if min_price is not None and str(min_price).strip() != "":
        try:
            query += " AND price >= ?"
            params.append(float(min_price))
        except ValueError:
            pass

    if max_price is not None and str(max_price).strip() != "":
        try:
            query += " AND price <= ?"
            params.append(float(max_price))
        except ValueError:
            pass

    # Sorting
    if sort_by == "price_asc":
        query += " ORDER BY price ASC"
    elif sort_by == "price_desc":
        query += " ORDER BY price DESC"
    elif sort_by == "oldest":
        query += " ORDER BY id ASC"
    else:  # newest default
        query += " ORDER BY id DESC"

    cursor.execute(query, params)
    products = cursor.fetchall()
    conn.close()
    return products


def get_product_by_id(product_id):
    """Retrieve single product by id."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    conn.close()
    return product


def get_user_products(user_id):
    """Retrieve all products listed by a specific seller."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE user_id = ? ORDER BY id DESC", (user_id,))
    products = cursor.fetchall()
    conn.close()
    return products


def update_product(product_id, name, description, category, price, condition, seller_name, seller_contact, status, image_filename=None):
    """Update existing product listing."""
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if image_filename:
        cursor.execute("""
            UPDATE products
            SET name = ?, description = ?, category = ?, price = ?, condition = ?,
                seller_name = ?, seller_contact = ?, status = ?, image_filename = ?, updated_at = ?
            WHERE id = ?
        """, (
            name.strip(), description.strip(), category, float(price), condition,
            seller_name.strip(), seller_contact.strip(), status, image_filename, now, product_id
        ))
    else:
        cursor.execute("""
            UPDATE products
            SET name = ?, description = ?, category = ?, price = ?, condition = ?,
                seller_name = ?, seller_contact = ?, status = ?, updated_at = ?
            WHERE id = ?
        """, (
            name.strip(), description.strip(), category, float(price), condition,
            seller_name.strip(), seller_contact.strip(), status, now, product_id
        ))

    conn.commit()
    conn.close()


def update_product_status(product_id, new_status):
    """Toggle status between 'Available' and 'Sold'."""
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("UPDATE products SET status = ?, updated_at = ? WHERE id = ?", (new_status, now, product_id))
    conn.commit()
    conn.close()


def delete_product(product_id):
    """Delete product from database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()


# ================= WISHLIST OPERATIONS =================

def add_to_wishlist(user_id, product_id):
    """Add a product to user's wishlist."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO wishlist (user_id, product_id) VALUES (?, ?)", (user_id, product_id))
        conn.commit()
        conn.close()
        return True, "Product added to wishlist!"
    except sqlite3.IntegrityError:
        conn.close()
        return False, "This product is already in your wishlist."
    except Exception as e:
        conn.close()
        return False, str(e)


def remove_from_wishlist(user_id, product_id):
    """Remove a product from user's wishlist."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM wishlist WHERE user_id = ? AND product_id = ?", (user_id, product_id))
    conn.commit()
    conn.close()
    return True


def is_in_wishlist(user_id, product_id):
    """Check if product is in user's wishlist."""
    if not user_id:
        return False
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM wishlist WHERE user_id = ? AND product_id = ?", (user_id, product_id))
    res = cursor.fetchone() is not None
    conn.close()
    return res


def get_user_wishlist(user_id):
    """Retrieve full product details for items in user's wishlist."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.*, w.created_at AS saved_at
        FROM wishlist w
        JOIN products p ON w.product_id = p.id
        WHERE w.user_id = ?
        ORDER BY w.id DESC
    """, (user_id,))
    items = cursor.fetchall()
    conn.close()
    return items


# ================= STATS & ANALYTICS =================

def get_marketplace_stats():
    """Retrieve comprehensive platform metrics for dashboards and home page."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM products")
    total_products = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM products WHERE status = 'Available'")
    available_products = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM products WHERE status = 'Sold'")
    sold_products = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM wishlist")
    total_wishlist_items = cursor.fetchone()[0]

    # Category breakdown for charts
    cursor.execute("""
        SELECT category, COUNT(*) as count
        FROM products
        GROUP BY category
    """)
    cat_rows = cursor.fetchall()
    category_counts = {row["category"]: row["count"] for row in cat_rows}

    conn.close()
    return {
        "total_products": total_products,
        "available_products": available_products,
        "sold_products": sold_products,
        "total_users": total_users,
        "total_wishlist_items": total_wishlist_items,
        "category_counts": category_counts
    }


def get_seller_stats(user_id):
    """Retrieve metrics for an individual seller's dashboard."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM products WHERE user_id = ?", (user_id,))
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM products WHERE user_id = ? AND status = 'Available'", (user_id,))
    available = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM products WHERE user_id = ? AND status = 'Sold'", (user_id,))
    sold = cursor.fetchone()[0]

    conn.close()
    return {
        "total": total,
        "available": available,
        "sold": sold
    }


if __name__ == "__main__":
    init_db()
    print("CampusMart database initialized and verified.")
    stats = get_marketplace_stats()
    print("Marketplace stats:", stats)
