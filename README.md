# 🏠 Nestora — PG & Accommodation Review Platform

Nestora is a full-stack Django web application that helps users discover, review, and compare PG (Paying Guest) accommodations. Property owners can list PGs with images and details, while users can search, filter, and review listings.

The platform focuses on clean UI, multi-image galleries, owner dashboards, and smart filtering to deliver a production-ready PG discovery experience.

---

## 🚀 Features

### 👤 User Features
- Browse PG listings with rich UI cards
- Search by name, city, and area
- Advanced filters:
  - Price range
  - Availability
  - Tenant type (Family / Bachelor / Company)
- PG detail pages with image gallery
- Full-screen image modal view
- Ratings & reviews system
- User authentication (register/login)

### 🧑‍💼 Owner Features
- Owner registration mode
- Owner dashboard
- Create / Edit / Delete PG listings
- Upload multiple PG images
- Manage PG details and rent
- Add food availability & tenant preferences

### ⭐ Review System
- Star ratings
- Text reviews
- Average rating auto-calculation
- Auth-protected review submission

### 🎨 UI / UX Features
- Animated hero section
- Card-based PG layout
- Responsive grid design
- Modal image viewer
- Styled forms (login/register/PG form/review form)
- Sticky navbar + footer
- Professional filter bar

---

## 🛠 Tech Stack

**Backend**
- Django 6
- Python 3.12+
- SQLite (default, can switch to Postgres)

**Frontend**
- Django Templates
- Custom CSS
- JavaScript
- Responsive layout

**Media Handling**
- Django media storage
- Multi-image upload per PG

**Deployment**
- Render (recommended)
- Gunicorn
- WhiteNoise (for static files)
- Aiven