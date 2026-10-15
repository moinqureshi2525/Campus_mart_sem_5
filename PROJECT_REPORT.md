# COLLEGE PROJECT REPORT

**PROJECT TITLE:** CampusMart Lite — Student Buy-and-Sell Website  
**DOMAIN:** Web Application Development & Database Management  
**ACADEMIC LEVEL:** Information Technology Engineering (Semester Project)  
**TECHNOLOGY STACK:** Python, Streamlit, SQLite3, HTML, CSS  

---

## 1. ABSTRACT

College students frequently purchase expensive textbooks, scientific calculators, stationery items, and laboratory kits that are utilized for a single academic semester and subsequently remain idle. Simultaneously, junior students entering the course require the identical educational materials at affordable prices. **CampusMart Lite** addresses this institutional challenge by providing a lightweight, responsive, and easy-to-use web-based marketplace tailored specifically for intra-campus peer-to-peer commerce. Built using Python, Streamlit, and SQLite3, the application enables students to browse listings, search and filter items across six academic categories, add new listings, modify prices and availability statuses, and contact peers directly. The architecture avoids external database dependencies, expensive cloud hosting, or complex authentication mechanisms, making it exceptionally reliable, simple to run locally, and ideal for academic evaluation.

---

## 2. INTRODUCTION

The rising cost of academic books, specialized engineering instruments, and laboratory materials poses an ongoing financial burden on undergraduate students. Traditional commercial marketplaces (such as Amazon or generic classifieds like OLX) are often ill-suited for immediate campus exchanges due to delivery lead times, shipping charges, and a lack of campus localization. CampusMart Lite establishes a straightforward localized portal where students within the same campus can list surplus academic gear and discover affordable essentials.

---

## 3. PROBLEM STATEMENT

At the conclusion of each academic semester:
1. Senior students possess textbooks, drafters, calculators, and lab components with negligible personal utility.
2. Incoming junior students spend significant sums purchasing brand new copies of identical resources.
3. Informal communication channels (such as generic messaging groups) suffer from message clutter, lack of categorization, inability to track whether an item has been sold, and zero search capability.

Therefore, an organized, lightweight, and dedicated digital bulletin board is required to streamline campus exchanges.

---

## 4. OBJECTIVES

The core objectives of the CampusMart Lite project are:
- To develop an intuitive, web-based platform for peer-to-peer student transactions.
- To provide full search and category-based filtering capabilities for academic equipment.
- To implement complete CRUD (Create, Read, Update, Delete) functionality for product listings.
- To maintain dynamic item availability statuses (`Available` vs `Sold`).
- To provide key marketplace metrics (Total Listings, Active Listings, Sold Items).
- To utilize an embedded SQLite database ensuring zero external server setup and 100% offline local operability.

---

## 5. SCOPE

### In-Scope:
- Presentation of available items in visually appealing responsive cards.
- Search listings by title keyword or item description.
- Filter listings by category (Textbooks, Calculators, Electronics, Stationery, Lab Equipment, Other).
- Listing management: adding items, editing prices/descriptions, toggling Available/Sold statuses, and confirmed deletion.
- Aggregated real-time marketplace counters.
- Development reset feature to reseed standard demonstration items during viva examinations.

### Out-of-Scope (Strict Scope Boundaries):
- User registration, login, and JWT/OAuth authentication.
- Online payment processing and digital wallets.
- Image file uploads and cloud storage.
- Real-time in-app chat or messaging systems.
- Administrative permission tiers.

---

## 6. EXISTING SYSTEM

In most universities, students currently rely on:
- **Physical College Notice Boards:** High latency, low reach, cannot be searched or updated once posted.
- **WhatsApp / Telegram Groups:** Unstructured messages that quickly get buried in chat feeds; no way to filter by price or category; impossible to know if an item was already purchased.
- **Commercial Classifieds (OLX / Quikr):** General public visibility increases scam risk; physical delivery is inconvenient compared to meeting directly in college corridors or libraries.

---

## 7. PROPOSED SYSTEM

CampusMart Lite solves these issues by providing:
- **Centralized Database:** All academic items are structured with clear attributes (price, seller contact, category, condition).
- **Instant Search & Categorization:** Find specific books or instruments within seconds.
- **Status Transparency:** Items marked as "Sold" clearly notify students, preventing redundant inquiries.
- **Zero Configuration:** Leverages Streamlit and SQLite, launching with a single Python command on any Windows PC.

---

## 8. HARDWARE AND SOFTWARE REQUIREMENTS

### Hardware Requirements:
- **Processor:** Intel Core i3 / AMD Ryzen 3 or higher
- **RAM:** Minimum 2 GB (4 GB recommended)
- **Hard Disk:** 200 MB free disk space
- **Display:** 1366 x 768 or higher resolution

### Software Requirements:
- **Operating System:** Microsoft Windows 10 / 11
- **Language / Runtime:** Python 3.8+ (Tested on Python 3.14)
- **Web Framework:** Streamlit (v1.35+)
- **Database Engine:** SQLite 3 (Standard Python Library `sqlite3`)
- **Web Browser:** Google Chrome, Microsoft Edge, Mozilla Firefox, or Safari

---

## 9. SYSTEM ARCHITECTURE

