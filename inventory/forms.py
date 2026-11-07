from django import forms
from .models import Product, Category, Supplier, WarehouseLocation


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Industrial Automation, Lubricants & Chemicals",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Brief description of the goods stored under this category",
                }
            ),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "category",
            "supplier",
            "warehouse_location",
            "unit",
            "cost_price",
            "unit_price",
            "quantity_on_hand",
            "reorder_threshold",
            "barcode",
            "description",
            "is_active",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Industrial Hydraulic Pump"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "supplier": forms.Select(attrs={"class": "form-control"}),
            "warehouse_location": forms.Select(attrs={"class": "form-control"}),
            "unit": forms.Select(attrs={"class": "form-control"}),
            "cost_price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "placeholder": "0.00"}),
            "unit_price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "placeholder": "0.00"}),
            "quantity_on_hand": forms.NumberInput(attrs={"class": "form-control", "min": "0"}),
            "reorder_threshold": forms.NumberInput(attrs={"class": "form-control", "min": "1"}),
            "barcode": forms.TextInput(attrs={"class": "form-control", "placeholder": "Optional barcode / EAN"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Product specifications, notes, or details"}),
            "is_active": forms.CheckboxInput(attrs={"style": "width: 18px; height: 18px;"}),
        }
