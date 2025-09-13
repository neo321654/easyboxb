from django.db import models
from django.conf import settings

class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Warehouse(BaseModel):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Category(BaseModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Product(BaseModel):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, unique=True)
    barcode = models.CharField(max_length=100, unique=True, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    unit = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Stock(BaseModel):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        unique_together = ('warehouse', 'product')

    def __str__(self):
        return f'{self.product.name} at {self.warehouse.name}'

class Movement(BaseModel):
    class MovementType(models.TextChoices):
        INCOMING = 'incoming', 'Incoming'
        OUTGOING = 'outgoing', 'Outgoing'
        TRANSFER = 'transfer', 'Transfer'

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    movement_type = models.CharField(max_length=10, choices=MovementType.choices)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    reference = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.movement_type} of {self.quantity} {self.product.unit} of {self.product.name}'

class Inventory(BaseModel):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'

    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    started_at = models.DateTimeField()
    finished_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)

    def __str__(self):
        return f'Inventory at {self.warehouse.name} on {self.started_at.date()}'

class InventoryItem(BaseModel):
    inventory = models.ForeignKey(Inventory, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    counted_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    expected_quantity = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.product.name} in inventory {self.inventory.id}'