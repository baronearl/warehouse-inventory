from django.core.management.base import BaseCommand
from inventory.models import Category, Supplier, WarehouseLocation, Product
from decimal import Decimal


class Command(BaseCommand):
    help = "Seed database with realistic initial warehouse inventory data for demonstration"

    def handle(self, *args, **options):
        self.stdout.write("Seeding inventory data...")

        # 1. Categories
        categories_data = [
            ("Electronics & Hardware", "Computer components, sensors, cables, and electronic modules"),
            ("Industrial Equipment", "Pumps, motors, valves, and heavy-duty machinery parts"),
            ("Safety & PPE", "Personal protective equipment, helmets, gloves, and safety vests"),
            ("Packaging Materials", "Cardboard boxes, bubble wraps, pallets, and packing tape"),
            ("Automotive Spare Parts", "Filters, brake pads, fluids, spark plugs, and bearings"),
        ]
        categories = {}
        for name, desc in categories_data:
            cat, _ = Category.objects.get_or_create(
                name=name,
                defaults={"description": desc}
            )
            categories[name] = cat

        # 2. Suppliers
        suppliers_data = [
            ("Apex Industrial Supply Co.", "Marcus Vance", "marcus@apexindustrial.com", "+1-555-0192", "450 Logistics Blvd, Detroit, MI"),
            ("Global Tech Logistics", "Elena Chen", "contact@globaltechlog.com", "+1-555-0144", "1200 Innovation Way, Austin, TX"),
            ("ShieldSafe Safety Products", "David Miller", "sales@shieldsafe.com", "+1-555-0188", "88 Industrial Park Rd, Chicago, IL"),
            ("Pinnacle Packaging Ltd", "Rachel Adams", "orders@pinnaclepack.com", "+1-555-0177", "300 Freight Way, Atlanta, GA"),
        ]
        suppliers = {}
        for name, contact, email, phone, addr in suppliers_data:
            sup, _ = Supplier.objects.get_or_create(
                name=name,
                defaults={
                    "contact_name": contact,
                    "email": email,
                    "phone": phone,
                    "address": addr,
                }
            )
            suppliers[name] = sup

        # 3. Warehouse Locations
        locations_data = [
            ("Main Depot A", "Zone 1 - High Bay Aisle 01"),
            ("Main Depot A", "Zone 2 - Small Parts Rack 04"),
            ("Cold & Secure Vault B", "Aisle 02 - Shelf 10"),
            ("Receiving Bay C", "Inbound Staging Area"),
            ("Bulk Storage Yard D", "Outdoor Heavy Rack 08"),
        ]
        locations = []
        for name, zone in locations_data:
            loc, _ = WarehouseLocation.objects.get_or_create(
                name=name,
                zone_or_aisle=zone,
                defaults={"is_active": True}
            )
            locations.append(loc)

        # 4. Products (Diverse initial stock states: in_stock, low_stock, out_of_stock)
        products_data = [
            {
                "name": "Industrial Hydraulic Pump 2.5HP",
                "category": "Industrial Equipment",
                "supplier": "Apex Industrial Supply Co.",
                "location": locations[0],
                "unit": "pcs",
                "cost_price": Decimal("340.00"),
                "unit_price": Decimal("495.00"),
                "quantity": 48,
                "threshold": 10,
                "desc": "Heavy-duty hydraulic pump for manufacturing rigs",
            },
            {
                "name": "100m High-Speed Cat6 Cable Spool",
                "category": "Electronics & Hardware",
                "supplier": "Global Tech Logistics",
                "location": locations[1],
                "unit": "box",
                "cost_price": Decimal("45.00"),
                "unit_price": Decimal("78.50"),
                "quantity": 120,
                "threshold": 25,
                "desc": "High-bandwidth industrial Ethernet networking cable",
            },
            {
                "name": "Reinforced Nitrile Heavy Gloves (Pack of 50)",
                "category": "Safety & PPE",
                "supplier": "ShieldSafe Safety Products",
                "location": locations[1],
                "unit": "box",
                "cost_price": Decimal("18.00"),
                "unit_price": Decimal("29.99"),
                "quantity": 240,
                "threshold": 40,
                "desc": "Abrasion and chemical resistant nitrile workshop gloves",
            },
            {
                "name": "Double-Wall Corrugated Carton (Large)",
                "category": "Packaging Materials",
                "supplier": "Pinnacle Packaging Ltd",
                "location": locations[4],
                "unit": "carton",
                "cost_price": Decimal("1.80"),
                "unit_price": Decimal("3.50"),
                "quantity": 850,
                "threshold": 150,
                "desc": "Heavy-duty cardboard storage and shipping box",
            },
            {
                "name": "Heavy Duty Pallet Stretch Film (6 Rolls)",
                "category": "Packaging Materials",
                "supplier": "Pinnacle Packaging Ltd",
                "location": locations[4],
                "unit": "box",
                "cost_price": Decimal("52.00"),
                "unit_price": Decimal("85.00"),
                "quantity": 95,
                "threshold": 20,
                "desc": "20-micron industrial stretch wrap",
            },
            # Low stock items (testing reorder alerts)
            {
                "name": "ANSI Approved Hard Hat with Visor",
                "category": "Safety & PPE",
                "supplier": "ShieldSafe Safety Products",
                "location": locations[2],
                "unit": "pcs",
                "cost_price": Decimal("16.50"),
                "unit_price": Decimal("28.00"),
                "quantity": 6,
                "threshold": 15,
                "desc": "Impact resistant safety helmet with quick-adjust dial",
            },
            {
                "name": "Industrial High-Torque AC Motor 1500W",
                "category": "Industrial Equipment",
                "supplier": "Apex Industrial Supply Co.",
                "location": locations[0],
                "unit": "pcs",
                "cost_price": Decimal("220.00"),
                "unit_price": Decimal("350.00"),
                "quantity": 4,
                "threshold": 10,
                "desc": "3-phase high efficiency squirrel cage induction motor",
            },
            {
                "name": "Precision Microcontroller Board Pro-v4",
                "category": "Electronics & Hardware",
                "supplier": "Global Tech Logistics",
                "location": locations[1],
                "unit": "pcs",
                "cost_price": Decimal("22.50"),
                "unit_price": Decimal("39.00"),
                "quantity": 8,
                "threshold": 20,
                "desc": "Embedded programmable logic board for automation",
            },
            # Out of stock items (testing stockout alert)
            {
                "name": "Oil & Fuel Filter Heavy Spec",
                "category": "Automotive Spare Parts",
                "supplier": "Apex Industrial Supply Co.",
                "location": locations[1],
                "unit": "pcs",
                "cost_price": Decimal("12.00"),
                "unit_price": Decimal("24.00"),
                "quantity": 0,
                "threshold": 30,
                "desc": "High particulate filtration cartridge for heavy machinery",
            },
            {
                "name": "Class 2 Reflective Hi-Vis Vest (XL)",
                "category": "Safety & PPE",
                "supplier": "ShieldSafe Safety Products",
                "location": locations[2],
                "unit": "pcs",
                "cost_price": Decimal("5.50"),
                "unit_price": Decimal("11.99"),
                "quantity": 0,
                "threshold": 25,
                "desc": "Reflective mesh safety vest with radio tab",
            },
        ]

        created_count = 0
        for item in products_data:
            prod, created = Product.objects.get_or_create(
                name=item["name"],
                defaults={
                    "category": categories[item["category"]],
                    "supplier": suppliers[item["supplier"]],
                    "warehouse_location": item["location"],
                    "unit": item["unit"],
                    "cost_price": item["cost_price"],
                    "unit_price": item["unit_price"],
                    "quantity_on_hand": item["quantity"],
                    "reorder_threshold": item["threshold"],
                    "description": item["desc"],
                }
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Successfully seeded database! Added {created_count} products across {len(categories)} categories."
        ))
