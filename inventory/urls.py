from django.urls import path
from . import views

app_name = "inventory"

urlpatterns = [
    # Public routes
    path("", views.landing_view, name="landing"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Authenticated operations
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("products/", views.product_list_view, name="product_list"),
    path("products/new/", views.product_create_view, name="product_create"),
    path("products/<int:pk>/", views.product_detail_view, name="product_detail"),
    path("products/<int:pk>/edit/", views.product_update_view, name="product_update"),

    # Category operations
    path("categories/", views.category_list_view, name="category_list"),
    path("categories/<int:pk>/edit/", views.category_update_view, name="category_update"),
    path("categories/<int:pk>/delete/", views.category_delete_view, name="category_delete"),
]
