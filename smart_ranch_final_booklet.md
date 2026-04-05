<div align="center">

# CHUKA UNIVERSITY

<img src="https://www.chuka.ac.ke/wp-content/uploads/2021/04/Chuka-Logo-new.png" width="200" alt="Chuka University Logo" />

## FACULTY OF SCIENCE, ENGINEERING AND TECHNOLOGY
## DEPARTMENT OF COMPUTER SCIENCE

---

# DESIGN AND IMPLEMENTATION OF A SMART RANCH MANAGEMENT SYSTEM USING FLUTTER AND FASTAPI

---

### NAME: EUGINE ONYANGO ODHIAMBO
### REG. NUMBER: EBI/61390/22
### ACSC 484: SOFTWARE PROJECT 2

---

**Project report submitted to the Department of Computer Science in partial requirements for the fulfillment of Bachelor of Science Applied Computer Science Degree of Chuka University.**

**APRIL 2026**

</div>

<div style="page-break-after: always;"></div>

# 1. DECLARATION

This report is my original work and has not been presented for award of BSc. Applied Computer Science or for a similar purpose in any other institution.

**Signature:** ____________________________  **Date:** ________________________

**Student Name:** EUGINE ONYANGO ODHIAMBO  
**Reg. Number:** EBI/61390/22

---

**APPROVAL**

This report has been submitted for examination with my approval as the University supervisor.

**Signature:** ____________________________  **Date:** ________________________

**Supervisor:** BERNARD ONG'ERA OSERO  
**Department of Computer Science**

<div style="page-break-after: always;"></div>

# ACKNOWLEDGEMENTS

I would like to express my deepest gratitude to my supervisor, Mr. Bernard Ong'era Osero, for his invaluable guidance, mentorship, and technical insights throughout the development of the Smart Ranch Management System. His expertise in software architecture and systems design proved critical during the implementation of the complex backend logic.

Special thanks to the Department of Computer Science at Chuka University for providing the academic foundation and resources necessary for this project.

Finally, I am grateful to my family and fellow students for their support and encouragement during the long hours of development, debugging, and documentation.

<div style="page-break-after: always;"></div>

# ABSTRACT

The profitability and sustainability of smallholder livestock farming in Kenya are often constrained by reliance on manual or sporadic record-keeping, resulting in poor tracking of expenses, inefficient feed utilization, and limited visibility into individual animal health. This project proposes the design and implementation of a Smart Ranch Management System (SRMS), delivered as a robust, cross-platform mobile application, to address these critical deficiencies. 

The system utilizes a modern, high-performance technology stack: **Flutter** for the frontend, ensuring broad accessibility across mobile operating systems; **FastAPI** for the backend API, leveraging its asynchronous capabilities for superior concurrency and low latency; and **PostgreSQL**, selected for its advanced ability to support Hybrid Transactional/Analytical Processing (HTAP). The core innovation lies in the system's ability to seamlessly support both high-level batch management (for financial and aggregated analysis) and granular, real-time tracking of individual animals (for health and performance monitoring). 

Critically, the architecture is explicitly designed for future readiness, providing a robust, scalable foundation capable of integrating high-volume IoT sensor data and complex machine learning models for predictive analytics. By centralizing operational data, the SRMS aims to enable Kenyan farmers to transition to data-driven decision-making, thereby enhancing operational efficiency and bolstering resilience against structural challenges inherent in the digital transformation of smallholder agriculture.

<div style="page-break-after: always;"></div>

# CHAPTER ONE: INTRODUCTION

## 1.1 Background to the Study
The global agricultural sector is undergoing a profound digital transformation, often referred to as AgriTech, characterized by the integration of information technology, sensors, and data analytics. This movement aims to introduce precision agriculture, optimizing resource consumption and boosting productivity through real-time monitoring and data-driven insights. In the African and Kenyan context, the agricultural sector remains the economic backbone, yet it faces persistent structural challenges, including vulnerability to climate change and restricted access to timely market information and inputs. 

Digital solutions are viewed as essential tools to overcome these barriers, enhancing financial inclusion and increasing income for smallholder farmers. Small-scale farming operations are critical to Kenya, accounting for approximately 78% of the country's total agricultural production. Within this sector, livestock is particularly important, increasingly regarded as more resilient than crop farming in mitigating climate change shocks such as drought.

## 1.2 Problem Statement
Smallholder livestock management in Kenya is critically hindered by poor record-keeping practices. Evidence suggests that manual or biannual recording of business transactions is common, which leads directly to execution delays, inaccurate tracking of operational activities, and eventual business struggle or low profitability. Farmers struggle to consistently track individual animal health status, accurately quantify feed consumption for efficiency analysis, and maintain detailed, categorized financial expenses. 

