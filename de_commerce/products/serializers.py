"""
Serializers Module for API

This module contains DRF (Django Rest Framework) serializers that convert:
- Python model instances <-> JSON responses
- Request data <-> Python objects
- Validation logic

Serializers are used for:
1. User Registration/Login (custom serializers)
2. Product browsing (Category and Product serializers - public)
3. Cart management (authenticated only)
4. Order management (authenticated only)

All serializers support the API endpoints defined in api.py
"""

from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Category, Product, Cart, CartItem, Order, OrderItem
from django.contrib.auth.models import User

# ============================================================================
# AUTHENTICATION SERIALIZERS (NO LOGIN REQUIRED for registration/login)
# ============================================================================

class RegisterSerializer(serializers.ModelSerializer):
    # Serializer for user registration/sign-up
    # Fields: username, email, password1, password2
    # Validates passwords match and user doesn't already exist
    # API Endpoint: POST /api/register/ (NO LOGIN REQUIRED - AllowAny)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def validate(self, data):
        # Check passwords match and user doesn't already exist
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('Passwords do not match.')
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('Username already exists.')
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError('Email already exists.')
        return data

    def create(self, validated_data):
        # Create new User object with hashed password
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password1']
        )
        return user

class LoginSerializer(serializers.Serializer):
    # Serializer for user login authentication
    # Fields: username, password (validates structure only)
    # Actual authentication in LoginAPIView.post() using Django's authenticate()
    # API Endpoint: POST /api/login/ (NO LOGIN REQUIRED - AllowAny)
    username = serializers.CharField()
    password = serializers.CharField()

# ============================================================================
# PRODUCT BROWSING SERIALIZERS (NO LOGIN REQUIRED - Public Read)
# ============================================================================

class CategorySerializer(serializers.ModelSerializer):
    # Serializer for Category model
    # Fields: id, name, description
    # API Endpoint: GET /api/categories/ (NO LOGIN REQUIRED - AllowAny)
    # ViewSet: CategoryViewSet (read-only, uses ReadOnlyModelViewSet)
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class ProductSerializer(serializers.ModelSerializer):
    # Serializer for Product model
    # Fields: id, name, description, price, category (nested), image, more_description, specifications, stock_status
    # Key Feature: Nested 'category' field includes full category data
    # API Endpoints: GET /api/products/, GET /api/products/{id}/ (NO LOGIN - AllowAny)
    # ViewSet: ProductViewSet (read-only, uses ReadOnlyModelViewSet)
    # Frontend: ProductList.vue, ProductDetail.vue, ProductCard.vue
    category = CategorySerializer(read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'image', 'more_description', 'specifications', 'stock_status']

# ============================================================================
# CART SERIALIZERS (REQUIRES LOGIN - IsAuthenticated)
# ============================================================================

class CartItemSerializer(serializers.ModelSerializer):
    # Serializer for CartItem model - nested within CartSerializer
    # Fields: id, product (nested ProductSerializer), quantity
    # Key Feature: Nested 'product' shows full product details with each item
    # API Access: Only through /api/carts/ endpoint (REQUIRES LOGIN)
    # Frontend: Cart.vue displays each item with product details and quantity
    product = ProductSerializer(read_only=True)
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    # Serializer for Cart model
    # Fields: id, user, created_at, items (nested CartItemSerializer array)
    # Key Feature: Nested 'items' shows full product details for each cart item
    # API Endpoint: GET /api/carts/ (REQUIRES LOGIN - IsAuthenticated)
    # ViewSet: CartViewSet filters to current user only
    # Frontend: Cart.vue, Checkout.vue uses useCartStore for state management
    items = CartItemSerializer(many=True, read_only=True)
    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'items']

# ============================================================================
# ORDER SERIALIZERS (REQUIRES LOGIN - IsAuthenticated)
# ============================================================================

class OrderItemSerializer(serializers.ModelSerializer):
    # Serializer for OrderItem model - nested within OrderSerializer
    # Fields: id, product (nested ProductSerializer), quantity, price
    # Key Feature: Stores price at time of order (historical accuracy)
    # API Access: Only through /api/orders/ endpoint (REQUIRES LOGIN)
    # Frontend: OrderHistory.vue, OrderDetail.vue, Profile.vue display order items
    product = ProductSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    # Serializer for Order model
    # Fields: id, user, created_at, updated_at, shipping_address, phone_number
    #         payment_method, status, items (nested OrderItemSerializer array)
    # Key Feature: Nested 'items' shows full product details with prices at order time
    # API Endpoints (REQUIRES LOGIN - IsAuthenticated):
    #   - GET /api/orders/: List all orders for logged-in user
    #   - GET /api/orders/{id}/: Retrieve specific order details
    #   - POST /api/orders/: Create new order
    # ViewSet: OrderViewSet filters to current user only
    # Frontend: OrderHistory.vue, OrderDetail.vue, Profile.vue
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'updated_at', 'shipping_address', 'phone_number', 'payment_method', 'status', 'items']


class UserSerializer(serializers.ModelSerializer):
    """
    Minimal serializer for authenticated user profile data returned by /api/me/
    Includes is_superuser flag to indicate if user has admin privileges
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined', 'is_superuser']
