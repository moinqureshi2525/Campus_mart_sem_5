# CAMPUSMART — STUDENT BUY-AND-SELL MARKETPLACE
## Semester 5 Information Technology Mini Project Report

---

### 1. TITLE OF THE PROJECT
**CampusMart: A Secure, Lightweight Peer-to-Peer Student Marketplace Web Application**

---

### 2. ABSTRACT
The recurring financial burden of purchasing specialized engineering textbooks, high-precision scientific calculators, engineering graphics equipment, and electronic laboratory kits is a pervasive concern for college students. Once a semester finishes, these costly resources often lie dormant. **CampusMart** provides an intuitive, web-based, campus-localized buy-and-sell portal designed exclusively for college environments. Developed with **Python Flask**, **Bootstrap 5**, and an **embedded SQLite** database, CampusMart allows students to list surplus items, search and filter listings across engineering categories, bookmark items in a personal wishlist, manage their postings via a seller dashboard, and communicate directly with fellow students. The system integrates robust server-side validation, salted cryptographic password hashing, role-based session authorization, image upload sanitization, and parameterized SQL queries to prevent SQL injection.

---

### 3. INTRODUCTION
In higher education institutions, particularly engineering and technology colleges, students require distinct textbooks, lab apparatus, and tools for each semester. Commercial e-commerce platforms and broad classified portals (such as OLX) do not cater to the rapid, trust-based, and zero-delivery-cost nature of peer interactions on a college campus. CampusMart bridges this gap by creating an intra-campus academic marketplace where transactions occur face-to-face in libraries, classrooms, or cafeterias without middleman commissions.

---

### 4. PROBLEM STATEMENT
Students currently face the following problems:
1. **Financial Inefficiency:** Senior students have books and kits that they no longer require, while juniors purchase the same items brand new at full retail prices.
2. **Unstructured Communication:** Relying on unofficial messaging groups leads to spam, rapid message loss, lack of categorized searching, and no way to identify whether an item is still available or already sold.
3. **Complexity of Commercial Marketplaces:** Commercial platforms require courier shipping, charge transaction fees, and expose students to external public risks.

---

### 5. OBJECTIVES
The principal objectives of CampusMart are:
- To provide a modern, responsive web application for college student commerce.
- To implement full CRUD capabilities for academic product listings.
- To enable multi-criteria search and filtering (keyword, branch category, item condition, price boundaries, and sorting).
- To provide secure student authentication with salted password hashing and role-based permissions (Student vs. Administrator).
- To feature personal seller dashboards and student wishlists.
- To incorporate an administrator oversight dashboard with Chart.js analytics for category distribution.
- To operate 100% locally with zero cloud dependencies or external paid APIs.

---

### 6. SCOPE OF THE PROJECT
- **In-Scope:**
  - Responsive web interface designed using Bootstrap 5 and custom CSS.
  - Multi-parameter search and dynamic category filtering.
  - User registration, login, logout, and password hashing using Werkzeug.
  - Listing creation with optional image upload and file validation.
  - Seller dashboard with aggregate listing metrics and one-click status toggling (`Available` / `Sold`).
  - Personal student wishlist.
  - Administrator portal with platform moderation and Chart.js analytics.
  - Parameterized SQLite3 queries for database security.
- **Out-of-Scope:**
  - Third-party payment gateways (transactions happen physically in person).
  - Machine learning recommendation algorithms.
  - Live chat servers or SMS gateways.

---

### 7. EXISTING SYSTEM AND ITS LIMITATIONS
Existing informal channels include:
- **College Noticeboards:** Static, paper-based, low visibility, cannot be updated or searched.
- **WhatsApp / Telegram Groups:** Unorganized feed, message deluge, lack of search and price filters, no way to track sold items.
- **General Classifieds (OLX, Quikr):** General public exposure increases fraud risk; items cannot be easily inspected during class hours.

---

### 8. PROPOSED SYSTEM
CampusMart provides a dedicated, organized web application:
- **Centralized Database:** Structured attributes for author, edition, price, condition, and seller contact.
- **Dynamic Search & Filtering:** Instant keyword matching, category filtering, and price range isolation.
- **Live Lifecycle Tracking:** Instant badges indicating whether an item is `Available` or `Sold`.
- **Zero Cost Deployment:** Runs easily on any Windows laptop without database servers.

---