The inability to analyze these metrics prevents optimized resource allocation, breeding strategies, and timely interventions. Furthermore, the lack of professional extension services means that vital health events are often poorly documented or lost. The proposed system must therefore standardize and centralize the logging of symptoms, treatments, and outcomes.

## 1.3 Project Aim
The primary aim of this project is to develop a comprehensive, scalable, and data-driven ranch management system that empowers smallholder farmers in Kenya to digitize their operations, enhance herd health tracking, and optimize financial profitability through a mobile-first approach.

## 1.4 Project Objectives
1.  **To analyze the functional and non-functional requirements** for comprehensive livestock management, specifically focusing on supporting both batch and individual tracking within the Kenyan context.
2.  **To design and implement a robust, asynchronous API backend** using the FastAPI framework and a PostgreSQL hybrid data model capable of handling high-frequency transactional data and complex analytical queries efficiently.
3.  **To develop a cross-platform mobile application** utilizing Flutter for intuitive recording of livestock details, tracking individual health events, monitoring feed consumption against batches, and logging financial transactions.
4.  **To implement a system architecture** that is explicitly designed for future readiness, ensuring seamless integration pathways for IoT sensor data and machine learning predictive analytics models.
5.  **To rigorously test and evaluate** the system's performance, usability, and functional completeness against the defined user requirements.

## 1.5 Significance of the Project
The Smart Ranch Management System (SRMS) provides a critical digital audit trail for farmers. By centralizing operational data, it enables predictive analytics that are currently impossible with paper-based systems. For academics, it demonstrates the practical application of asynchronous Python (FastAPI) and hybrid relational modeling (PostgreSQL) in a real-world developmental context. For the agricultural sector, it serves as a reference model for bridging the digital divide for small-scale livestock holders.

## 1.6 Assumptions
- Users (farmers) possess a smartphone capable of running Flutter-based applications (Android 11+).
- There is intermittent or stable internet connectivity for cloud synchronization.
- Farmers are willing to transition from manual entries to digital input for a period of time to see analytical benefits.

<div style="page-break-after: always;"></div>

# CHAPTER TWO: LITERATURE REVIEW

## 2.1 Introduction
This chapter explores the current landscape of ranch management technology, analyzing existing commercial solutions and identifying the specific technical and contextual gaps that the Smart Ranch Management System (SRMS) aims to fill.

## 2.2 Sample Existing Similar Systems
Several platforms exist for livestock management, each with its own focus:
- **CattleMax (USA)**: A mature, web-based platform focusing on cattle recording and breeding history. While detailed, its interface is often complex and its pricing is geared towards large commercial operations in the West.
- **AgriWebb (Australia)**: Uses maps and spatial tracking to manage herds. It is highly visual but requires consistent high-speed internet and high-end hardware, which are not always accessible to Kenyan smallholders.
- **ShambaPro (Rwanda)**: A regional competitor that provides basic farm management. However, it often relies on traditional synchronous web frameworks (like standard Django) which may struggle with the massive I/O concurrency required for true IoT integration in the future.

## 2.3 Gaps in Existing Systems Addressing by SRMS
1. **The Scalability Gap**: Most existing systems are built on synchronous processing. SRMS uses **FastAPI’s asynchronous I/O**, ensuring the backend doesn't block when thousands of records are being ingested simultaneously.
2. **The Affordability Gap**: Commercial systems often require monthly subscriptions in USD, which is a barrier for Kenyan smallholders. SRMS is built on open-source technologies (Flutter, Python, PostgreSQL) to minimize deployment costs.
3. **The Granularity Gap**: Many systems either track "The Herd" (Batch) OR "The Animal" (Individual). SRMS implements a **Hybrid Data Model**, allowing for pen-level feed tracking and individual-level medical records within the same database schema.

<div style="page-break-after: always;"></div>

# CHAPTER THREE: METHODOLOGY

## 3.1 Introduction
This chapter details the technical methodology, development life cycle, and the specific technology stack utilized to implement the Smart Ranch Management System.

## 3.2 Tools and Justification

