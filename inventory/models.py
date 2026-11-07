import uuid
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=150)
    contact_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class WarehouseLocation(models.Model):
    name = models.CharField(max_length=100)
    zone_or_aisle = models.CharField(
        max_length=50,
        blank=True,
        help_text="e.g. Zone A, Aisle 3, Rack 2"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name", "zone_or_aisle"]

    def __str__(self):
        if self.zone_or_aisle:
            return f"{self.name} ({self.zone_or_aisle})"
        return self.name


class Product(models.Model):
    UNIT_CHOICES = [
        ("pcs", "Pieces (pcs)"),
        ("box", "Box"),
        ("carton", "Carton"),
        ("kg", "Kilograms (kg)"),
        ("liters", "Liters (L)"),
        ("pallets", "Pallets"),
    ]

    name = models.CharField(max_length=200)
    sku = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        help_text="Leave blank to auto-generate from category"
    )
    barcode = models.CharField(max_length=100, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products"
    )
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products"
    )
    warehouse_location = models.ForeignKey(
        WarehouseLocation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products"
    )
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default="pcs")
    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Standard selling price per unit"
    )
    cost_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
        help_text="Cost per unit for inventory valuation"
    )
    quantity_on_hand = models.PositiveIntegerField(
        default=0,
        help_text="Current physical stock in warehouse"
    )
    reorder_threshold = models.PositiveIntegerField(
        default=10,
        help_text="Minimum threshold before low-stock alert is triggered"
    )
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.sku:
            prefix = (self.category.name[:3].upper() if self.category else "PRD")
            code = uuid.uuid4().hex[:6].upper()
            self.sku = f"{prefix}-{code}"
        super().save(*args, **kwargs)

    @property
    def is_out_of_stock(self):
        return self.quantity_on_hand == 0

    @property
    def is_low_stock(self):
        return 0 < self.quantity_on_hand <= self.reorder_threshold

    @property
    def stock_status(self):
        if self.quantity_on_hand == 0:
            return "out_of_stock"
        if self.quantity_on_hand <= self.reorder_threshold:
            return "low_stock"
        return "in_stock"

    @property
    def total_value(self):
        return self.quantity_on_hand * self.unit_price

    def __str__(self):
        return f"{self.name} ({self.sku})"
