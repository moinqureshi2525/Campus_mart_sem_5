# CampusMart — Student Buy-and-Sell Web Application

A full-stack student marketplace built with **Python Flask**, **Bootstrap 5**, and **SQLite3** for college students to buy and sell second-hand textbooks, calculators, stationery, and lab equipment.

Developed for **Semester 5 Information Technology Mini Project**.

---

## 🚀 Key Features

- **Modern Responsive Design:** Professional navy & indigo color palette, responsive cards, hover effects, and clean typography.
- **Browse & Filter:** Search by keywords, filter by category (`Textbooks`, `Calculators`, `Electronics`, `Stationery`, `Lab Equipment`, `Other`), condition, and price range, with sorting by newest and price.
- **Product Details & Direct Contact:** Detailed view with condition tags, date listed, and seller contact details.
- **Sell an Item:** Controlled listing form with price validation and safe image uploading.
- **Authentication & Security:** User registration, login, logout, Werkzeug salted password hashing, and custom CSRF protection.
- **Student Wishlist:** Bookmark favorite items with duplicate prevention.
- **Seller Dashboard:** View active/sold counts, edit listings, toggle `Available`/`Sold` status, and delete items.
- **Admin Control Center:** Platform overview with user moderation, listing oversight, Chart.js category distribution chart, and one-click demo data reset.

---

## 🛠️ Technology Stack

- **Backend:** Python Flask 3.1
- **Database:** SQLite3 (parameterized queries, foreign keys enabled)
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5.3, Bootstrap Icons 1.11
- **Data Visualization:** Chart.js
- **Testing:** Pytest

---

## 📁 Project Structure

```text
CampusMart/
├── app.py                      # Flask routes, auth, session checks, CSRF, and file upload
├── database.py                 # SQLite helper, schema migration, CRUD, and demo data
├── schema.sql                  # Database schema definitions
├── requirements.txt            # Python dependencies (Flask, Werkzeug, pytest)
├── README.md                   # Setup guide and presentation sequence
├── .env.example                # Example environment configuration
├── .gitignore                  # Git ignore rules
├── uploads/                    # Local directory for user uploaded product images
├── static/
│   ├── css/style.css           # Custom design system and components
│   ├── js/main.js              # Client helpers (alerts, file preview)
│   └── images/placeholder.svg  # Default product placeholder illustration
├── templates/
│   ├── base.html               # Shared navbar, flash messages, and footer
│   ├── index.html              # Home landing page with hero & metrics
│   ├── products.html           # Browse & search with filter sidebar
│   ├── product_detail.html     # Detailed item view and seller contact
│   ├── sell_product.html       # Post item form with image upload
│   ├── edit_product.html       # Edit listing and delete option
│   ├── login.html              # User login page
│   ├── register.html           # User registration page
│   ├── wishlist.html           # Saved items page
│   ├── seller_dashboard.html   # Personal seller management table
│   ├── admin_dashboard.html    # Admin moderation & Chart.js analytics
│   ├── 403.html                # Access forbidden template
│   └── 404.html                # Page not found template
├── tests/
│   └── test_app.py             # 12 automated test cases (pytest)
└── documentation/
    ├── PROJECT_REPORT.md       # Complete 20-section college report
    ├── DATABASE_DESIGN.md      # ER model and table documentation
    ├── TEST_CASES.md           # Test cases and verification report
    └── VIVA_QUESTIONS.md       # 10 essential viva Q&A for examiners
```

---

## ⚡ Quick Start Instructions (Windows)

### 1. Open Terminal in Project Folder
```powershell
cd c:\Users\ADMIN\Desktop\sem5_project
```

### 2. (Optional) Create & Activate Virtual Environment
```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```
*(Or use `py -m pip install -r requirements.txt`)*

### 4. Run the Web Application
```powershell
python app.py
```
*(Or use `py app.py`)*

Open your browser at:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🔑 Pre-Configured Demo Accounts

For college presentation and testing, the following accounts are ready to use:

| Role | Email | Password | Access / Purpose |
|:---|:---|:---|:---|
| **Student (Seller 1)** | `student@campusmart.edu` | `student123` | Rahul Sharma (owns textbooks, lab kit listings) |
| **Student (Seller 2)** | `priya@campusmart.edu` | `priya123` | Priya Patel (owns calculator, drafter listings) |
| **Administrator** | `admin@campusmart.edu` | `admin123` | CampusMart Admin (access to `/admin` dashboard) |

*You can also register any new student account directly from the website.*

---

## 🧪 Running Automated Tests

To run the complete automated test suite:
```powershell
py -m pytest -v tests/test_app.py
```
Expected output: **`12 passed in < 1.0s`**

---

## 👨‍🏫 Demonstration Sequence for College Viva / Professor

Follow this 5-minute walkthrough to demonstrate your project:

1. **Home Page & Metrics:**
   - Open `http://127.0.0.1:5000`.
   - Point out the navy/indigo brand design, hero banner, search bar, category shortcuts, live database counters, and recently listed items.
2. **Browse, Search & Filter:**
   - Click **Browse Products**.
   - Type `Calculator` in the search bar to demonstrate real-time SQL filtering.
   - Select Category `Textbooks` and adjust price min/max filters to show multi-parameter filtering.
3. **Product Details & Wishlist:**
   - Click **View Details** on any listing to show condition, listed date, and seller contact details.
   - Click **Login to Save to Wishlist** to demonstrate protected route redirection.
   - Log in using `student@campusmart.edu` / `student123`.
   - Click **Add to Wishlist** and open the **Wishlist** page to show saved items.
4. **Post an Item for Sale:**
   - Click **Sell an Item**.
   - Fill in:
     - Title: `Operating System Concepts (Galvin, 9th Edition)`
     - Category: `Textbooks`
     - Condition: `Like New`
     - Price: `450`
   - Upload an optional product image or leave blank for default SVG illustration.
   - Submit and show that the new listing immediately appears on the platform.
5. **Seller Dashboard & Status Toggle:**
   - Click **Dashboard** in the top navigation.
   - Show personal statistics (total, active, sold).
   - Click the green checkmark button to mark the item as **Sold**. Show that the status badge changes to red `Sold` across the whole platform.
6. **Administrator Oversight & Chart.js:**
   - Log out and log in as `admin@campusmart.edu` / `admin123`.
   - Click **Admin** in the navbar.
   - Show the interactive **Chart.js Category Distribution** doughnut chart, the registered student accounts table, and moderation controls.
   - Explain that regular students receive an **HTTP 403 Forbidden** if they attempt to access `/admin`.