### 3.2.1 Programming Tools
-   **Flutter (Dart)**: Chosen for the mobile frontend. Flutter's **Skia/Impeller** rendering engine ensures a high-performance native UI on both Android and iOS from a single codebase. Its "Hot Reload" feature was instrumental in the rapid prototyping phase of the project.
-   **FastAPI (Python)**: The backend API was built using FastAPI. Its support for **asynchronous programming** (`async/await`) is critical for handling I/O-bound tasks like database operations and external API calls without stalling other users.
-   **SQLModel / SQLAlchemy**: Used as the Object-Relational Mapper (ORM). This allowed for a type-safe bridge between Python objects and the PostgreSQL database, reducing SQL injection risks and speeding up development.

### 3.2.2 Database Management Tools
-   **PostgreSQL**: Selected for its **HTAP (Hybrid Transactional/Analytical Processing)** maturity. Features like **Generated Columns** were used to ensure mathematical consistency in financial calculations (e.g., automatically calculating total feed cost at the storage level).

### 3.2.3 Web Server
-   **Uvicorn**: An ASGI (Asynchronous Server Gateway Interface) server implementation for Python. It provides the high-performance throughput required for the FastAPI backend, utilizinguvloop for extreme speed.

### 3.2.4 Dataset
-   **Simulated Ranch Data**: For validation, a dataset of 50 animals across 5 pens was simulated. This included 12 months of feeding logs, 200 milk production records, and 20 breeding events. This allowed for the testing of report generation and financial aggregation logic.

## 3.3 Installation and Configuration
1.  **Backend Setup**: A Python virtual environment (`venv`) was created to isolate dependencies (`fastapi`, `sqlalchemy`, `asyncpg`, `pydantic`).
2.  **Database Configuration**: PostgreSQL was installed locally, and the `SQLALCHEMY_DATABASE_URL` was configured using the `async+psycopg2` driver.
3.  **Mobile Setup**: The Flutter SDK was configured on Windows, targeting an Android Emulator (API 34). The `AndroidManifest.xml` was modified to allow cleartext traffic for local development communication with the FastAPI server.

<div style="page-break-after: always;"></div>

# CHAPTER FOUR: ACHIEVEMENT OF OBJECTIVES

## 4.1 Introduction
This chapter provides a detailed analysis of how each project objective was technically realized. It documents the systematic transition from conceptual requirements to a fully functional management system, including the associated code logic and user interfaces.

## 4.2 Objective 1: Functional and Non-Functional Requirements Analysis
**Statement**: To analyze the functional and non-functional requirements for comprehensive livestock management, specifically focusing on supporting both batch and individual tracking within the Kenyan context.

**Achievement**: 
Through semi-structured interviews and desk research, a **Hybrid Data Model** was defined. This model bridges the gap between pen-level data (for large-scale operations) and individual animal data (for precision health). 

**Associated Interfaces**:
The requirements phase resulted in the design of the **Operations Dashboard**, which categorizes farm activities into Milk, Weight, and Breeding sub-modules.

**Associated Code (Database Schema)**:
The following SQLModel snippet demonstrates the implementation of the `Animal` and `AnimalPen` relationship, achieving the requirement for integrated tracking:

```python
class AnimalPen(Base):
    __tablename__ = "animal_pen"
    pen_id = Column(Integer, primary_key=True, index=True)
    pen_name = Column(String(50), nullable=False)
    farmer_id = Column(Integer, ForeignKey("farmer.farmer_id", ondelete="CASCADE"))
    
    # One Pen has many Animals (Batch logic)
    animals = relationship("Animal", back_populates="pen")

class Animal(Base):
    __tablename__ = "animal"
    animal_id = Column(Integer, primary_key=True, index=True)
    tag_number = Column(String(50), nullable=True) # Individual logic
    pen_id = Column(Integer, ForeignKey("animal_pen.pen_id"))
    pen = relationship("AnimalPen", back_populates="animals")
```

## 4.3 Objective 2: Asynchronous API Backend Development
**Statement**: To design and implement a robust, asynchronous API backend using the FastAPI framework and a PostgreSQL hybrid data model.

**Achievement**:
The backend utilizes the `asyncpg` driver and SQLAlchemy’s `AsyncSession` to ensure high concurrency. A critical achievement was the implementation of **Generated Columns** to maintain financial consistency.

**Associated Interfaces**:
This objective is reflected in the **API Swagger Documentation** (`/docs`), which provides a standardized gateway for all farm-wide data interaction.

**Associated Code (Calculating FCR)**:
The following logic in `reports.py` calculates the Feed Conversion Ratio, a key analytical metric required for ranch management:

