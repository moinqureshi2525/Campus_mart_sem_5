# DATABASE DESIGN SPECIFICATION: CAMPUSMART

## 1. Overview
The **CampusMart** relational database is implemented using **SQLite3**. It supports student peer-to-peer commerce, credential protection, product listings with lifecycle tracking, and personal wishlists.

Database File: `campusmart.db`

---

## 2. Entity-Relationship (ER) Model

```
+------------------+         1 : N         +--------------------+
|      USERS       | --------------------> |      PRODUCTS      |
|------------------|                       |--------------------|
| id (PK)          |                       | id (PK)            |
| name             |                       | user_id (FK)       |
| email (UNIQUE)   |                       | name               |
| password_hash    |                       | description        |
| role             |                       | category           |
| created_at       |                       | price              |
+------------------+                       | condition          |
        | 1                                | image_filename     |
        |                                  | seller_name        |
        |                                  | seller_contact     |
        | N                                | status             |
        v                                  | created_at         |
+------------------+                       | updated_at         |
|     WISHLIST     |                       +--------------------+
|------------------|                                 ^
| id (PK)          |                                 |
| user_id (FK)     | --------------------------------+
| product_id (FK)  |               N : 1
| created_at       |
+------------------+
```

---

## 3. Relational Schema & Tables

### Table 1: `users`
Stores student and administrator user credentials.

| Column | Data Type | Constraints | Description |
|:---|:---|:---|:---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique identifier for each user |
| `name` | TEXT | NOT NULL | User's full name |
| `email` | TEXT | UNIQUE NOT NULL | College email address (used as login username) |
| `password_hash` | TEXT | NOT NULL | Password hash generated via Werkzeug (`scrypt`/`pbkdf2`) |
| `role` | TEXT | DEFAULT 'student' | Access role: `'student'` or `'admin'` |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Registration timestamp |

### Table 2: `products`
Stores marketplace product listings created by student sellers.

| Column | Data Type | Constraints | Description |
|:---|:---|:---|:---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique listing identifier |
| `user_id` | INTEGER | FOREIGN KEY REFERENCES `users(id)` | Owner user account ID |
| `name` | TEXT | NOT NULL | Title of the product / book / equipment |
| `description` | TEXT | NULLABLE | Detailed description and condition notes |
| `category` | TEXT | NOT NULL | One of: `Textbooks`, `Calculators`, `Electronics`, `Stationery`, `Lab Equipment`, `Other` |
| `price` | REAL | NOT NULL | Price in Indian Rupees (₹) |
| `condition` | TEXT | DEFAULT 'Good' | Item condition: `'New'`, `'Like New'`, `'Good'`, `'Used'` |
| `image_filename`| TEXT | DEFAULT 'placeholder.svg' | Filename in `uploads/` or default asset |
| `seller_name` | TEXT | NOT NULL | Display name of the seller |
| `seller_contact`| TEXT | NOT NULL | Phone number or college email for inquiries |
| `status` | TEXT | DEFAULT 'Available' | Availability: `'Available'` or `'Sold'` |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Listing creation date |
| `updated_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Last modification date |

### Table 3: `wishlist`
Stores bookmarked items saved by students.

| Column | Data Type | Constraints | Description |
|:---|:---|:---|:---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique bookmark ID |
| `user_id` | INTEGER | FOREIGN KEY REFERENCES `users(id)` ON DELETE CASCADE | ID of student bookmarking the item |
| `product_id` | INTEGER | FOREIGN KEY REFERENCES `products(id)` ON DELETE CASCADE | ID of bookmarked product |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Bookmark creation timestamp |

*Constraint:* `UNIQUE(user_id, product_id)` ensures a student cannot bookmark the same product more than once.

---

## 4. Query Optimization & Security
- **Foreign Keys Enabled:** `PRAGMA foreign_keys = ON;` is enforced on every database connection.
- **Parameterized SQL:** All SQL operations use Python standard `?` positional parameters. No string formatting or concatenation is used, eliminating SQL injection.
- **Row Factory:** Enabled `conn.row_factory = sqlite3.Row` for safe column-name-based dictionary indexing.