```
+-------------------------------------------------------------------+
|                        Client Web Browser                         |
|           (http://localhost:8501 - Streamlit Reactive UI)         |
+-------------------------------------------------------------------+
                                  │
                                  │ HTTP / WebSockets
                                  ▼
+-------------------------------------------------------------------+
|                     Streamlit Application (app.py)                 |
|  - Page Layout & Header Injection                                 |
|  - Sidebar Navigation (Home, Browse, Add Product, Manage Listings)|
|  - Form Processing, Validation & User Feedback                    |
+-------------------------------------------------------------------+
                                  │
                                  │ Python Function Calls
                                  ▼
+-------------------------------------------------------------------+
|                    Database Module (database.py)                  |
|  - Parameterized SQL CRUD Execution                               |
|  - Demo Data Initialization & Seeding                             |
|  - Query Filtering & Aggregate Metrics Generation                 |
+-------------------------------------------------------------------+
                                  │
                                  │ File I/O
                                  ▼
+-------------------------------------------------------------------+
|                     SQLite Database (campusmart.db)               |
|  - Table: products                                                |
+-------------------------------------------------------------------+
```

---

## 10. MODULE DESCRIPTION

1. **Database Module (`database.py`):**
   - Manages connection lifecycle via `sqlite3.connect()`.
   - `init_db()`: Automatically creates the `products` table and seeds 6 realistic student listings if empty.
   - `add_product()`: Safely inserts new listings using parameterized queries (`?` placeholders).
   - `get_all_products()`: Constructs dynamic SQL queries supporting keyword searches and multi-parameter filters.
   - `update_product()` & `update_product_status()`: Modifies existing records and toggles `Available` / `Sold` flags.
   - `delete_product()`: Permanently drops a record by ID.
   - `get_statistics()`: Computes total, available, and sold product quantities.

2. **Web Interface Module (`app.py`):**
   - **Header & Metrics Banner:** Displays application branding and key live figures.
   - **Home View:** Introductory text and orientation guide.
   - **Browse Products View:** Displays cards in a 2-column responsive layout with price tags, category chips, and seller contact blocks.
   - **Add Product View:** Controlled form with input validation (preventing empty titles or negative prices).
   - **Manage Listings View:** Selection dropdown to inspect records, quick status toggling, and protected deletion requiring checkbox confirmation.
   - **Developer Options:** Sidebar tool to reset database to initial demonstration listings.

---

## 11. DATABASE DESIGN

The system uses a single normalized table named `products` stored in `campusmart.db`.

### Table Name: `products`

| Column Name | Data Type | Constraints | Description |
|:---|:---|:---|:---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique identifier for each listing |
| `name` | TEXT | NOT NULL | Title of the product / book / equipment |
| `description` | TEXT | NULLABLE | Detailed description, condition, or edition |
| `category` | TEXT | NOT NULL | One of 6 predefined campus categories |
| `price` | REAL | NOT NULL | Price in Indian Rupees (₹) |
| `seller_name` | TEXT | NOT NULL | Full name of the student selling the item |
| `seller_contact`| TEXT | NOT NULL | Mobile number or campus email |
| `status` | TEXT | DEFAULT 'Available' | Current availability ('Available' or 'Sold') |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Date and time when the listing was created |

---

## 12. IMPLEMENTATION

The application is implemented in clean, idiomatic Python using the Streamlit library. Key implementation principles include:
- **Parameterized SQL:** All queries utilize `?` parameters to eliminate SQL injection vulnerabilities.
- **Row Factory:** SQLite `conn.row_factory = sqlite3.Row` is configured so database records can be accessed cleanly by field names.
- **Component Isolation:** Database operations are entirely encapsulated in `database.py`, keeping presentation logic in `app.py` clean and readable.
- **Defensive Deletion:** Accidental data removal is prevented via mandatory confirmation checkboxes.

---

## 13. TESTING

Functional, unit, and integration tests were conducted:
- **Initialization Test:** Verified automatic database file and table creation upon startup.
- **Data Persistence Test:** Confirmed that newly posted listings remain stored in SQLite even after restarting the Streamlit server.
- **Search & Filter Test:** Verified SQL `LIKE` queries correctly filter items by keywords and categories.
- **Boundary Validation:** Verified that empty forms or negative price values are rejected with informative error alerts.

Refer to [`TEST_CHECKLIST.md`](file:///c:/Users/ADMIN/Desktop/sem5_project/TEST_CHECKLIST.md) for individual test cases and pass results.

---

## 14. ADVANTAGES

- **Zero Cloud Costs:** Runs 100% locally on standard college computer lab systems or student laptops.
- **No Setup Hassle:** No external server installations (no XAMPP, MySQL Server, Docker, or Node.js).
- **Student-Centric:** Designed specifically for campus items like calculators, lab coats, and engineering textbooks.
- **Clean UI:** Responsive cards, intuitive navigation, and real-time metric indicators.
- **Secure by Design:** Uses parameterized SQL queries and defensive confirmation dialogs.

---

## 15. LIMITATIONS

- Designed for local execution within a single network/machine; multi-user concurrent cloud deployment requires external hosting.
- Image uploads are omitted in version 1.0 to prioritize simplicity and eliminate binary file management.
- Does not authenticate user identities with passwords or college ID cards.

---

## 16. FUTURE SCOPE

- **Student Authentication:** Integration of college email OTP verification (`@college.edu`).
- **Image Support:** Storing and displaying actual photos of book covers or equipment conditions.
- **Chatbot / Direct Messaging:** Internal message exchange between buyer and seller.
- **Hostel / Department Tags:** Filter listings by specific campus hostels or engineering departments.

---

## 17. CONCLUSION

**CampusMart Lite** successfully fulfills the objective of creating a simple, functional, and reliable buy-and-sell web application for university students. By focusing on essential marketplace features, clean code architecture, and an embedded SQLite database, the project achieves maximum usability with minimal maintenance overhead. The project stands complete, verified, and ready for college presentation and viva voce examination.