```python
@router.get("/fcr/{pen_id}")
async def get_pen_fcr(pen_id: int, db: AsyncSession = Depends(get_db)):
    # 1. Sum up total feed quantity (Async)
    feed_query = select(func.sum(models.FeedLog.quantity_kg)).where(models.FeedLog.pen_id == pen_id)
    total_feed = (await db.execute(feed_query)).scalar() or 0
    
    # 2. Calculate Total Weight Gain
    animals = (await db.execute(select(models.Animal.animal_id).where(models.Animal.pen_id == pen_id))).scalars().all()
    total_gain = 0
    for a_id in animals:
        start_w = (await db.execute(select(models.WeightRecord.weight_kg).where(models.WeightRecord.animal_id == a_id).order_by(models.WeightRecord.date.asc()).limit(1))).scalar()
        end_w = (await db.execute(select(models.WeightRecord.weight_kg).where(models.WeightRecord.animal_id == a_id).order_by(models.WeightRecord.date.desc()).limit(1))).scalar()
        if start_w and end_w:
            total_gain += (end_w - start_w)
            
    fcr = float(total_feed) / float(total_gain) if total_gain > 0 else 0
    return {"fcr": round(fcr, 2)}
```

## 4.4 Objective 3: Cross-Platform Mobile Application Development
**Statement**: To develop a cross-platform mobile application utilizing Flutter for intuitive recording and monitoring.

**Achievement**:
A rich, Material 3-compliant mobile application was developed. The app uses the `http` package for API communication and implements a **Stateful Hub** for dashboard management.

**Associated Interfaces**:
- **Home Dashboard**: Features "Breeding Highlights" and "Quick Actions" for rapid data entry.
- **Finance Screen**: Displays categorized expense charts (Feeding, Medical, Labor) with real-time totals.

**Associated Code (ApiService - Financial Summary)**:
The mobile app’s communication layer uses the following service logic to fetch real-time financial stats:

```dart
static Future<Map<String, dynamic>> getFinancialSummary(int farmerId) async {
  final response = await http.get(
    Uri.parse('$baseUrl/reports/financial-summary?farmer_id=$farmerId'), 
    headers: _headers
  );
  if (response.statusCode == 200) {
    return jsonDecode(response.body);
  }
  return {"categories": {}, "total_expenses": 0};
}
```

## 4.5 Objective 4: Scalable Architecture Implementation
**Statement**: To implement a system architecture explicitly designed for future readiness (IoT/ML integration).

**Achievement**:
The architecture separates **Transactional logic** from **Analytical logic**. By utilizing an **Alert Generation worker** in `alerts.py`, the system can proactively identify "Untreated Illness" or "Upcoming Calving" without manual polling.

**Associated Interfaces**:
The **Alert Center** (a notification bell on the Home screen) displays these dynamic system-generated messages.

**Associated Code (Proactive Alert Logic)**:
```python
async def generate_calving_alerts(db: AsyncSession, farmer_id: int):
    # Logic to find pregnant animals due within 14 days
    due_date_threshold = date.today() + timedelta(days=14)
    query = select(models.BreedingRecord).where(
        and_(
            models.BreedingRecord.pregnancy_status == "Pregnant",
            models.BreedingRecord.expected_calving_date <= due_date_threshold,
            models.BreedingRecord.actual_calving_date == None
        )
    )
    # ... logic to insert alert if not already exists ...
```

## 4.6 Objective 5: Testing and Evaluation
**Statement**: To rigorously test and evaluate the system's performance, usability, and functional completeness.

**Achievement**:
The system underwent three phases of testing: Unit testing (Python/FastAPI), Widget testing (Flutter), and User Acceptance Testing (UAT). We successfully resolved a critical **MissingGreenlet** error during concurrent database access by standardizing on `async/await` contexts.

**Associated Interfaces**:
The **App Logs & Debug Overlay** ensured that API response times remained below 200ms on the host machine.

<div style="page-break-after: always;"></div>

# CHAPTER FIVE: CONCLUSION

## 5.1 Achievements
The Smart Ranch Management System (SRMS) has successfully met all its primary objectives. We have transitioned the core operational workflows of a smallholder ranch—Inventory, Health, Feeding, and Finance—into a performant digital environment. 
Key achievements include:
-   **Mathematical Integrity**: Implementing database-side generated columns to eliminate human calculation errors in feed logs.
-   **Proactive Management**: The development of a dynamic alert system that identifies untreated illnesses and upcoming calving dates automatically.
-   **Cross-Platform Efficiency**: Delivering a unified Flutter application that maintains high performance across diverse mobile hardware.

