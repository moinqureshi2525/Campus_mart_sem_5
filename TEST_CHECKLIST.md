# TEST CHECKLIST: CAMPUSMART LITE

This document records the functional verification and test cases executed for **CampusMart Lite**.

---

## 🧪 Functional Test Suite

| Test Case ID | Feature / Module | Test Description | Expected Result | Actual Result | Status |
|:---:|:---|:---|:---|:---|:---:|
| **TC-01** | Database Initialization | Launch app or run `database.py` when database does not exist. | Creates `campusmart.db` and populates 6 demonstration records. | `campusmart.db` created; 6 demo records seeded. | **PASS** |
| **TC-02** | Home Page Metrics | View Home screen with initial demo data. | Displays 6 total listings, 5 available, 1 sold. | Metrics rendered accurately as cards. | **PASS** |
| **TC-03** | Sidebar Navigation | Switch between Home, Browse, Add Product, and Manage Listings. | Relevant view renders seamlessly without error. | Smooth navigation between all 4 views. | **PASS** |
| **TC-04** | Product Search | Search for keyword `Calculator` in Browse Products. | Only listings with 'Calculator' in title/description are shown. | Casio scientific calculator displayed. | **PASS** |
| **TC-05** | Category Filter | Select category `Textbooks` from dropdown. | Only textbook listings are shown. | Displays B.S. Grewal & Data Structures books. | **PASS** |
| **TC-06** | Status Filter | Select status `Sold` from dropdown. | Displays only items marked as Sold. | Displays Engineering Drawing Kit. | **PASS** |
| **TC-07** | Empty Search State | Search for non-existent keyword `Quantum999`. | Helpful warning message informs student that no items match. | "No listings found matching your search criteria." displayed. | **PASS** |
| **TC-08** | Add Product Validation | Submit Add Product form with empty title or contact. | Displays clear error message requiring mandatory fields. | Validation errors displayed; record not saved. | **PASS** |
| **TC-09** | Add Product Success | Submit valid form (e.g. Lab Coat & Goggles, ₹350). | Inserts record into database; displays success alert with ID. | Success message displayed; listing persists in DB. | **PASS** |
| **TC-10** | Edit Product Listing | Update product price or description in Manage Listings. | Changes are saved to SQLite and reflected immediately. | Updated price/description saved and displayed. | **PASS** |
| **TC-11** | Quick Status Toggle | Click `Mark as Sold` or `Mark as Available`. | Toggles status between Available and Sold. | Status badge toggles between green and red instantly. | **PASS** |
| **TC-12** | Delete Confirmation | Attempt delete without checking confirmation box. | Blocks deletion and shows warning requiring checkbox check. | Warning displayed; listing preserved. | **PASS** |
| **TC-13** | Delete Product Success | Check confirmation box and click Delete Listing. | Removes record from database; updates metrics. | Record deleted; total count decreases by 1. | **PASS** |
| **TC-14** | Reset Demo Data | Check confirmation and click Reset to Demo Data. | Resets database back to default 6 demonstration products. | Database reseeded; initial 6 demo items restored. | **PASS** |
| **TC-15** | Persistence Check | Restart application or query database directly. | Data survives server restart without data loss. | Verified with SQLite query and server restart. | **PASS** |

---

## 📋 Summary

- **Total Test Cases:** 15
- **Passed:** 15
- **Failed:** 0
- **Overall Result:** 100% Pass Rate. Ready for College Demonstration and Viva.
