from django.contrib import admin
from .models import (
    Warehouse, Category, Product, Stock, Movement, Inventory, InventoryItem
)

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'location')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'category', 'unit')
    list_filter = ('category',)
    search_fields = ('name', 'sku')

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('product', 'warehouse', 'quantity')
    list_filter = ('warehouse',)
    search_fields = ('product__name', 'warehouse__name')

@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
    list_display = ('product', 'warehouse', 'movement_type', 'quantity', 'created_by', 'created_at')
    list_filter = ('movement_type', 'warehouse')
    search_fields = ('product__name', 'reference')

class InventoryItemInline(admin.TabularInline):
    model = InventoryItem
    extra = 1

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('warehouse', 'started_at', 'finished_at', 'status')
    list_filter = ('status', 'warehouse')
    inlines = [InventoryItemInline]