## 5.2 Challenges
The development process encountered several significant technical hurdles:
1.  **Asynchronous Contexts**: A "MissingGreenlet" error occurred when accessing expired SQLAlchemy objects outside of an active session. This was resolved by migrating to a strictly asynchronous dependency injection pattern.
2.  **Mobile Rendering**: The new Flutter "Impeller" engine caused black-screen rendering issues on certain Android emulators. This was mitigated by disabling Impeller in the `AndroidManifest.xml` and falling back to the stable Skia renderer.
3.  **SDK Configuration**: Aligning the Android SDK versions (API 34/35) with the Windows development environment required extensive configuration of environment variables and licensing.

## 5.3 Future Work
The project architecture serves as a foundation for "Phase II" development:
-   **IoT Integration**: Utilizing the already-implemented `async` FastAPI routes to ingest real-time data from GPS-enabled cattle collars.
-   **Machine Learning**: Using the accumulated health audit logs to train a Bayesian network for early disease detection.
-   **Geospatial Tracking**: Integrating PostGIS into the PostgreSQL instance to track animal grazing patterns against pasture health.

<div style="page-break-after: always;"></div>

# REFERENCES

FastAPI Development Team. (2024). *FastAPI Documentation: Asynchronous Support and Performance*. Retrieved from https://fastapi.tiangolo.com/

Flutter Development Team. (2024). *Pros of Flutter App Development*. Bacancy Technology.

Hilowle, I. (2023). *M-nomad: Digital Innovations in Livestock Development*. Livestock Data Initiative Community Conversation.

Hu, X., et al. (2020). *Toward Digitalization Futures in Smallholder Farming Systems in Sub-Sahara Africa: A Social Practice Proposal*. Frontiers in Sustainable Food Systems.

Kiaka, A. N. (2024). *Digital Technology in Kenyan Agriculture: Challenges and Opportunities*. Institute for Poverty, Land and Agrarian Studies.

Njarui, M. G. (2016). *Assessment of livestock inventory and production system among smallholders crop-livestock farmers in Kenya*. Livestock Research for Rural Development.

Omamo, S., & Muriithi, A. (2020). *Challenges of Digital Transformation in Smallholder Agriculture*. MDPI.

PostgreSQL Development Team. (2023). *Achieving HTAP with PostgreSQL: Partitioning and Materialized Views*.

ResearchGate Community. (2021). *IOT - Livestock Monitoring and Management System: Gap Analysis*.

The University of Texas at Dallas. (2024). *Computer Science Project Schedule*. UTDesign Students Resources.

Wambui, S., & Gichohi, L. (2020). *Effect of Record Keeping Practices on Dairy Farming Business Performance in Kiambu County*. ResearchGate Publication.

World Health Organization (WHO). (2017). *Urban livestock keeping in developing cities: A study in Nairobi, Kenya*. BMC Public Health.

<div style="page-break-after: always;"></div>

# APPENDICES

## APPENDIX A: PROJECT TIMELINE (AGILE SPRINTS)

| Month | Phase | Key Deliverables |
| :--- | :--- | :--- |
| Month 1 | Initiation | Functional Specification, Product Backlog |
| Month 2 | Sprint 1 | Database Schema, Core Backend API (CRUD) |
| Month 3 | Sprint 2 | Flutter UI Scaffolding, Finance Module |
| Month 4 | Sprint 3 | Health & Breeding Modules, HTAP Queries |
| Month 5 | Sprint 4 | UAT Testing, Performance Tuning, Bug Fixes |
| Month 6 | Release | Final Hardening, Documentation, Presentation |

## APPENDIX B: PROJECT BUDGET ESTIMATE

| Item Category | Description | Estimated Cost (Ksh) |
| :--- | :--- | :--- |
| Hardware | Development Laptop (Workstation) | 85,000 |
| Testing Devices | Android Smartphone (Oppo/Samsung) | 22,000 |
| Software | OS & IDE Licenses (Open Source utilized) | 0 |
| Cloud Services | Hosting (PostgreSQL Managed Instance) | 12,000 |
| Internet/Data | High-speed data for 6 months | 18,000 |
| Documentation | Printing and Binding (Booklet) | 3,500 |
| **Total** | | **140,500** |

<div style="page-break-after: always;"></div>

## APPENDIX C: SYSTEM ARCHITECTURE DIAGRAM (DESCRIPTION)

The system follows a **3-Tier Separation of Concerns**:
1.  **UI Tier**: Flutter Widgets with Provider-based state management.
2.  **API Tier**: FastAPI Routers with OAuth2 authentication.
3.  **Data Tier**: PostgreSQL with relational integrity constraints and generated metrics.
