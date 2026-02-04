from django.contrib import admin
from .models import Category, Supplier, Product, StockMovement

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name',)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'email')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'sku',
        'category',
        'supplier',
        'stock',
        'min_stock',
        'is_active',
    )
    list_filter = ('category', 'supplier', 'is_active')
    search_fields = ('name', 'sku')
    list_editable = ('stock', 'min_stock')


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'movement_type',
        'quantity',
        'created_at',
        'created_by',
    )
    list_filter = ('movement_type', 'created_at')
    search_fields = ('product__name',)
