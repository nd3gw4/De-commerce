# De-Commerce Frontend

Vue.js frontend for the Django E-Commerce application.

## Features

- Vue 3 with Composition API
- Vue Router for navigation
- Pinia for state management
- Bootstrap 5 for styling
- Axios for API communication
- Session-based authentication
- Shopping cart with local storage
- Responsive design

## Development

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Project Structure

- `src/views/` - Page components
- `src/components/` - Reusable components
- `src/store/` - Pinia stores for state management
- `src/services/` - API service functions
- `src/router/` - Vue Router configuration

## Authentication Flow

1. User registers/logs in via API
2. Session cookie set by backend
3. Frontend stores auth state in localStorage
4. Protected routes check authentication status
5. API requests include session cookies automatically
