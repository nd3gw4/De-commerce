"""
REST API ViewSets Module

This module defines ViewSet classes that handle API operations for:
1. Categories and Products (read-only, public access)
2. Shopping Carts (authenticated users only)
3. Orders (authenticated users only)

ViewSets provide automatic REST endpoints:
- {model}/: GET (list), POST (create)
- {model}/{id}/: GET (retrieve), PUT (update), PATCH (partial update), DELETE

Permission system:
- AllowAny: Anyone can access (visitors without login)
- IsAuthenticated: Only authenticated users can access (requires login)
- IsAuthenticatedOrReadOnly: Public read access, authenticated write access
"""

from rest_framework import viewsets, permissions, status
from .models import Category, Product, Cart, Order, OrderItem
from .serializers import CategorySerializer, ProductSerializer, CartSerializer, OrderSerializer
from django.core.mail import send_mail
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.db import transaction

# ============================================================================
# PUBLIC VIEWSETS (NO LOGIN REQUIRED - AllowAny)
# ============================================================================

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
	"""
	ViewSet for Category model - Read-Only endpoint
	
	Endpoints:
	- GET /api/categories/: List all categories
	- GET /api/categories/{id}/: Retrieve single category details
	
	Allowed Methods: GET only (read-only)
	- No POST, PUT, PATCH, DELETE (cannot create/edit categories from API)
	
	Permission: AllowAny (no login required)
	- Unauthenticated users can browse categories
	- Used for category filtering in ProductList.vue dropdown
	
	Serializer: CategorySerializer
	- Returns: id, name, description
	
	QuerySet: All Category objects
	- No filtering, all categories visible to all users
	
	Frontend Usage:
	- ProductList.vue: Fetches categories for filter dropdown
	- Uses fetchCategories() from products.js service
	"""
	queryset = Category.objects.all()
	serializer_class = CategorySerializer
	permission_classes = [permissions.AllowAny]

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
	"""
	ViewSet for Product model - Read-Only endpoint
	
	Endpoints:
	- GET /api/products/: List all products (paginated if configured)
	- GET /api/products/{id}/: Retrieve single product details
	
	Allowed Methods: GET only (read-only)
	- No POST, PUT, PATCH, DELETE (cannot manage products from API)
	
	Permission: AllowAny (no login required)
	- Unauthenticated visitors can browse all products
	- Important: Product listing is publicly accessible
	- Authenticated users can add products to cart (on ProductDetail)
	
	Serializer: ProductSerializer
	- Returns: id, name, description, price, category (nested), image
	- Category field is nested (full object, not just ID)
	
	QuerySet: All Product objects
	- No filtering, all products visible to all users
	- Includes related category data
	
	Frontend Usage:
	- ProductList.vue: Fetches all products for grid display
	- ProductDetail.vue: Fetches single product by ID
	- ProductCard.vue: Displays product data
	- Uses fetchProducts() and fetchProduct() from products.js service
	"""
	queryset = Product.objects.all()
	serializer_class = ProductSerializer
	permission_classes = [permissions.AllowAny]

# ============================================================================
# PROTECTED VIEWSETS (REQUIRES LOGIN - IsAuthenticated)
# ============================================================================

class CartViewSet(viewsets.ModelViewSet):
	"""
	ViewSet for Cart model - Full CRUD operations (for authenticated users only)
	
	Endpoints:
	- GET /api/carts/: List all carts (user sees only their own cart)
	- POST /api/carts/: Create/add items to cart
	- GET /api/carts/{id}/: Retrieve specific cart
	- PUT /api/carts/{id}/: Update entire cart
	- PATCH /api/carts/{id}/: Partially update cart
	- DELETE /api/carts/{id}/: Delete cart
	- DELETE /api/carts/clear/: Custom action to clear all items
	
	Permission: IsAuthenticated (LOGIN REQUIRED)
	- Only logged-in users can access any cart operations
	- Unauthenticated users get 401 Unauthorized response
	
	Serializer: CartSerializer
	- Returns: id, user, created_at, items (nested CartItem objects)
	
	Key Security Feature - get_queryset() method:
	- CRITICAL FOR SECURITY: Filters Cart.objects.filter(user=self.request.user)
	- Users can ONLY see and modify their own cart
	- Even if user tries to access another user's cart ID, filtered out
	- Prevents unauthorized access to other users' shopping carts
	
	Frontend Usage:
	- Cart.vue: Fetches user's cart to display items
	- Checkout.vue: Shows cart summary before placing order
	- AddToCart button on ProductDetail.vue adds to cart
	
	Workflow:
	1. User adds product to cart (ProductDetail.vue handleAddCart)
	2. Frontend cart store updated locally via useCartStore.add()
	3. When user checks out, order is created from cart items
	4. Cart persists across sessions (localStorage on frontend)
	
	Notes:
	- Cart is one-to-one per user (defined in Cart model)
	- CartItems accessed through nested 'items' field
	- Uses select_related('product') for efficient database queries
	"""
	serializer_class = CartSerializer
	permission_classes = [permissions.IsAuthenticated]
	
	def get_queryset(self):
		"""
		SECURITY-CRITICAL METHOD: Filters cart items to current user only
		
		Returns only the authenticated user's own cart items.
		This prevents users from accessing or modifying other users' carts.
		"""
		return Cart.objects.filter(user=self.request.user).select_related('product')
	
	@action(detail=False, methods=['delete'])
	def clear(self, request):
		"""
		Clear all items from the user's cart
		
		DELETE /api/carts/clear/
		
		Returns: {"message": "Cart cleared successfully"}
		"""
		cart_items = Cart.objects.filter(user=request.user)
		cart_items.delete()
		return Response({"message": "Cart cleared successfully"})

	def get_queryset(self):
		"""
		SECURITY-CRITICAL METHOD: Filters cart to current user only
		
		Returns only the authenticated user's own cart objects.
		This ensures users cannot access other users' shopping carts
		even if they know the cart ID.
		"""
		return Cart.objects.filter(user=self.request.user)