### 9. HARDWARE AND SOFTWARE REQUIREMENTS
- **Hardware:** Intel Core i3 / AMD Ryzen 3 or higher, 2 GB RAM minimum, 200 MB disk space.
- **Operating System:** Microsoft Windows 10 / 11, Linux, or macOS.
- **Backend Framework:** Python 3.8+ with Flask 3.1.
- **Database:** SQLite3 with foreign keys enabled.
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5.3, Bootstrap Icons 1.11, Chart.js.
- **Browser:** Google Chrome, Microsoft Edge, Firefox, or Safari.

---

### 10. SYSTEM ARCHITECTURE
The application follows the Model-View-Controller (MVC) architectural pattern:
- **Model (`database.py`, `schema.sql`):** SQLite connection, schema migrations, and parameterized CRUD operations.
- **View (`templates/`, `static/`):** Jinja2 templates, Bootstrap 5 components, and custom CSS.
- **Controller (`app.py`):** Flask route handlers, input validation, session management, CSRF enforcement, and file uploads.

---

### 11. MODULE DESCRIPTIONS
1. **Authentication Module:** Handles registration, login, password hashing, and session management.
2. **Product Catalog & Search Module:** Displays responsive cards with keyword search, category filtering, and price sorting.
3. **Listing Management Module:** Allows authorized students to add, edit, toggle availability, and delete listings.
4. **Wishlist Module:** Allows students to bookmark items with duplicate prevention.
5. **Seller Dashboard Module:** Provides individual metrics (total, active, sold) and table management.
6. **Administrator Module:** Provides oversight, user lists, listing removal, and category distribution charts.

---

### 12. USE-CASE DESCRIPTION
- **Student (Buyer):** Browse catalog, filter by price/category, view seller contact, bookmark to wishlist.
- **Student (Seller):** Register account, upload item with image and condition, edit listing, mark as sold.
- **Administrator:** Log in with admin credentials, inspect platform statistics, review all users and listings, remove inappropriate content, reset demo data.

---

### 13. DATABASE DESIGN AND RELATIONSHIPS
- **`users` (1) to `products` (N):** One student can list multiple items.
- **`users` (1) to `wishlist` (N):** One student can save multiple wishlist items.
- **`products` (1) to `wishlist` (N):** A product can be saved by multiple students.
Refer to [`DATABASE_DESIGN.md`](file:///c:/Users/ADMIN/Desktop/sem5_project/documentation/DATABASE_DESIGN.md) for table schemas and constraints.

---

### 14. EXPLANATION OF CRUD OPERATIONS
- **Create:** `INSERT INTO products (...) VALUES (?, ?)` with validated prices and sanitized image filenames.
- **Read:** `SELECT * FROM products WHERE 1=1 AND category = ? ...` with parameterized filters.
- **Update:** `UPDATE products SET name = ?, price = ? ... WHERE id = ?` with seller ownership checks.
- **Delete:** `DELETE FROM products WHERE id = ?` with ownership verification and confirmation prompts.

---

### 15. IMPLEMENTATION DETAILS
- **Password Security:** Hashes passwords with salt using `werkzeug.security.generate_password_hash()`.
- **CSRF Token Verification:** Tokens validated on all state-altering requests (`POST`, `PUT`, `DELETE`).
- **Safe File Uploads:** Validates MIME extensions, randomizes file prefixes, and enforces 5 MB size caps.

---

### 16. TESTING AND TEST RESULTS
Automated testing conducted using Pytest:
- **12/12 Automated Tests Passed (100% Pass Rate).**
- Tests verified route accessibility, registration, duplicate rejection, login/logout, password hashing, price validation, unauthorized access blocks, role enforcement, wishlist operations, and edit ownership constraints.
Refer to [`TEST_CASES.md`](file:///c:/Users/ADMIN/Desktop/sem5_project/documentation/TEST_CASES.md) for full records.

---

### 17. ADVANTAGES
- **Campus Focused:** Tailored specifically for student academic resources.
- **Professional UI:** Navy/indigo theme, responsive Bootstrap 5 layout, clean typography.
- **Secure Architecture:** Parameterized queries, salted password hashes, CSRF protection.
- **Zero Maintenance:** Embedded SQLite database with zero external configuration.

---

### 18. LIMITATIONS
- System operates within a local network or single host machine; internet deployment requires a production WSGI server.
- Omits live chat and online payment gateways to keep the codebase simple and appropriate for a college mini project.

---

### 19. FUTURE SCOPE
- Institutional email verification (`@college.edu`).
- Real-time notifications and in-app chat between buyers and sellers.
- Hostel and branch-specific location tags.

---

### 20. CONCLUSION
CampusMart successfully achieves the goals of a Semester 5 Information Technology mini project by delivering a clean, functional, and secure campus marketplace. The project demonstrates solid full-stack engineering fundamentals, database integrity, and practical web security.
