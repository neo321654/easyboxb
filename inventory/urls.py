from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    WarehouseViewSet, CategoryViewSet, ProductViewSet, StockViewSet,
    MovementViewSet, InventoryViewSet, InventoryItemViewSet
)

router = DefaultRouter()
router.register(r'warehouses', WarehouseViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'stocks', StockViewSet)
router.register(r'movements', MovementViewSet)
router.register(r'inventories', InventoryViewSet)
router.register(r'inventory-items', InventoryItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
