# Django E-Commerce: Backend & Frontend Overview

This project is a full-stack e-commerce application split into two main parts:

- **Backend:** Django REST API (`de_commerce/`)
- **Frontend:** Vue.js SPA (`de_commerce_front-end/`)

## Features

### Backend (Django)
- RESTful API with Django REST Framework
- User authentication and session management
- **Admin product management with bulk import (CSV/JSON)**
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
- **Admin Dashboard for product management**
