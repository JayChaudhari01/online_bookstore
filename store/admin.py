from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Category, Book, CartItem, Order, OrderItem

# User Model Admin
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'phone', 'first_name', 'last_name', 'is_staff']
    search_fields = ('username', 'first_name', 'last_name', 'email', 'phone')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    
    # UPDATED FIELDSETS - Add new profile fields
    fieldsets = UserAdmin.fieldsets + (
        ('Profile Information', {
            'fields': ('phone', 'address', 'city', 'state', 'pincode', 'age', 'profile_picture')
        }),
    )
    
    # For adding new user
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Profile Information', {
            'fields': ('phone', 'address', 'city', 'state', 'pincode', 'age', 'profile_picture')
        }),
    )


# Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

# Book Admin
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'price', 'category', 'isbn']
    list_filter = ['category', 'author']
    search_fields = ['title', 'author', 'isbn']

# CartItem Admin
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'quantity', 'total_price']
    list_filter = ['user']

# OrderItem Inline for Order
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['book', 'quantity', 'price']

# Order Admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'user', 'city', 'phone', 'payment_method', 'total', 'status', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at', 'city']
    search_fields = ['full_name', 'phone', 'address', 'user__username']
    list_editable = ['status']
    readonly_fields = ['created_at']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('user', 'full_name', 'phone')
        }),
        ('Shipping Address', {
            'fields': ('address', 'city', 'pincode')
        }),
        ('Order Details', {
            'fields': ('payment_method', 'total', 'status', 'created_at')
        }),
    )

# OrderItem Admin
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'book', 'quantity', 'price']
    list_filter = ['order__status']