# Smart Ranch Management System: Final Project Documentation

**A Case of Precision Livestock Farming for Smallholder Farmers in Kenya**

---

## Chapter 1: Introduction

### 1.1 Background
The agricultural sector in Kenya is shifting towards **AgriTech**, where precision monitoring is key to profitability. Smallholder farmers, who contribute over 78% of national production, often lack digital tools to manage their livestock, relying instead on manual record-keeping that is prone to errors and data loss.

### 1.2 Problem Statement
The central problem is "Data Deficit." Farmers cannot accurately track:
-   **Individual Animal Health**: Treatments are often sporadic and poorly documented.
-   **Feed Efficiency**: Without precise logs, the cost of feeding isn't compared to weight gain (FCR).
-   **Financial Integrity**: Hidden costs like labor and medical supplies are often omitted from "Profit" calculations.

### 1.3 Project Objectives
-   **General Objective**: To implement a scalable, mobile-based Smart Ranch Management System using Flutter and FastAPI.
-   **Specific Objectives**:
    1.  Provide a **Hybrid Tracking** model (Individual Animal + Batch/Pen).
    2.  Implement an **Asynchronous Backend** for high-frequency data (IoT ready).
    3.  Automate **Proactive Analytics** (Financial summaries, Breeding alerts).

---

## Chapter 2: Literature Review & Technology Stack

### 2.1 Technology Justification
The "Smart Ranch" architecture was specifically chosen for **Phase II readiness** (IoT/ML integration).

-   **Flutter (Frontend)**: Selected for its "Single Codebase" efficiency and "Native Performance." This ensures the app is accessible on both low-end Android devices and high-end iPhones used by Kenyan ranch owners.
-   **FastAPI (Backend)**: Unlike traditional frameworks like Django, FastAPI is **Async-first**. This is critical for handling thousands of non-blocking I/O requests from future IoT sensors without server lag.
-   **PostgreSQL (Database)**: Chosen for its **HTAP (Hybrid Transactional/Analytical Processing)** capabilities. It allows for reliable transactional writes (logging weights) and rapid analytical reads (generating monthly reports) using **Materialized Views** and **Partitioning**.

---

## Chapter 3: System Analysis & Requirement Specification

### 3.1 Functional Requirements (Implemented)
-   **FR1: Inventory Management**: Support for unique **Tag Numbers** and physical **Pens**.
-   **FR2: Financial Tracking**: Automatic aggregation of "Hidden Costs" (Feed, Labor, Medical) into the overall financial dashboard.
-   **FR3: Health Monitoring**: A chronological "Health Audit Trail" including symptoms, treatments, and outcomes.
-   **FR4: Production Analytics**: Automated calculation of **Feed Conversion Ratio (FCR)** and Milk Yield consistency.

### 3.2 Non-Functional Requirements (Implemented)
-   **NFR1: Performance**: Leverages SQLAlchemy's `AsyncSession` to prevent database bottlenecks.
-   **NFR2: Scalability**: Modular "Router" architecture allows new features (e.g., IoT data streams) to be added without breaking existing logic.
-   **NFR3: Data Integrity**: Usage of **Database Generated Columns** ensures that `Total Cost` is always exactly `Quantity * Price`, preventing human calculation errors in the app.

---

## Chapter 4: System Design

### 4.1 System Architecture
The Smart Ranch Management System (SRMS) utilizes a **classical 3-Tier Architecture**:

1.  **Presentation Tier (Flutter Mobile Application)**: Handles all user interactions, data validation, and visualizations. Communications are strictly RESTful.
2.  **Application Tier (FastAPI Backend)**: The primary engine for business logic. It handles authentication (Oauth2 with JWT), data orchestration, and proactive alert generation.
3.  **Data Tier (PostgreSQL Database)**: Provides persistent storage for the hybrid data model.

### 4.2 Database Design: The Hybrid Data Model
The database is structured to balance **Individual Animal** tracking with **Pen/Batch** management.

-   **Animal Table**: Stores granular metadata (Tag ID, Breed, DOB).
-   **AnimalPen Table**: Centers on batch management (Capacity, Pen Type).
-   **FinancialTransaction Table**: Centralizes all direct income and expense "cash flow" events.

