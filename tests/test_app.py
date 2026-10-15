"""
test_app.py - Automated Unit & Integration Tests for CampusMart
Tests authentication, authorization, CRUD, wishlist, and search/filters.
"""

import pytest
import os
from app import app
import database as db


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        with app.app_context():
            db.init_db()
        yield client


def test_home_page_loads(client):
    """Verify home page loads successfully with 200 OK and branding."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"CampusMart" in response.data


def test_browse_products_and_search(client):
    """Verify browsing and search keyword filter works."""
    response = client.get('/products?q=Calculator')
    assert response.status_code == 200
    assert b"Calculator" in response.data


def test_category_filter(client):
    """Verify filtering by category 'Textbooks'."""
    response = client.get('/products?category=Textbooks')
    assert response.status_code == 200
    assert b"Textbooks" in response.data


def test_user_registration_and_duplicate_rejection(client):
    """Verify user registration and rejection of duplicate email."""
    client.get('/logout')  # ensure clean session
    email = "uniquestudent99@college.edu"
    res = client.post('/register', data={
        'name': 'Test Student',
        'email': email,
        'password': 'password123',
        'confirm_password': 'password123'
    }, follow_redirects=True)
    assert res.status_code == 200
    assert b"Welcome to CampusMart" in res.data

    # Log out before attempting duplicate registration
    client.get('/logout')
    res_dup = client.post('/register', data={
        'name': 'Duplicate User',
        'email': email,
        'password': 'password123',
        'confirm_password': 'password123'
    }, follow_redirects=True)
    assert b"already registered" in res_dup.data


def test_login_and_logout(client):
    """Verify login with demo credentials and logout."""
    client.get('/logout')
    # Login
    res = client.post('/login', data={
        'email': 'student@campusmart.edu',
        'password': 'student123'
    }, follow_redirects=True)
    assert res.status_code == 200
    assert b"Welcome back" in res.data

    # Logout
    res_logout = client.get('/logout', follow_redirects=True)
    assert res_logout.status_code == 200
    assert b"logged out" in res_logout.data


def test_password_is_hashed(client):
    """Verify plaintext password is never stored in SQLite."""
    user = db.get_user_by_email('student@campusmart.edu')
    assert user is not None
    assert user['password_hash'] != 'student123'
    assert user['password_hash'].startswith('scrypt:') or user['password_hash'].startswith('pbkdf2:')


def test_product_creation_and_negative_price_rejection(client):
    """Verify product creation by logged-in user and price validation."""
    client.get('/logout')
    client.post('/login', data={'email': 'student@campusmart.edu', 'password': 'student123'})

    # 1. Reject negative price
    res_neg = client.post('/sell', data={
        'name': 'Invalid Product',
        'category': 'Other',
        'condition': 'Good',
        'price': '-50',
        'seller_name': 'Rahul',
        'seller_contact': '9876543210'
    }, follow_redirects=True)
    assert b"Price cannot be a negative value" in res_neg.data

    # 2. Valid creation
    res_valid = client.post('/sell', data={
        'name': 'Engineering Mechanics Dynamics',
        'description': 'Textbook by J.L. Meriam. Clean pages.',
        'category': 'Textbooks',
        'condition': 'Like New',
        'price': '420.00',
        'seller_name': 'Rahul Sharma',
        'seller_contact': 'student@campusmart.edu',
        'status': 'Available'
    }, follow_redirects=True)
    assert res_valid.status_code == 200
    assert b"Engineering Mechanics Dynamics" in res_valid.data


def test_unauthorized_user_cannot_access_protected_routes(client):
    """Verify guest user is redirected from /dashboard, /sell, and /wishlist."""
    client.get('/logout')

    res_sell = client.get('/sell')
    assert res_sell.status_code == 302
    assert '/login' in res_sell.headers['Location']

    res_dash = client.get('/dashboard')
    assert res_dash.status_code == 302
    assert '/login' in res_dash.headers['Location']

    res_wish = client.get('/wishlist')
    assert res_wish.status_code == 302
    assert '/login' in res_wish.headers['Location']


def test_student_cannot_access_admin_dashboard(client):
    """Verify regular student receives 403 Forbidden when requesting /admin."""
    client.get('/logout')
    client.post('/login', data={'email': 'student@campusmart.edu', 'password': 'student123'})
    res_admin = client.get('/admin')
    assert res_admin.status_code == 403
    assert b"403" in res_admin.data


def test_admin_can_access_admin_dashboard(client):
    """Verify administrator can access /admin."""
    client.get('/logout')
    client.post('/login', data={'email': 'admin@campusmart.edu', 'password': 'admin123'})
    res = client.get('/admin')
    assert res.status_code == 200
    assert b"Platform Administration" in res.data


def test_wishlist_add_and_remove(client):
    """Verify adding and removing items from wishlist."""
    client.get('/logout')
    # Login as Priya (user_id=3)
    client.post('/login', data={'email': 'priya@campusmart.edu', 'password': 'priya123'})

    # Find an existing product
    products = db.get_products()
    assert len(products) > 0
    target_product = products[0]
    prod_id = target_product['id']

    # Toggle into wishlist
    res_add = client.post(f'/wishlist/{prod_id}/toggle', follow_redirects=True)
    assert res_add.status_code == 200

    # Check wishlist page contains this item
    res_page = client.get('/wishlist')
    assert res_page.status_code == 200
    assert target_product['name'].encode() in res_page.data

    # Toggle again to remove
    res_remove = client.post(f'/wishlist/{prod_id}/toggle', follow_redirects=True)
    assert res_remove.status_code == 200
    assert b"removed from your wishlist" in res_remove.data


def test_ownership_enforcement_on_edit(client):
    """Verify user cannot edit another user's product."""
    client.get('/logout')
    # Find a product owned by user_id=2 (Rahul)
    rahul_prods = db.get_user_products(2)
    assert len(rahul_prods) > 0
    rahul_item_id = rahul_prods[0]['id']

    # Login as Priya Patel (user_id=3)
    client.post('/login', data={'email': 'priya@campusmart.edu', 'password': 'priya123'})
    
    # Try to edit Rahul's item
    res = client.get(f'/products/{rahul_item_id}/edit')
    assert res.status_code == 403
