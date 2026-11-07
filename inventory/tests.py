from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Category, Supplier, WarehouseLocation, Product


class InventoryModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Industrial Equipment",
            description="Heavy machinery and tools"
        )
        self.supplier = Supplier.objects.create(
            name="Apex Tools Ltd",
            email="apex@test.com"
        )
        self.location = WarehouseLocation.objects.create(
            name="Main Depot",
            zone_or_aisle="Aisle 1"
        )

    def test_category_slug_generation(self):
        self.assertEqual(self.category.slug, "industrial-equipment")

    def test_product_auto_sku_generation(self):
        product = Product.objects.create(
            name="Pneumatic Drill",
            category=self.category,
            supplier=self.supplier,
            warehouse_location=self.location,
            unit_price=Decimal("150.00"),
            cost_price=Decimal("95.00"),
            quantity_on_hand=25,
            reorder_threshold=10,
        )
        self.assertTrue(product.sku.startswith("IND-"))
        self.assertEqual(product.stock_status, "in_stock")
        self.assertFalse(product.is_low_stock)
        self.assertFalse(product.is_out_of_stock)
        self.assertEqual(product.total_value, Decimal("3750.00"))

    def test_product_low_and_out_of_stock_properties(self):
        low_product = Product.objects.create(
            name="Replacement Seal",
            category=self.category,
            unit_price=Decimal("12.00"),
            quantity_on_hand=5,
            reorder_threshold=10,
        )
        self.assertTrue(low_product.is_low_stock)
        self.assertEqual(low_product.stock_status, "low_stock")

        out_product = Product.objects.create(
            name="Exhaust Gasket",
            category=self.category,
            unit_price=Decimal("8.00"),
            quantity_on_hand=0,
            reorder_threshold=15,
        )
        self.assertTrue(out_product.is_out_of_stock)
        self.assertEqual(out_product.stock_status, "out_of_stock")


class InventoryAuthAndAccessTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="supervisor",
            password="supervisor123",
            first_name="Project",
            last_name="Supervisor"
        )
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Multimeter Pro",
            category=self.category,
            unit_price=Decimal("50.00"),
            quantity_on_hand=15,
            reorder_threshold=5,
        )

    def test_public_landing_page_accessible_without_auth(self):
        response = self.client.get(reverse("inventory:landing"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Warehouse Inventory Management")
        self.assertContains(response, "with Demand Forecasting")

    def test_login_page_accessible_without_auth(self):
        response = self.client.get(reverse("inventory:login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Warehouse Portal Sign In")

    def test_dashboard_redirects_unauthenticated_user_to_login(self):
        response = self.client.get(reverse("inventory:dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("inventory:login"), response.url)

    def test_catalog_redirects_unauthenticated_user_to_login(self):
        response = self.client.get(reverse("inventory:product_list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("inventory:login"), response.url)

    def test_login_success_and_access_dashboard(self):
        login_success = self.client.login(username="supervisor", password="supervisor123")
        self.assertTrue(login_success)

        response = self.client.get(reverse("inventory:dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dashboard Overview")
        self.assertContains(response, "Multimeter Pro")

    def test_authenticated_product_list_and_search(self):
        self.client.login(username="supervisor", password="supervisor123")

        response = self.client.get(reverse("inventory:product_list"), {"q": "Multimeter"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Multimeter Pro")

        response = self.client.get(reverse("inventory:product_list"), {"q": "NonExistent"})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Multimeter Pro")

    def test_logout_redirects_to_landing(self):
        self.client.login(username="supervisor", password="supervisor123")
        response = self.client.get(reverse("inventory:logout"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("inventory:landing"))

    def test_category_creation_via_ui(self):
        self.client.login(username="supervisor", password="supervisor123")
        response = self.client.post(
            reverse("inventory:category_list"),
            {"name": "Heavy Chemicals", "description": "Solvents, degreasers, and lubricants"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Category.objects.filter(name="Heavy Chemicals").exists())

    def test_category_update_via_ui(self):
        self.client.login(username="supervisor", password="supervisor123")
        response = self.client.post(
            reverse("inventory:category_update", kwargs={"pk": self.category.pk}),
            {"name": "Electronics & Sensors", "description": "Updated description"}
        )
        self.assertEqual(response.status_code, 302)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, "Electronics & Sensors")

    def test_category_delete_success_when_empty(self):
        self.client.login(username="supervisor", password="supervisor123")
        empty_cat = Category.objects.create(name="Temporary Testing Category")
        response = self.client.post(reverse("inventory:category_delete", kwargs={"pk": empty_cat.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Category.objects.filter(name="Temporary Testing Category").exists())

    def test_category_delete_blocked_when_products_exist(self):
        self.client.login(username="supervisor", password="supervisor123")
        # self.category has self.product linked to it
        response = self.client.post(reverse("inventory:category_delete", kwargs={"pk": self.category.pk}))
        self.assertEqual(response.status_code, 302)
        # Verify category still exists
        self.assertTrue(Category.objects.filter(pk=self.category.pk).exists())