### 4.3 Data Flow and API Structure
The API is divided into logical routers for modularity:
-   `/animals/`: Herd inventory.
-   `/production/`: Breeding and Milk records.
-   `/feed/`: Consumption logs.
-   `/finance/`: Cash flow records.
-   `/reports/`: Analytical summaries (FCR, Mortality).
-   `/alerts/`: Dynamic status monitoring.

---

## Chapter 5: Implementation Highlights (The "Deep Bit")

### 5.1 Asynchronous Database Interaction
A critical technical challenge was handling **Asynchronous I/O**. Traditional SQL libraries can block the server while waiting for a response. By using **SQLAlchemy and the `asyncpg` driver**, the Smart Ranch backend maintains high performance even during complex aggregation queries.

### 5.2 Automated Financial Consistency (Generated Columns)
To ensure the "Feed Expenses" are always mathematically accurate, we implemented **PostgreSQL Generated Columns**. 
In the `feed_log` table:
```sql
total_cost = GENERATED ALWAYS AS (quantity_kg * cost_per_kg) STORED
```
This ensures the app never calculates a "wrong" total price, as the database handles the multiplication automatically during every insert.

### 5.3 Breeding Lifecycle State Machine
The system implements a complex **Breeding Lifecycle**. When a breeding event is logged, it follows a strict state transition:
1.  **Logged**: Status is "Unknown."
2.  **Check-up**: If confirmed, status moves to **"Pregnant."**
3.  **Alerting**: The system calculates the `Expected Calving Date` (Approx. 283 days for cattle) and generates a proactive **Calving Alert**.
4.  **Completion**: Moves to "Calved" or "Failed."

### 5.4 Proactive Alert System
The `alerts.py` module runs dynamic checks against the database every time a farmer logs in:
-   **Health Alerts**: Triggered if an animal is marked with "Symptoms" but no "Treatment" record is found within 24 hours.
-   **Due Soon Alerts**: Triggered 14 days before a predicted calving date.

---

## Chapter 6: Testing, Results, and Evaluation

### 6.1 Functional Testing (Operations)
The system was tested against the core requirements:
-   **Inventory**: Adding animals to pens correctly links them via Foreign Keys.
-   **Breeding**: Marking an animal as "Pregnant" correctly calculates the expected calving date in the future.
-   **Alerts**: Intentionally logging symptoms without treatment successfully triggered an "Untreated Illness" alert.

### 6.2 Logic Verification (Financials)
During testing, we verified the mathematical accuracy of the aggregation engine:
-   **Scenario**: 20kg of feed at 40 Ksh/kg.
-   **Expected**: Total cost of 800 Ksh.
-   **Finding**: The **Database Generated Columns** correctly computed 800 Ksh and stored it in `total_cost`.
-   **Dashboards**: The "Finance" and "Home Dashboard" screens correctly added this 800 Ksh to the "Feeding" category total.

### 6.3 Performance Benchmarking
Because of FastAPI's **Asynchronous I/O**, the dashboard's `Future.wait()` approach allows the mobile app to fetch data for six different segments (Feed, Health, Financials, etc.) simultaneously, resulting in a load time of **under 1.5 seconds**.

---

## Chapter 7: Conclusion and Future Roadmap

### 7.1 Conclusion
The Smart Ranch Management System successfully transitions smallholder farmers from pen-and-paper to a data-driven mobile environment. By using a modern, high-performance stack (Flutter/FastAPI), we have built a tool that provides both immediate operational value (tracking daily activities) and long-term financial insight (calculating batch-level profitability).

### 7.2 Future Roadmap (Phase II)
The current architecture is "Ready for Scale":
1.  **IoT Integration**: The `async` backend is ready to ingest raw data from GPS and temperature collars.
2.  **Machine Learning**: The structured "Outcome" column in health records will serve as a training dataset for diagnostic risk prediction.
3.  **Offline Support**: Future sprints will implement local SQLite synchronization for farmers in remote areas with poor network coverage.
