from django.contrib import admin
from .models import Warehouse, Product, Stock, StockMovement, Supplier


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'active', 'created_at']
    list_filter = ['active']
    search_fields = ['code', 'name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['sku', 'name', 'category', 'unit_cost', 'active']
    list_filter = ['active', 'category']
    search_fields = ['sku', 'name']


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['product', 'warehouse', 'quantity', 'updated_at']
    list_filter = ['warehouse']
    search_fields = ['product__sku', 'product__name']


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'movement_type', 'product', 'warehouse', 'quantity_change', 'user']
    list_filter = ['movement_type', 'warehouse', 'timestamp']
    search_fields = ['product__sku', 'reference']
    readonly_fields = ['timestamp', 'user']  # Immutable
    
    def save_model(self, request, obj, form, change):
        """Auto-populate user field with current user"""
        if not obj.pk:  # Only on creation
            obj.user = request.user
        super().save_model(request, obj, form, change)
    
    def has_change_permission(self, request, obj=None):
        # Prevent editing stock movements (immutable)
        return False


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'contact_name', 'email', 'phone', 'active']
    list_filter = ['active']
    search_fields = ['code', 'name', 'contact_name']
