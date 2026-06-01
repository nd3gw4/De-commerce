"""
Product Models Module

This module defines database models for the e-commerce application including:
- Category: Product categories for organization
- Product: Individual products for sale
- Cart: Shopping cart per user (one-to-one relationship)
- CartItem: Individual items in a cart
- Order: Customer orders with status tracking
- OrderItem: Individual items in an order

All models use Django ORM and are used by Django Rest Framework serializers
to create API endpoints for both authenticated and unauthenticated users.
"""

from django.db import models
from django.conf import settings


class Category(models.Model):
    """
    Category Model: Represents product categories
    
    Fields:
    - name: Unique category name (max 100 chars)
    - description: Optional category description (TextField)
    
    Methods:
    - __str__: Returns the category name for admin display and string representation
    
    Usage: Categories are used to organize products. Retrieved via GET /api/categories/
    which is accessible without authentication (AllowAny permission).
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name



class Product(models.Model):
    """
    Product Model: Represents individual products available for purchase
    
    Fields:
    - name: Product name (max 255 chars)
    - description: Detailed product description (TextField)
    - price: Product price as decimal (max 10 digits, 2 decimal places)
    - category: ForeignKey reference to Category model (creates many-to-one relationship)
    - image: Optional image file uploaded to 'product_images/' directory
    
    Methods:
    - __str__: Returns the product name for admin display
    - get_price(): Returns the product's current price (float)
    - get_category(): Returns the assigned Category object for this product
    
    API Access:
    - GET /api/products/: List all products (NO LOGIN required - AllowAny)
    - GET /api/products/{id}/: Retrieve single product details (NO LOGIN required - AllowAny)
    
    Usage: Products are displayed on the frontend ProductList and ProductDetail views.
    Unauthenticated users can browse products; authenticated users can add them to cart.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    image1 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    image2 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    image4 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    more_description = models.TextField(blank=True, help_text="Additional detailed description for the product")
    specifications = models.TextField(blank=True, help_text="Product specifications and technical details")
    stock_status = models.CharField(max_length=100, blank=True, help_text="Current stock availability status (e.g., 'In Stock', 'Out of Stock', 'Limited Stock')")

    def __str__(self):
        return self.name

    def get_price(self):
        """Return the price of the product."""
        return self.price

    def get_category(self):
        """Return the category of the product."""
        return self.category



class Cart(models.Model):
    """
    Cart Model: Represents a shopping cart (one per authenticated user)
    
    Fields:
    - user: OneToOneField to Django User model (each user has exactly one cart)
    - created_at: Timestamp when the cart was created (auto_now_add=True, set once)
    
    Related Items:
    - items: Reverse relation to CartItem via ForeignKey (access via cart.items.all())
    
    Methods:
    - __str__: Returns cart owner's username
    - total_items(): Calculates sum of all item quantities in the cart (int)
    - total_price(): Calculates total monetary value of all items in cart (Decimal)
    
    API Access (REQUIRES LOGIN - IsAuthenticated):
    - GET /api/carts/: Retrieve current user's cart only (filtered by user in viewset)
    - POST /api/carts/: Create or add items to cart (user auto-set to current user)
    - DELETE /api/carts/clear/: Clear all items from user's cart
    
    Note: Carts are user-specific via permissions in CartViewSet.get_queryset()
    which filters: Cart.objects.filter(user=self.request.user)
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

    def total_items(self):
        """Return the total number of items in the cart."""
        return sum(item.quantity for item in self.items.all())

    def total_price(self):
        """Return the total price of all items in the cart."""
        return sum(item.product.price * item.quantity for item in self.items.select_related('product').all())


class CartItem(models.Model):
    """
    CartItem Model: Represents individual items in a shopping cart
    
    Fields:
    - cart: ForeignKey to Cart (many-to-one, allows multiple items per cart)
    - product: ForeignKey to Product (the product being added)
    - quantity: Positive integer representing how many units of this product (default=1)
    
    Methods:
    - __str__: Returns formatted string "X x ProductName"
    - get_total_price(): Calculates line total for this item (product.price * quantity)
    
    API Access (REQUIRES LOGIN - IsAuthenticated):
    - Items accessed through /api/carts/ endpoint
    - CartItemSerializer displays as nested 'items' array in Cart response
    
    Usage Flow:
    1. User adds product to cart on ProductDetail.vue (toggleCart function)
    2. Frontend cart store updates locally via useCartStore.add()
    3. CartItem objects created/updated when checkout processes the cart
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_total_price(self):
        """Return the total price for this cart item."""
        return self.product.price * self.quantity


