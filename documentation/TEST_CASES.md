# FUNCTIONAL TEST CASES & VERIFICATION REPORT

**PROJECT:** CampusMart — Student Buy-and-Sell Platform  
**TEST RUNNER:** Pytest 9.1.1 & Manual End-to-End Walkthrough  
**TOTAL TESTS:** 12 Automated Suite Tests + Manual Checks  
**STATUS:** ALL PASSED (100%)  

---

## Automated Test Cases (`tests/test_app.py`)

| Test ID | Module | Scenario / Description | Expected Behavior | Actual Outcome | Status |
|:---:|:---|:---|:---|:---|:---:|
| **TC-01** | Public UI | Home page loading (`GET /`) | Status 200, CampusMart branding, metrics, and hero loaded. | Status 200 OK, full layout rendered. | **PASS** |
| **TC-02** | Search | Search query `GET /products?q=Calculator` | Returns Casio Scientific Calculator in listing results. | Calculator listing returned in HTML response. | **PASS** |
| **TC-03** | Category Filter | Category filter `GET /products?category=Textbooks` | Only textbook listings returned. | Textbook products displayed. | **PASS** |
| **TC-04** | User Auth | New student registration (`POST /register`) | Account created, auto logged-in, session set. | Redirects to home with welcome alert. | **PASS** |
| **TC-05** | User Auth | Duplicate email registration (`POST /register`) | Rejected with clear flash error. | "Email address is already registered." displayed. | **PASS** |
| **TC-06** | User Auth | User Login & Logout (`POST /login`, `GET /logout`) | Validates password, sets session, and clears on logout. | Successfully sets session and clears on logout. | **PASS** |
| **TC-07** | Security | Password hashing verification | Passwords stored with irreversible salted hashes. | Verified hash begins with `scrypt:` / `pbkdf2:`. | **PASS** |
| **TC-08** | Validation | Negative price rejection (`POST /sell`) | Rejects form with validation error. | "Price cannot be a negative value" shown. | **PASS** |
| **TC-09** | Access Control | Unauthorized access to protected routes | Redirects unauthenticated guest to login. | HTTP 302 redirect to `/login` verified. | **PASS** |
| **TC-10** | Role Security | Student access to admin area (`GET /admin`) | Blocks regular student with HTTP 403. | HTTP 403 Forbidden verified. | **PASS** |
| **TC-11** | Role Security | Admin access to admin area (`GET /admin`) | Allows authorized admin with HTTP 200. | Admin dashboard loaded with stats and table. | **PASS** |
| **TC-12** | Wishlist | Toggle item in/out of wishlist | Adds to user's saved items, removes on second toggle. | Wishlist table updated and verified. | **PASS** |
| **TC-13** | Ownership | Edit ownership enforcement (`GET /products/<id>/edit`) | Prevents student from editing another student's item. | HTTP 403 Forbidden returned when user != owner. | **PASS** |

---

## Summary
- Automated Unit & Integration Tests: **12/12 Passed**
- Database Persistence Check: **Passed** (data verified across app reloads)
- CSRF Protection: **Passed** (validates session tokens on all state-altering POST requests)
