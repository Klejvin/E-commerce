# 🛒 ProScale E-commerce – Advanced Full-Stack Platform

ProScale is a high-performance, feature-rich e-commerce solution built with **Python** and **Django**. This platform is designed to handle the entire customer journey—from product discovery and search to cart management and automated order confirmations. It features a robust backend architecture and a modern, responsive frontend.

## 🌟 Comprehensive Features

### 🏢 Product & Inventory Management
- **Dynamic Catalog:** Multi-category support with a real-time search engine for products.
- **Image Processing:** Automated thumbnail generation and optimized image rendering using `Pillow`.
- **Relational Database:** Structured data models linking products, categories, and user interactions.

### 🛍️ Shopping Experience
- **Session-Based Cart:** A sophisticated shopping cart system that tracks items using Django sessions, allowing both guests and logged-in users to shop seamlessly.
- **Wishlist Functionality:** Users can curate personal lists of favorite items for future purchase.
- **Context Processors:** Global availability of categories and cart counts across all pages for a smooth UX.

### 🔐 User Security & Communication
- **Full Auth Suite:** Secure registration, login, and profile management with Django’s built-in security protocols.
- **Automated Workflow:** Integration with SMTP servers to send automatic welcome emails and order confirmation receipts.
- **Secure Password Reset:** Token-based "Forgot Password" system for safe account recovery.

### 📱 Modern Frontend & UI/UX
- **Mobile-First Design:** Fully responsive interface built with **Bootstrap 5** and custom CSS, ensuring a perfect look on smartphones and desktops.
- **Interactive Elements:** JavaScript-driven UI components for a dynamic feel without unnecessary page reloads.

## 🛠️ Technical Stack

- **Framework:** Django
- **Language:** Python .
- **Frontend:** HTML5, CSS3, JavaScript (ES6), Bootstrap 5.
- **Database:** PostgreSQL (Production) / SQLite (Development).
- **Environment:** VS Code, Git, Virtualenv.

## 📂 Project Architecture

```text
├── core/                # Project settings and WSGI/ASGI config
├── products/            # Models for Products, Categories, and Slugs
├── cart/                # Complex logic for Cart sessions and calculations
├── users/               # Authentication, Profiles, and Email logic
├── templates/           # Organized HTML structure (Base, Navbar, Footer)
├── static/              # Custom CSS, JS, and brand assets
└── media/               # User-uploaded product images
