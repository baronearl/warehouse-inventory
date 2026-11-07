# Project Roadmap & Supervisor Milestone Deliverables

> **Academic Project:** Warehouse Inventory Management System with Demand Forecasting  
> **Purpose:** Step-by-step phased development plan designed for supervisor review check-ins, feature demos, and thesis/project defense milestones.

---

## 📅 Phased Milestone Breakdown

```
[ Milestone 1: Core Catalog ] ➔ [ Milestone 2: Stock Operations ] ➔ [ Milestone 3: Data & Analytics ]
                                                                             │
[ Milestone 6: Final Polish ] ⬅ [ Milestone 5: Smart Reordering ] ⬅ [ Milestone 4: Forecasting Engine ]
```

---

### **Milestone 1: Foundation & Core Catalog (Demo 1)**
* **Objective:** Establish the database schema, relational entities, public landing page, authentication gateway, and authenticated management interface.
* **Key Deliverables:**
  - **Public Homepage (`/`)**: Academic project overview, architecture breakdown, and supervisor login gateway.
  - **Authentication System (`/login/`, `/logout/`)**: Role-based authentication protecting internal warehouse operations.
  - Database schema & connection setup (PostgreSQL).
  - Core domain models: `Category`, `Supplier`, `WarehouseLocation`, and `Product` (SKU, barcode, unit price, minimum stock threshold).
  - Customized Django Admin interface with search filters, category tags, and list displays.
  - A mock dataset script to populate realistic warehouse products.
  - Clean Vanilla CSS interface (no Tailwind) inspired by PharmaLy design.
* **Supervisor Demonstration:**
  - Visiting the public homepage explaining the platform and system architecture.
  - Logging in with demo credentials (`supervisor` / `supervisor123`).
  - Accessing the protected dashboard and catalog with live stock calculations, low-stock threshold alerts, and search/filters.

---

### **Milestone 2: Stock Operations & Inventory Movement (Demo 2)**
* **Objective:** Turn the static catalog into an active operational warehouse with real-time tracking.
* **Key Deliverables:**
  - Transaction models: `StockMovement` (Stock In / Receiving, Stock Out / Dispatch, Transfer, and Audit Adjustment).
  - Core business logic: Automatic inventory calculation and atomic transaction handling.
  - Low-stock and safety-stock threshold triggers (warning flags when stock drops below reorder point).
  - Dedicated web pages for clerks: Stock Intake Form, Dispatch Form, and Live Stock Movement Audit Log.
* **Supervisor Demonstration:**
  - Performing a live Stock-In and Stock-Out transaction and showing stock balance updates in real time.
  - Triggering a low-stock alert when an item dips below its threshold.
  - Complete immutable audit trail showing who moved what item, when, and why.

---

### **Milestone 3: Data Generator & Analytics Dashboard (Demo 3)**
* **Objective:** Visualize warehouse performance and prepare historical time-series data for forecasting.
* **Design Reference:** Modeled after [PharmaLy Dashboard](https://pharmaly-next.vercel.app/dashboard) (clean modern SaaS aesthetic with sidebar navigation, metric cards, charts, and alert tables).
* **Key Deliverables:**
  - **Synthetic Data Generator Script**: Generates 6–12 months of daily historical sales/demand patterns (introducing seasonal spikes and trends) so forecasting models have realistic training data.
  - **Operational Dashboard (PharmaLy-inspired layout)**:
    - **Header & Navigation**: Fixed sidebar navigation (Dashboard, Inventory, Stock In/Out, Forecasting, Orders, Reports), breadcrumbs, search, user role badge.
    - **KPI Metric Cards**: Total Inventory Value, Active SKUs, Inbound/Outbound units, Low Stock count, Out-of-Stock count.
    - **Interactive Charts (Chart.js / ApexCharts)**:
      - *Demand & Stock Movement Overview* (with Daily/Weekly/Monthly time toggle).
      - *Inventory by Category* (Donut breakdown).
    - **Quick Status Tables**:
      - *Recent Stock Movements* (time, SKU, transaction type, quantity, status badge).
      - *Critical Alerts Box* (low stock / items reaching reorder threshold).
* **Supervisor Demonstration:**
  - Interactive executive dashboard with charts and operational KPIs.
  - Demonstration of historical demand datasets formatted for time-series analysis.

---

### **Milestone 4: Demand Forecasting Engine (Demo 4 - Academic Highlight)**
* **Objective:** Implement and visualize predictive demand algorithms.
* **Key Deliverables:**
  - Decoupled `forecasting` app/service layer.
  - **Baseline model**: Moving Average & Exponential Smoothing (Holt-Winters).
  - **Advanced model**: Time-series or ML model (e.g., Prophet, SARIMA, or Random Forest/XGBoost).
  - Forecasting interface: Product detail page showing past 30–90 days actual demand vs. next 7–30 days predicted demand curve with confidence intervals.
* **Supervisor Demonstration:**
  - Selecting any product and generating a demand forecast graph for the upcoming month.
  - Explaining the mathematical approach and the rationale for choosing specific algorithms.

---

### **Milestone 5: Decision Support & Model Evaluation (Demo 5)**
* **Objective:** Bridge forecasting to actionable warehouse decisions and prove model performance.
* **Key Deliverables:**
  - **Evaluation Metrics Module**: Calculates MAE (Mean Absolute Error), RMSE, and MAPE to prove model accuracy (essential for academic grading).
  - **Smart Reorder Recommendation System**: Calculates optimal reorder quantity based on:
    $$\text{Reorder Quantity} = \text{Forecasted Demand during Lead Time} + \text{Safety Stock} - \text{Current Stock}$$
  - Report export feature (downloadable CSV/PDF summary for suppliers and purchase orders).
* **Supervisor Demonstration:**
  - Model evaluation scorecard comparing baseline vs. advanced model accuracy.
  - Auto-generated purchase recommendation list suggesting exact reorder dates and quantities.

---

### **Milestone 6: Role-Based Access, UI Polish & Final Defense Prep (Demo 6)**
* **Objective:** Package the project for presentation and final grading.
* **Key Deliverables:**
  - User roles & permissions: *Warehouse Manager*, *Inventory Clerk*, and *Auditor/Supervisor*.
  - Polished modern responsive UI.
  - Comprehensive documentation, user manual, and presentation slides.
* **Supervisor Demonstration:**
  - Final project walkthrough from login with different role permissions to final reporting.
  - Complete demo ready for oral defense.