class Order(models.Model):
    """
    Order Model: Represents customer orders with full details and status tracking
    
    STATUS_CHOICES:
    - 'pending': Order created but not processed
    - 'shipped': Order has been shipped to customer
    - 'delivered': Order has arrived at customer
    - 'cancelled': Order was cancelled
    
    Fields:
    - status: Choice field selecting from STATUS_CHOICES (default='pending')
    - user: ForeignKey to User who placed the order
    - created_at: Timestamp when order was created (auto_now_add=True)
    - updated_at: Timestamp of last status update (auto_now=True)
    - shipping_address: Text field for delivery address
    - phone_number: Contact phone number (max 15 chars)
    - payment_method: Choice field for payment type (Credit Card or PayPal)
    
    Related Items:
    - items: Reverse relation to OrderItem via ForeignKey
    
    Methods:
    - __str__: Returns formatted string "Order {id} by {username}"
    - total_items(): Calculates total quantity of items ordered (int)
    - total_price(): Calculates total order amount (Decimal)
    
    API Access (REQUIRES LOGIN - IsAuthenticated):
    - GET /api/orders/: List all orders for authenticated user only (filtered in viewset)
    - GET /api/orders/{id}/: Retrieve order details (user can only see own orders)
    - POST /api/orders/: Create new order (user auto-set to current user)
    
    Note: Used in Orderserialize for API responses, frontend shows via OrderHistory.vue
    """
    STATUS_CHOICES = [
        ('ordered', 'Ordered'),
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ordered',
        help_text='Order status',
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    shipping_address = models.TextField(default='Default Address')  # Default value for existing rows
    phone_number = models.CharField(max_length=15)  # New field for phone number
    payment_method = models.CharField(
        max_length=50,
        choices=[('Credit Card', 'Credit Card'), ('PayPal', 'PayPal')],
        default='Credit Card'  # Default value for existing rows
    )  # New field for payment method

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

    def total_items(self):
        """Return the total number of items in the order."""
        return sum(item.quantity for item in self.items.all())

    def total_price(self):
        """Return the total price of the order."""
        return sum(item.price * item.quantity for item in self.items.all())

class OrderItem(models.Model):
    """
    OrderItem Model: Represents individual items within an order
    
    This model captures the product details at the time of purchase, keeping historical
    data even if product prices change later. Price is stored at order time, not from Product model.
    
    Fields:
    - order: ForeignKey to Order (many-to-one, allows multiple items per order)
    - product: ForeignKey to Product (stores which product was ordered)
    - quantity: Positive integer of units ordered
    - price: Decimal field storing the PRICE AT TIME OF ORDER (crucial for historical accuracy)
    
    Methods:
    - __str__: Returns formatted string "{quantity} x {product_name} (Order {order_id})"
    - get_total_price(): Calculates line total (price * quantity), uses stored price not current price
    
    Important Note:
    The 'price' field stores the product price AT THE TIME THE ORDER WAS PLACED.
    This ensures that even if product prices change in the future, the order shows
    what the customer actually paid (not current product price).
    
    API Access (REQUIRES LOGIN - IsAuthenticated):
    - Items accessed through /api/orders/ endpoint
    - OrderItemSerializer displays as nested 'items' array in Order response
    - Users can only see items from their own orders (filtered by OrderViewSet)
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # price at time of order


    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order {self.order.id})"

    def get_total_price(self):
        """Return the total price for this order item."""
        return self.price * self.quantity

