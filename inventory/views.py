from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, F, Sum, ExpressionWrapper, DecimalField, ProtectedError
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import Product, Category, Supplier, WarehouseLocation
from .forms import ProductForm, CategoryForm


# ==============================================================================
# Public Views
# ==============================================================================

def landing_view(request):
    """
    Public Landing Page
    Showcases the project purpose, architecture, core features, and provides
    access points for the supervisor and administrators.
    """
    total_products_count = Product.objects.filter(is_active=True).count()
    categories_count = Category.objects.count()

    context = {
        "page_title": "Smart Warehouse Inventory & Demand Forecasting",
        "total_products_count": total_products_count,
        "categories_count": categories_count,
    }
    return render(request, "public/landing.html", context)


def login_view(request):
    """
    User Sign-In View
    Authenticates warehouse staff, managers, and project supervisors.
    """
    if request.user.is_authenticated:
        return redirect("inventory:dashboard")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            next_url = request.GET.get("next")
            if next_url:
                return redirect(next_url)
            return redirect("inventory:dashboard")
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = AuthenticationForm(request)

    context = {
        "form": form,
        "page_title": "Sign In — Warehouse Portal",
    }
    return render(request, "public/login.html", context)


def logout_view(request):
    """
    User Logout
    Logs out the user and redirects to the public landing page.
    """
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect("inventory:landing")


# ==============================================================================
# Protected Warehouse Operations (Authentication Required)
# ==============================================================================

@login_required
def dashboard_view(request):
    """
    Internal Warehouse Overview Dashboard
    Accessible only to authenticated users.
    Displays primary warehouse KPIs, inventory status counts, and critical low-stock alerts.
    """
    total_products = Product.objects.filter(is_active=True).count()
    out_of_stock_count = Product.objects.filter(is_active=True, quantity_on_hand=0).count()
    low_stock_count = Product.objects.filter(
        is_active=True,
        quantity_on_hand__gt=0,
        quantity_on_hand__lte=F("reorder_threshold")
    ).count()
    in_stock_count = Product.objects.filter(
        is_active=True,
        quantity_on_hand__gt=F("reorder_threshold")
    ).count()

    # Total inventory valuation: sum of (quantity_on_hand * unit_price)
    valuation_expr = ExpressionWrapper(
        F("quantity_on_hand") * F("unit_price"),
        output_field=DecimalField(max_digits=14, decimal_places=2)
    )
    total_valuation = Product.objects.filter(is_active=True).aggregate(
        total=Sum(valuation_expr)
    )["total"] or 0

    # Critical alert products (low stock or out of stock)
    alert_products = Product.objects.filter(
        is_active=True,
        quantity_on_hand__lte=F("reorder_threshold")
    ).select_related("category", "warehouse_location").order_by("quantity_on_hand")[:8]

    # Recent products
    recent_products = Product.objects.filter(is_active=True).select_related(
        "category", "warehouse_location"
    ).order_by("-created_at")[:6]

    context = {
        "total_products": total_products,
        "in_stock_count": in_stock_count,
        "low_stock_count": low_stock_count,
        "out_of_stock_count": out_of_stock_count,
        "total_valuation": total_valuation,
        "alert_products": alert_products,
        "recent_products": recent_products,
        "page_title": "Warehouse Overview",
    }
    return render(request, "inventory/dashboard.html", context)


@login_required
def product_list_view(request):
    """
    Product Catalog view with search and filter capabilities.
    """
    query = request.GET.get("q", "").strip()
    category_id = request.GET.get("category", "").strip()
    status_filter = request.GET.get("status", "").strip()

    products = Product.objects.filter(is_active=True).select_related(
        "category", "warehouse_location", "supplier"
    )

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(sku__icontains=query) |
            Q(barcode__icontains=query)
        )

    if category_id:
        products = products.filter(category_id=category_id)

    if status_filter == "out_of_stock":
        products = products.filter(quantity_on_hand=0)
    elif status_filter == "low_stock":
        products = products.filter(
            quantity_on_hand__gt=0,
            quantity_on_hand__lte=F("reorder_threshold")
        )
    elif status_filter == "in_stock":
        products = products.filter(quantity_on_hand__gt=F("reorder_threshold"))

    categories = Category.objects.all()

    context = {
        "products": products,
        "categories": categories,
        "selected_category": category_id,
        "selected_status": status_filter,
        "query": query,
        "total_results": products.count(),
        "page_title": "Product Catalog",
    }
    return render(request, "inventory/product_list.html", context)


@login_required
def product_detail_view(request, pk):
    """
    Detailed inspection of a specific product.
    """
    product = get_object_or_404(
        Product.objects.select_related("category", "supplier", "warehouse_location"),
        pk=pk
    )
    context = {
        "product": product,
        "page_title": f"Product: {product.name}",
    }
    return render(request, "inventory/product_detail.html", context)


@login_required
def product_create_view(request):
    """
    Create a new product record.
    """
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            messages.success(request, f"Product '{product.name}' was created successfully with SKU {product.sku}.")
            return redirect("inventory:product_detail", pk=product.pk)
    else:
        form = ProductForm()

    context = {
        "form": form,
        "form_title": "Add New Product",
        "page_title": "Create Product",
    }
    return render(request, "inventory/product_form.html", context)


@login_required
def product_update_view(request, pk):
    """
    Edit an existing product.
    """
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f"Product '{product.name}' was updated successfully.")
            return redirect("inventory:product_detail", pk=product.pk)
    else:
        form = ProductForm(instance=product)

    context = {
        "form": form,
        "product": product,
        "form_title": f"Edit Product: {product.name}",
        "page_title": "Edit Product",
    }
    return render(request, "inventory/product_form.html", context)


@login_required
def category_list_view(request):
    """
    View and manage inventory categories with inline creation.
    """
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f"Category '{category.name}' created successfully.")
            return redirect("inventory:category_list")
        else:
            messages.error(request, "Please check the form inputs and try again.")
    else:
        form = CategoryForm()

    categories = Category.objects.all().prefetch_related("products")
    context = {
        "categories": categories,
        "form": form,
        "page_title": "Product Categories",
    }
    return render(request, "inventory/category_list.html", context)


@login_required
def category_update_view(request, pk):
    """
    Edit an existing inventory category.
    """
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f"Category '{category.name}' was updated successfully.")
            return redirect("inventory:category_list")
    else:
        form = CategoryForm(instance=category)

    context = {
        "form": form,
        "category": category,
        "page_title": f"Edit Category: {category.name}",
    }
    return render(request, "inventory/category_form.html", context)


@login_required
def category_delete_view(request, pk):
    """
    Delete an inventory category with safety checks against orphaned products.
    """
    category = get_object_or_404(Category, pk=pk)
    product_count = category.products.count()

    if request.method == "POST":
        if product_count > 0:
            messages.error(
                request,
                f"Cannot delete '{category.name}' because it contains {product_count} product{'' if product_count == 1 else 's'}. "
                f"Please reassign or remove these products first."
            )
            return redirect("inventory:category_list")

        name = category.name
        try:
            category.delete()
            messages.success(request, f"Category '{name}' was deleted successfully.")
        except ProtectedError:
            messages.error(request, f"Category '{name}' is linked to protected records and cannot be deleted.")
        return redirect("inventory:category_list")

    context = {
        "category": category,
        "product_count": product_count,
        "page_title": f"Confirm Delete: {category.name}",
    }
    return render(request, "inventory/category_confirm_delete.html", context)
