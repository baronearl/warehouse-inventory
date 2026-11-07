from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Supplier, WarehouseLocation, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "product_count", "created_at")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = "Products"


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("name", "contact_name", "email", "phone", "product_count")
    search_fields = ("name", "contact_name", "email", "phone")

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = "Supplied Products"


@admin.register(WarehouseLocation)
class WarehouseLocationAdmin(admin.ModelAdmin):
    list_display = ("name", "zone_or_aisle", "is_active", "product_count")
    list_filter = ("is_active",)
    search_fields = ("name", "zone_or_aisle")

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = "Stored Products"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "sku",
        "category",
        "warehouse_location",
        "quantity_on_hand",
        "unit",
        "unit_price",
        "stock_badge",
        "is_active",
    )
    list_filter = ("category", "warehouse_location", "unit", "is_active")
    search_fields = ("name", "sku", "barcode", "description")
    readonly_fields = ("sku", "created_at", "updated_at")
    fieldsets = (
        ("Basic Information", {
            "fields": ("name", "sku", "barcode", "description", "category", "is_active")
        }),
        ("Warehouse & Supplier", {
            "fields": ("warehouse_location", "supplier")
        }),
        ("Stock & Pricing", {
            "fields": ("quantity_on_hand", "reorder_threshold", "unit", "cost_price", "unit_price")
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

    def stock_badge(self, obj):
        status = obj.stock_status
        if status == "out_of_stock":
            color = "#ef4444"
            bg = "#fee2e2"
            label = "Out of Stock"
        elif status == "low_stock":
            color = "#f59e0b"
            bg = "#fef3c7"
            label = f"Low Stock ({obj.quantity_on_hand})"
        else:
            color = "#10b981"
            bg = "#d1fae5"
            label = "In Stock"
        return format_html(
            '<span style="background-color: {}; color: {}; padding: 3px 8px; border-radius: 9999px; font-size: 11px; font-weight: 600;">{}</span>',
            bg, color, label
        )
    stock_badge.short_description = "Status"