class OrderViewSet(viewsets.ReadOnlyModelViewSet):
	"""
	ViewSet for Order model - Read-Only operations for customers
	
	Endpoints:
	- GET /api/orders/: List all orders (user sees only their own orders)
	- GET /api/orders/{id}/: Retrieve specific order details
	
	RESTRICTED METHODS: No POST, PUT, PATCH, DELETE for customers
	- Orders can only be created via checkout process
	- Order status updates should be admin-only
	- Prevents customers from modifying their order history
	
	Permission: IsAuthenticated (LOGIN REQUIRED)
	- Only logged-in users can view orders
	- Unauthenticated users get 401 Unauthorized response
	
	Serializer: OrderSerializer
	- Returns: id, user, created_at, updated_at, shipping_address, phone_number, 
	           payment_method, status, items (nested OrderItem objects)
	
	Key Security Feature - get_queryset() method:
	- Filters Order.objects.filter(user=self.request.user)
	- Users can ONLY see their own orders
	- Prevents unauthorized access to other users' order information
	
	Frontend Usage:
	- OrderHistory.vue: Fetches all user orders for display list
	- OrderDetail.vue: Fetches single order details by ID
	- Profile.vue: Shows user's orders in profile section
	
	Order Workflow:
	1. User adds products to cart (ProductDetail.vue)
	2. User clicks checkout and proceeds to Checkout.vue
	3. Order created via custom checkout endpoint (not this ViewSet)
	4. Order automatically assigned to authenticated user
	5. Order status starts as 'ordered'
	6. User can view order history anytime via OrderHistory.vue
	
	Order Status Progression:
	- 'ordered': Just created, not yet processed
	- 'pending': Awaiting shipment
	- 'shipped': Order sent to customer
	- 'delivered': Order received by customer
	- 'cancelled': Order was cancelled
	
	Notes:
	- OrderItems accessed through nested 'items' field
	- Stores product snapshot + price at time of order (not current price)
	- Payment method and shipping address captured at order time
	"""
	serializer_class = OrderSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		"""
		SECURITY-CRITICAL METHOD: Filters orders to current user only
		
		Returns only the authenticated user's own order objects.
		This protects sensitive order information from unauthorized access.
		"""
		return Order.objects.filter(user=self.request.user).prefetch_related('items__product')

	def create(self, request, *args, **kwargs):
		"""
		Custom create method for order placement
		
		Creates an order from the user's current cart items.
		Process:
		1. Get user's cart and cart items
		2. Validate cart is not empty
		3. Create Order with provided data
		4. Create OrderItem records for each cart item (with current prices)
		5. Clear the cart
		6. Return the created order
		
		Expected request data:
		- shipping_address: string
		- phone_number: string  
		- payment_method: 'Credit Card' or 'PayPal'
		"""
		user = request.user
		
		# Get user's cart
		try:
			cart = Cart.objects.get(user=user)
			cart_items = cart.items.select_related('product').all()
		except Cart.DoesNotExist:
			return Response(
				{'error': 'No cart found. Add items to cart before checkout.'}, 
				status=status.HTTP_400_BAD_REQUEST
			)
		
		if not cart_items:
			return Response(
				{'error': 'Cart is empty. Add items before checkout.'}, 
				status=status.HTTP_400_BAD_REQUEST
			)
		
		# Create the order atomically and validate stock
		order_data = request.data.copy()
		order_data['user'] = user.id
		order_data['status'] = 'ordered'  # Default status

		with transaction.atomic():
			# basic stock/status check: prevent ordering products marked 'Out of Stock'
			for cart_item in cart_items:
				if getattr(cart_item.product, 'stock_status', '').lower() == 'out of stock':
					return Response({'error': f"Product {cart_item.product.name} is out of stock."}, status=status.HTTP_400_BAD_REQUEST)

			serializer = self.get_serializer(data=order_data)
			serializer.is_valid(raise_exception=True)
			order = serializer.save()

			# Create order items from cart items
			order_items = []
			for cart_item in cart_items:
				order_item = OrderItem.objects.create(
					order=order,
					product=cart_item.product,
					quantity=cart_item.quantity,
					price=cart_item.product.price  # Store current price at time of order
				)
				order_items.append(order_item)

			# Clear the cart
			cart_items.delete()

			# Return the order with items populated
			order_serializer = self.get_serializer(order)
			return Response(order_serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def create_order(request):
	"""
	API View for order creation (checkout process)
	
	Endpoint: POST /api/create-order/
	
	Permission: IsAuthenticated (LOGIN REQUIRED)
	
	HTTP Methods:
	- POST: Create new order from user's cart
	  - Request body: {shipping_address, phone_number, payment_method}
	  - Creates Order and OrderItem records from cart
	  - Clears cart after successful order creation
	  - Returns: Created order with all details
	
	Status Codes:
	- 201 Created: Order successfully created
	- 400 Bad Request: Invalid data or empty cart
	- 401 Unauthorized: User not authenticated
	
	Frontend Integration:
	- Called from Checkout.vue submitOrder() function
	- Uses createOrder() service function from order.js
	- On success, redirects to order history page
	- On error, displays error message to user
	
	Security:
	- User can only create orders from their own cart
	- Order automatically assigned to authenticated user
	- Cart cleared only after successful order creation
	"""
	if not request.user.is_authenticated:
		return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
	
	user = request.user
	
	# Get user's cart
	try:
		cart = Cart.objects.get(user=user)
		cart_items = cart.items.select_related('product').all()
	except Cart.DoesNotExist:
		return Response(
			{'error': 'No cart found. Add items to cart before checkout.'}, 
			status=status.HTTP_400_BAD_REQUEST
		)
	
	if not cart_items:
		return Response(
			{'error': 'Cart is empty. Add items before checkout.'}, 
			status=status.HTTP_400_BAD_REQUEST
		)
	
	# Create the order
	order_data = request.data.copy()
	order_data['user'] = user.id
	order_data['status'] = 'ordered'  # Default status
	
	serializer = OrderSerializer(data=order_data)
	if serializer.is_valid():
		with transaction.atomic():
			for cart_item in cart_items:
				if getattr(cart_item.product, 'stock_status', '').lower() == 'out of stock':
					return Response({'error': f"Product {cart_item.product.name} is out of stock."}, status=status.HTTP_400_BAD_REQUEST)

			order = serializer.save()

			# Create order items from cart items
			order_items = []
			for cart_item in cart_items:
				order_item = OrderItem.objects.create(
					order=order,
					product=cart_item.product,
					quantity=cart_item.quantity,
					price=cart_item.product.price  # Store current price at time of order
				)
				order_items.append(order_item)

			# Clear the cart
			cart_items.delete()

			# Return the order with items populated
			order_serializer = OrderSerializer(order)
			return Response(order_serializer.data, status=status.HTTP_201_CREATED)

	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout_view(request):
	"""
	API View for user logout
	
	Endpoint: POST /api/logout/
	
	Permission: IsAuthenticated (but logout should work even if session expired)
	
	HTTP Methods:
	- POST: Destroy user's session
	  - No request body required
	  - Calls Django's logout() to clear session
	  - Returns: Success message
	
	Status Codes:
	- 200 OK: Logout successful
	- 401 Unauthorized: User not authenticated (but still clears any existing session)
	
	Frontend Integration:
	- Called from Navbar.vue logout() function
	- Uses logoutUser() service function from auth.js
	- Frontend also clears local auth state
	- Redirects to login page
	
	Security:
	- Always returns success to prevent user enumeration
	- Session cookie invalidated on server side
	- Frontend handles localStorage cleanup
	"""
	from django.contrib.auth import logout
	logout(request)
	return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def password_reset(request):
    email = request.data.get('email')
    if not email:
        return Response({'error': 'Email is required'}, status=400)

    # Simulate sending a password reset email
    send_mail(
        'Password Reset Request',
        'Click the link below to reset your password.',
        'noreply@de-commerce.com',
        [email],
        fail_silently=False,
    )

    return Response({'message': 'Password reset link sent'})

@api_view(['POST'])
def contact_form(request):
    name = request.data.get('name')
    email = request.data.get('email')
    message = request.data.get('message')

    if not all([name, email, message]):
        return Response({'error': 'All fields are required'}, status=400)

    # Simulate saving the message or sending an email
    send_mail(
        f'New Contact Form Submission from {name}',
        message,
        email,
        ['support@de-commerce.com'],
        fail_silently=False,
    )

    return Response({'message': 'Your message has been sent successfully'})
