from rest_framework import viewsets, permissions
from django.db import transaction
from .models import (
    Warehouse, Category, Product, Stock, Movement, Inventory, InventoryItem
)
from .serializers import (
    WarehouseSerializer, CategorySerializer, ProductSerializer, StockSerializer,
    MovementSerializer, InventorySerializer, InventoryItemSerializer
)
from users.models import User

# Permissions
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == User.Role.ADMIN

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == User.Role.MANAGER

class IsWorker(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == User.Role.WORKER

# ViewSets
class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin | IsManager]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin | IsManager]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin | IsManager]

class StockViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [permissions.IsAuthenticated]

class MovementViewSet(viewsets.ModelViewSet):
    queryset = Movement.objects.all()
    serializer_class = MovementSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsAdmin() | IsManager() | IsWorker()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        movement = serializer.save(created_by=self.request.user)
        self.update_stock(movement)

    def update_stock(self, movement):
        with transaction.atomic():
            stock, created = Stock.objects.get_or_create(
                warehouse=movement.warehouse,
                product=movement.product
            )
            if movement.movement_type == Movement.MovementType.INCOMING:
                stock.quantity += movement.quantity
            elif movement.movement_type == Movement.MovementType.OUTGOING:
                stock.quantity -= movement.quantity
            stock.save()

class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin | IsManager]

    def perform_update(self, serializer):
        inventory = serializer.save()
        if inventory.status == Inventory.Status.COMPLETED:
            self.update_stock_from_inventory(inventory)

    def update_stock_from_inventory(self, inventory):
        with transaction.atomic():
            for item in inventory.items.all():
                stock, created = Stock.objects.get_or_create(
                    warehouse=inventory.warehouse,
                    product=item.product
                )
                stock.quantity = item.counted_quantity
                stock.save()

class InventoryItemViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin | IsManager]