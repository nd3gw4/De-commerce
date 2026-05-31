"""
URL Configuration for Products App API Endpoints

This module maps URL patterns to ViewSets and Views.
All endpoints are prefixed with the path from main urls.py (no prefix in this case).

URL Patterns Registered:
1. Authentication endpoints (register, login)
2. Product browsing endpoints (categories, products)
3. Cart management endpoints (requires login)
4. Order management endpoints (requires login)

DefaultRouter automatically generates:
- /model/: GET all, POST create
- /model/{id}/: GET detail, PUT update, DELETE destroy
- All list/detail combinations

ViewSet vs APIView:
- ViewSet: Used for model CRUD operations (auto-generates multiple routes)
- APIView: Used for custom endpoints like register/login
"""

from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from rest_framework.routers import DefaultRouter
from .api import CategoryViewSet, ProductViewSet, CartViewSet, OrderViewSet, create_order, logout_view, AdminProductImportViewSet


app_name = 'products'

# DefaultRouter automatically generates REST endpoints from ViewSets
router = DefaultRouter()

# Public endpoints (NO LOGIN REQUIRED)
# CategoryViewSet: GET /api/categories/ and GET /api/categories/{id}/ (AllowAny - no login needed)
router.register(r'api/categories', CategoryViewSet, basename='category')

# ProductViewSet: GET /api/products/ and GET /api/products/{id}/ (AllowAny - no login needed)
router.register(r'api/products', ProductViewSet, basename='product')

# Protected endpoints (REQUIRES LOGIN)
# CartViewSet: GET/POST /api/carts/, DELETE /api/carts/clear/ (IsAuthenticated - filtered to current user)
router.register(r'api/carts', CartViewSet, basename='cart')

# OrderViewSet: GET/POST /api/orders/ (IsAuthenticated - filtered to current user only)
router.register(r'api/orders', OrderViewSet, basename='order')

# Admin-only endpoints (REQUIRES SUPERUSER/STAFF)
# AdminProductImportViewSet: POST /api/admin/import-products/ (IsAdminUser)
router.register(r'api/admin', AdminProductImportViewSet, basename='admin')

urlpatterns = [
    # POST /api/register/ - Register new user account (AllowAny - no login required)
    path('api/register/', views.RegisterAPIView.as_view(), name='api-register'),
    
    # POST /api/login/ - Authenticate user and create session (AllowAny - no login required)
    path('api/login/', views.LoginAPIView.as_view(), name='api-login'),
    
    # POST /api/password-reset/ - Password reset request (AllowAny - no login required)
    path('api/password-reset/', views.PasswordResetAPIView.as_view(), name='api-password-reset'),
    
    # POST /api/logout/ - Logout user and destroy session (IsAuthenticated)
    path('api/logout/', logout_view, name='api-logout'),

    # GET /api/me/ - Return authenticated user profile + canonical cart (or session cart if anonymous)
    path('api/me/', views.MeAPIView.as_view(), name='api-me'),
    
    # Auto-generated routes from DefaultRouter (categories, products, carts, orders)
    path('', include(router.urls)),
    
    # DRF login/logout views (optional, for browser API testing)
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
