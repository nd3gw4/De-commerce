
from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'description')
	search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('name', 'category', 'price', 'admin_image')
	list_filter = ('category',)
	search_fields = ('name',)
	fields = (
		'name',
		'description',
		'price',
		'category',
		'image',
		'image1',
		'image2',
		'image3',
		'image4',
		'more_description',
		'specifications',
		'stock_status'
	)

	def admin_image(self, obj):
		if obj.image:
			return f'<img src="{obj.image.url}" style="max-height:50px;max-width:50px;" />'
		return ""
	admin_image.allow_tags = True
	admin_image.short_description = 'Image'

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
	list_display = ('user', 'created_at')
	search_fields = ('user__username',)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
	list_display = ('cart', 'product', 'quantity')
	search_fields = ('cart__user__username', 'product__name')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'created_at', 'status', 'payment_method')
	list_filter = ('status', 'payment_method')
	search_fields = ('user__username', 'id')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
	# Display product details and order quantity/price for each item
	# Note: OrderItems typically viewed through their parent Order
	list_display = ('product', 'quantity', 'price')
	search_fields = ('product__name',)
