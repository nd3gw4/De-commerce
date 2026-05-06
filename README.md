# Django E-Commerce: Backend & Frontend Overview

This project is a full-stack e-commerce application split into two main parts:

- **Backend:** Django REST API (`de_commerce/`)
- **Frontend:** Vue.js SPA (`de_commerce_front-end/`)

## Features

### Backend (Django)
- RESTful API with Django REST Framework
- User authentication and session management
- Product catalog with categories
- Shopping cart functionality
- Order management with status tracking
- CORS support for frontend integration
- SQLite database

### Frontend (Vue.js)
- Single Page Application with Vue Router
- Pinia for state management
- Bootstrap for styling
- Axios for API communication
- Authentication flow with protected routes
- Shopping cart with local storage persistence
- Order history and checkout process

## Quick Start

### Backend Setup
```bash
cd de_commerce
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend Setup
```bash
cd de_commerce_front-end
npm install
npm run dev
```

## API Endpoints

### Public Endpoints (No Authentication Required)
- `GET /api/categories/` - List all categories
- `GET /api/products/` - List all products
- `GET /api/products/{id}/` - Get product details
- `POST /api/register/` - User registration
- `POST /api/login/` - User login

### Protected Endpoints (Authentication Required)
- `GET /api/carts/` - Get user's cart
- `DELETE /api/carts/clear/` - Clear user's cart
- `GET /api/orders/` - List user's orders
- `GET /api/orders/{id}/` - Get order details
- `POST /api/create-order/` - Create new order from cart
- `POST /api/logout/` - Logout user

## Authentication

The application uses Django session-based authentication with CSRF protection. Frontend maintains authentication state in localStorage and sends session cookies with API requests.
