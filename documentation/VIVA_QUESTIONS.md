# VIVA VOCE EXAMINATION QUESTIONS & ANSWERS
## CampusMart — Student Buy-and-Sell Web Application

This guide prepares you to answer common theoretical and practical questions asked by external examiners and professors during your Semester 5 IT mini project viva.

---

### Q1: What is the main objective of your project?
**Answer:**  
CampusMart is an intra-campus student marketplace web application that allows college students to buy and sell pre-owned educational items such as engineering textbooks, scientific calculators, stationery kits, and laboratory equipment directly with their peers. It solves the problem of high textbook costs and semester-end unused equipment.

---

### Q2: What is the technology stack used, and why did you choose it?
**Answer:**
- **Backend:** Python Flask. Flask is a lightweight WSGI microframework that allows clean routing, session management, and template rendering without heavy boilerplate.
- **Frontend:** HTML5, CSS3, JavaScript, and Bootstrap 5 with Bootstrap Icons for a modern, responsive user experience.
- **Database:** SQLite3. It is serverless, zero-configuration, and integrated directly into Python's standard library, making it lightweight and reliable for local execution.
- **Security:** Werkzeug crypto library for secure password hashing and custom CSRF protection tokens.
- **Charts:** Chart.js for data visualization on the Administrator dashboard.

---

### Q3: How do you prevent SQL Injection attacks in your application?
**Answer:**  
We avoid string concatenation or formatting (such as `f"SELECT ... {input}"`) when querying the database. Instead, we use **parameterized queries** with SQLite placeholder `?` marks:
```python
cursor.execute("SELECT * FROM products WHERE category = ?", (category,))
```
The database driver treats the parameters strictly as data literals, rendering SQL injection impossible.

---

### Q4: How are user passwords stored in the database?
**Answer:**  
Passwords are never stored in plaintext. We utilize Werkzeug's `generate_password_hash()` function, which uses strong, salted one-way hashing algorithms (`scrypt` or `pbkdf2:sha256`). When a user logs in, `check_password_hash()` compares the hash of the provided password against the stored hash.

---

### Q5: How does session management and access control work?
**Answer:**  
When a user logs in successfully, their `user_id`, `user_name`, `user_email`, and `user_role` are stored in Flask's client-side cryptographically signed session (`session['user_id']`). We created two custom Python decorators:
1. `@login_required`: Checks if `session.get('user_id')` exists; if not, it redirects to the login page.
2. `@admin_required`: Ensures both that the user is logged in and that `session.get('user_role') == 'admin'`; otherwise, it returns an HTTP 403 Forbidden status.

---

### Q6: How do you prevent a student from modifying or deleting another student's listing?
**Answer:**  
In the edit, toggle-status, and delete route handlers, we query the product by ID from SQLite and verify its `user_id` against the currently logged-in user's session:
```python
if product['user_id'] != session.get('user_id') and session.get('user_role') != 'admin':
    abort(403)
```
If the IDs do not match and the user is not an administrator, the server halts execution with a 403 Forbidden response.

---

### Q7: What are the main tables in your database schema?
**Answer:**  
The database consists of three relational tables:
1. `users`: Stores user credentials (`id`, `name`, `email` [UNIQUE], `password_hash`, `role`, `created_at`).
2. `products`: Stores product listings (`id`, `user_id` [FK], `name`, `description`, `category`, `price`, `condition`, `image_filename`, `seller_name`, `seller_contact`, `status`, `created_at`, `updated_at`).
3. `wishlist`: Junction table for bookmarked items (`id`, `user_id` [FK], `product_id` [FK], `created_at`) with a `UNIQUE(user_id, product_id)` constraint to prevent duplicate bookmarks.

---

### Q8: How does the file upload feature handle security?
**Answer:**  
- **Extension check:** Only specific image extensions (`png`, `jpg`, `jpeg`, `webp`) are allowed.
- **Filename sanitization:** We generate a cryptographically random hexadecimal filename (`secrets.token_hex(8)`) combined with `secure_filename()` to prevent directory traversal attacks (e.g., `../../etc/passwd`).
- **File size limit:** Flask's `MAX_CONTENT_LENGTH` is capped at 5 MB to prevent server denial-of-service via huge file uploads.

---

### Q9: What is CSRF and how do you protect against it?
**Answer:**  
Cross-Site Request Forgery (CSRF) is an attack where an unauthorized command is transmitted from a trusted user. We generate a random session-bound cryptographic token (`csrf_token()`) and validate it before processing any state-altering `POST`, `PUT`, or `DELETE` requests. If the token is missing or mismatched, the request is rejected with a 403 status.

---

### Q10: What are the limitations and potential future enhancements of this project?
**Answer:**
- **Current Limitations:** Runs locally within a single network; payments and real-time chat are not included to preserve simplicity and avoid external paid APIs.
- **Future Enhancements:** Institutional email OTP verification (`@college.edu`), real-time in-app chat via WebSockets, and department-specific filtering.
