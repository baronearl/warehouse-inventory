# Warehouse Inventory Management System with Demand Forecasting

> **Note for AI Agents & Contributors:** This is a student project focused on building a full-featured Warehouse Inventory Management System integrated with Demand Forecasting capabilities.

---

## 📌 Project Overview

This project is an end-to-end web-based inventory management platform designed to help warehouse managers and businesses monitor stock levels, manage supply chain operations, and predict future inventory demand using forecasting models.

### Key Objectives & Core Capabilities
1. **Warehouse & Stock Management**:
   - Tracking inventory levels, stock-ins, stock-outs, transfers, and adjustments across warehouse locations.
   - Categorization of items, SKU/barcode management, low-stock alerts, and reorder point thresholds.
2. **Demand Forecasting**:
   - Historical sales/usage data analysis to identify seasonality, trends, and demand patterns.
   - Predictive demand modeling to forecast future stock requirements and prevent both stockouts and overstocking.
3. **Order & Supplier Management**:
   - Purchase orders, supplier tracking, and customer dispatch management.
4. **Analytics & Reporting**:
   - Dashboard visualizations of warehouse utilization, inventory valuation, stock turnover, and forecast accuracy.

---

## 🛠️ Tech Stack

- **Backend Framework**: Django (Python 3)
- **Database**: PostgreSQL (`warehouse_inventory`)
- **Database Driver**: `psycopg` (v3)
- **Forecasting & Analytics** *(planned/in-progress)*: Python data science & machine learning libraries (e.g., pandas, NumPy, scikit-learn, statsmodels / Prophet)
- **Frontend**: Django Templates / HTML5 / CSS / JavaScript (or REST API / modern UI components)

---

## 📂 Project Structure

```text
warehouse-inventory/
├── README.md               # Project documentation and agent reference
├── manage.py               # Django management script
├── config/                 # Project configuration root
│   ├── settings.py         # Application settings & database configurations
│   ├── urls.py             # Root URL routing
│   ├── wsgi.py             # WSGI configuration
│   └── asgi.py             # ASGI configuration
└── venv/                   # Python virtual environment
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+
- PostgreSQL server running locally or accessible via network

### 2. Environment Setup
Clone the repository and set up a Python virtual environment:
```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Variables
Copy the example environment template and configure your secrets:
```bash
cp .env.example .env
```
Ensure your PostgreSQL database (e.g. `warehouse_inventory`) exists:
```bash
createdb -U postgres warehouse_inventory
```

### 4. Apply Migrations & Seed Sample Data
```bash
python manage.py migrate
python manage.py seed_inventory
python manage.py runserver
```

### 5. Access Credentials
- **Public Homepage**: `http://127.0.0.1:8000/`
- **Supervisor Access**: `supervisor` / `supervisor123`
- **Administrator Access**: `admin` / `admin123`
- **Django Admin**: `http://127.0.0.1:8000/admin/`

### 6. Run Test Suite
```bash
python manage.py test inventory
```

---

## 🤖 Guidance for AI Agents

When assisting with this project:
- **Context Awareness**: Keep in mind that this is an academic/student project; prioritize clear, clean, modular, and maintainable architecture with good documentation and readable code.
- **Modularity**: When creating new Django apps (e.g. `inventory`, `forecasting`, `orders`, `analytics`), keep concerns separated.
- **Forecasting Pipeline**: Ensure data preprocessing and forecasting logic are decoupled from views/models (e.g. via dedicated service modules).
- **Security & Best Practices**: Move sensitive credentials (secret keys, database passwords) to `.env` or environment variables when production-hardening.
