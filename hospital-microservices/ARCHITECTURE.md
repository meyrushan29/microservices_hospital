# 🏗️ Hospital Microservices Architecture — Design & Implementation

## Executive Summary

The Hospital Management System implements a **modern microservices architecture** following industry best practices. This document provides deep technical insight into system design, component relationships, and architectural decisions.

---

## 1. System Architecture Overview

### High-Level Architecture Diagram

```
┌────────────────────────────────────────────────────────────────────┐
│                          CLIENT LAYER                               │
│  (Web Browser, Mobile App, Third-party Systems)                    │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             │ HTTP/REST
                             ↓
┌────────────────────────────────────────────────────────────────────┐
│                   API GATEWAY (Port 8000)                           │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │ Core Functions:                                             │   │
│  │  • Request routing to microservices                        │   │
│  │  • JWT token validation                                   │   │
│  │  • Role-Based Access Control (RBAC)                      │   │
│  │  • Request/Response logging                              │   │
│  │  • Cross-Origin Resource Sharing (CORS) handling         │   │
│  └────────────────────────────────────────────────────────────┘   │
└──┬──────┬──────┬──────┬──────┬──────┬──────────────────────────────┘
   │      │      │      │      │      │
   │      │      │      │      │      │
   ↓      ↓      ↓      ↓      ↓      ↓
┌──────┐┌──────┐┌──────┐┌──────┐┌──────┐┌──────┐
│ 1️⃣  ││ 2️⃣  ││ 3️⃣  ││ 4️⃣  ││ 5️⃣  ││ 6️⃣  │  MICROSERVICES
│Patient││Doctor││Appt. ││Pharm.││Bill. ││Lab   │  (Independent Instances)
│Svc    ││Svc   ││Svc   ││Svc   ││Svc   ││Svc   │
│:8001  ││:8002 ││:8003 ││:8004 ││:8005 ││:8006 │
└──────┘└──────┘└──────┘└──────┘└──────┘└──────┘
```

### Key Architectural Principles

| Principle | Implementation | Benefit |
|---|---|---|
| **Single Responsibility** | Each service handles one business domain | Easy to understand, test, deploy |
| **Independence** | Services can be deployed separately | Minimal impact of updates |
| **Loose Coupling** | Services communicate through API Gateway | Changes isolated to one service |
| **High Cohesion** | Related operations grouped in one service | Clear ownership and accountability |
| **Resilience** | Service failure doesn't cascade | System remains partially operational |

---

## 2. Detailed Microservice Specifications

### Service 1: Patient Service (Port 8001)
**Developed by:** Meyrushan N

**Responsibilities:**
- Patient registration and profile management
- Medical history tracking
- Admission/discharge records
- Patient data validation and storage

**Core Endpoints:**
```
POST   /patients              → Register new patient
GET    /patients              → Retrieve all patients
GET    /patients/{id}         → Get specific patient details
PUT    /patients/{id}         → Update patient information
DELETE /patients/{id}         → Remove patient (admin only)
```

**Data Model:**
```python
Patient {
  id: int (unique identifier)
  name: str (full name)
  age: int
  gender: str (Male/Female/Other)
  blood_type: str (A+, B+, O+, etc.)
  phone: str (contact number)
  address: str (residential address)
  admitted_date: date
  medical_history: str (optional)
}
```

---

### Service 2: Doctor Service (Port 8002)
**Developed by:** Laxshika S

**Responsibilities:**
- Doctor registration and profile management
- Specialization tracking
- Availability management
- Qualifications and credentials

**Core Endpoints:**
```
POST   /doctors              → Register new doctor
GET    /doctors              → Retrieve all doctors
GET    /doctors/{id}         → Get specific doctor details
PUT    /doctors/{id}         → Update doctor information
DELETE /doctors/{id}         → Remove doctor (admin only)
GET    /doctors?spec=...     → Filter by specialization
```

**Data Model:**
```python
Doctor {
  id: int
  name: str
  specialization: str (Cardiology, Neurology, etc.)
  phone: str
  email: str
  qualification: str (MBBS, MD, etc.)
  experience_years: int
  is_available: bool
}
```

---

### Service 3: Appointment Service (Port 8003)
**Developed by:** Laksopan R

**Responsibilities:**
- Appointment scheduling
- availability checking
- Appointment status management
- Appointment history tracking

**Core Endpoints:**
```
POST   /appointments         → Book new appointment
GET    /appointments         → Retrieve all appointments
GET    /appointments/{id}    → Get appointment details
PUT    /appointments/{id}    → Update appointment status
DELETE /appointments/{id}    → Cancel appointment
GET    /appointments/doctor/{id}  → Get doctor's appointments
```

**Data Model:**
```python
Appointment {
  id: int
  patient_id: int (foreign key to Patient Service)
  doctor_id: int (foreign key to Doctor Service)
  date: date
  time: str (HH:MM format)
  reason: str (reason for appointment)
  status: str (pending, confirmed, completed, cancelled)
  notes: str (optional consultation notes)
}
```

---

### Service 4: Pharmacy Service (Port 8004)
**Developed by:** Viththakan N

**Responsibilities:**
- Medicine inventory management
- Prescription processing
- Stock level tracking
- Medicine availability checking

**Core Endpoints:**
```
GET    /medicines            → Get all medicines
POST   /medicines            → Add new medicine (admin only)
PUT    /medicines/{id}       → Update medicine info/stock
DELETE /medicines/{id}       → Remove medicine (admin only)
POST   /prescriptions        → Create prescription (doctor only)
GET    /prescriptions        → Retrieve prescriptions
PUT    /prescriptions/{id}   → Update prescription status
```

**Data Model:**
```python
Medicine {
  id: int
  name: str
  generic_name: str
  manufacturer: str
  dosage: str
  unit_price: float
  stock_quantity: int
  expiry_date: date
}

Prescription {
  id: int
  patient_id: int
  doctor_id: int
  medicine_id: int
  dosage_instructions: str
  quantity: int
  prescribed_date: date
  status: str (pending, filled, completed)
}
```

---

### Service 5: Billing Service (Port 8005)
**Developed by:** Hariyah L

**Responsibilities:**
- Invoice generation
- Payment processing
- Billing reports
- Financial transaction tracking

**Core Endpoints:**
```
POST   /bills                → Generate new bill
GET    /bills                → Retrieve all bills
GET    /bills/{id}           → Get bill details
PUT    /bills/{id}/payment   → Record payment
DELETE /bills/{id}           → Cancel bill (admin only)
GET    /bills/patient/{id}   → Get patient's bills
GET    /reports/revenue      → Revenue reports (admin only)
```

**Data Model:**
```python
Bill {
  id: int
  patient_id: int
  appointment_id: int
  medicine_cost: float
  lab_test_cost: float
  consultation_fee: float
  total_amount: float
  date_issued: date
  due_date: date
  status: str (pending, partial, paid)
  payment_method: str
  transaction_id: str
}
```

---

### Service 6: Lab Service (Port 8006)
**Developed by:** Nilakshan V

**Responsibilities:**
- Lab test ordering
- Test result management
- Test scheduling
- Result notification

**Core Endpoints:**
```
POST   /tests                → Order new lab test
GET    /tests                → Retrieve all tests
GET    /tests/{id}           → Get test details
PUT    /tests/{id}           → Update test status
DELETE /tests/{id}           → Cancel test (admin only)
POST   /test-results         → Record test results
GET    /test-results/{id}    → Get test results
```

**Data Model:**
```python
LabTest {
  id: int
  patient_id: int
  doctor_id: int (who ordered)
  test_type: str (Blood Count, Urinalysis, etc.)
  ordered_date: date
  scheduled_date: date
  status: str (pending, in-progress, completed)
  notes: str
}

TestResult {
  id: int
  test_id: int
  result_value: str
  reference_range: str
  status: str (normal, abnormal)
  recorded_date: date
  technician_id: int
}
```

---

## 3. API Gateway Architecture

### Gateway Responsibilities

```
┌─────────────────────────────────────────┐
│        Incoming Client Request           │
└──────────────────┬──────────────────────┘
                   │
                   ↓
        ┌──────────────────────┐
        │  1. Route Matching   │
        │  Extract path: /patients
        │  Determine Service: Patient Service (8001)
        └──────┬───────────────┘
               │
               ↓
        ┌──────────────────────┐
        │ 2. Authentication    │
        │  Extract JWT token   │
        │  Validate signature  │
        │  Check expiration    │
        └──────┬───────────────┘
               │
               ↓
        ┌──────────────────────┐
        │ 3. Authorization     │
        │  Extract user role   │
        │  Check RBAC rules    │
        │  Verify permissions  │
        └──────┬───────────────┘
               │
               ↓
        ┌──────────────────────┐
        │ 4. Request Routing   │
        │  Forward to service  │
        │  Include token       │
        │  Pass headers        │
        └──────┬───────────────┘
               │
               ↓
     ┌─────────────────────────┐
     │  Microservice Processing │
     └──────────┬────────────────┘
                │
                ↓
        ┌──────────────────────┐
        │ 5. Response Handling │
        │  Receive response    │
        │  Log transaction     │
        │  Return to client    │
        └──────┬───────────────┘
               │
               ↓
   ┌────────────────────────────┐
   │   Return to Client          │
   └────────────────────────────┘
```

### Port Configuration

| Component | Port | Status |
|---|---|---|
| API Gateway | 8000 | Main entry point |
| Patient Service | 8001 | Direct access (dev only) |
| Doctor Service | 8002 | Direct access (dev only) |
| Appointment Service | 8003 | Direct access (dev only) |
| Pharmacy Service | 8004 | Direct access (dev only) |
| Billing Service | 8005 | Direct access (dev only) |
| Lab Service | 8006 | Direct access (dev only) |

### How the Gateway Eliminates Multiple Port Problem

**Without Gateway (Complexity):**
```
Client must know all 6 ports and handle:
- Authentication with each service separately
- Different request/response formats
- Service discovery and updates
- Error handling across services
- CORS for each service

Result: Client code is complex and brittle
```

**With Gateway (Simplification):**
```
Client only knows port 8000:
- Single authentication point
- Consistent request/response format
- Automatic service routing
- Centralized logging and monitoring
- Single CORS policy

Result: Client code is simple and maintainable
```

---

## 4. Security Architecture

### JWT Token Flow

```
1. Authentication Request
   POST /authenticate
   {
     "username": "admin",
     "password": "admin123"
   }

2. Server generates JWT containing:
   Header:  {alg: "HS256", typ: "JWT"}
   Payload: {
     user_id: 1,
     username: "admin",
     role: "admin",
     exp: 1640000000 (expiration time)
   }
   Signature: HMAC-SHA256(header.payload, secret_key)

3. Full JWT Token:
   eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
   eyJ1c2VyX2lkIjogMSwgInVzZXJuYW1lIjogImFkbWluIn0.
   SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c

4. Client uses token in subsequent requests:
   Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

5. Gateway validates token:
   - Verifies signature using secret key
   - Checks expiration time
   - Extracts user data from payload
   - Enforces RBAC rules
```

### Role-Based Access Control (RBAC) Matrix

```
┌─────────┬─────────┬─────────┬─────────┬─────────┬──────────┐
│Endpoint │  Admin  │ Doctor  │ Patient │Manager  │  Guest   │
├─────────┼─────────┼─────────┼─────────┼─────────┼──────────┤
│ POST    │    ✓    │    ✗    │    ✗    │    ✗    │    ✗     │
│/patients├─────────┼─────────┼─────────┼─────────┼──────────┤
│ GET     │    ✓    │    ✓    │    △*   │    ✓    │    ✗     │
│/patients├─────────┼─────────┼─────────┼─────────┼──────────┤
│ PUT     │    ✓    │    ✓    │    ✗    │    ✗    │    ✗     │
│/patients├─────────┼─────────┼─────────┼─────────┼──────────┤
│ POST    │    ✓    │    ✓    │    ✗    │    ✗    │    ✗     │
│/appts   ├─────────┼─────────┼─────────┼─────────┼──────────┤
│ POST    │    ✓    │    ✗    │    ✗    │    ✓    │    ✗     │
│/bills   │         │         │         │         │          │
│ GET     │    ✓    │    ✓    │    △*   │    ✓    │    ✗     │
│/bills   └─────────┴─────────┴─────────┴─────────┴──────────┘

✓  = Full access
✗  = No access
△* = Own data only (patient can only see their own bills)
```

---

## 5. Inter-Service Communication

### Service-to-Service Communication Pattern

```
Scenario: Creating an appointment requires checking:
  - Patient exists (Patient Service)
  - Doctor exists and available (Doctor Service)

Flow:
┌──────────────────────────────────┐
│  Client Request to Gateway       │
│  POST /appointments              │
│  {patient_id: 1, doctor_id: 1}   │
└──────────────────┬───────────────┘
                   │
                   ↓
        ┌────────────────────────────┐
        │ API Gateway               │
        │ 1. Route to Appointment Svc│
        └──────────┬─────────────────┘
                   │
                   ↓
        ┌────────────────────────────┐
        │ Appointment Service        │
        │ Receives request           │
        │ Validates patient exists   │
        │ (calls Patient Service)    │
        └──────────┬─────────────────┘
                   │
            ┌──────┴──────┐
            │             │
            ↓             ↓
      ┌──────────┐  ┌──────────┐
      │Patient   │  │Doctor    │
      │Service   │  │Service   │
      └─────┬────┘  └────┬─────┘
            │             │
    ✓Patient│             │Doctor✓
    found   │             │available
            │             │
            └──────┬──────┘
                   │
                   ↓
    ┌──────────────────────────────┐
    │ Create appointment record    │
    │ Return appointment details   │
    └──────────┬───────────────────┘
               │
               ↓
    ┌──────────────────────────────┐
    │ API Gateway                  │
    │ Returns response to client   │
    └──────────────────────────────┘
```

### Communication Protocol
- **Method:** HTTP/REST
- **Format:** JSON
- **Authentication:** JWT tokens passed between services
- **Error Handling:** HTTP status codes (200, 400, 401, 403, 404, 500)

---

## 6. Technology Stack

### Backend Framework
```
Framework: FastAPI (Python)
  ✓ High performance ASGI framework
  ✓ Automatic API documentation (Swagger UI)
  ✓ Built-in data validation (Pydantic)
  ✓ Asynchronous request handling
  ✓ Type hints for better IDE support
```

### Security Libraries
```
PyJWT (2.8.1)      → Token creation and validation
python-jose         → Cryptographic operations
passlib (1.7.4)    → Password hashing
bcrypt (4.1.2)     → Bcrypt password algorithm
```

### Server
```
Uvicorn (0.30.6)   → ASGI application server
  ✓ Production-ready
  ✓ Supports multiple workers
  ✓ Hot reload for development
```

### Data Validation
```
Pydantic (2.9.2)   → Data schema validation
  ✓ Type checking
  ✓ JSON serialization
  ✓ Error messages
```

---

## 7. Deployment Architecture

### Development Environment
```
Single Machine Running Multiple Instances:
┌─────────────────────────────────────────────┐
│            Localhost (127.0.0.1)            │
│                                              │
│  Gateway:8000  ← Uvicorn Process 1         │
│  Patients:8001 ← Uvicorn Process 2         │
│  Doctors:8002  ← Uvicorn Process 3         │
│  Appts:8003    ← Uvicorn Process 4         │
│  Pharmacy:8004 ← Uvicorn Process 5         │
│  Bills:8005    ← Uvicorn Process 6         │
│  Lab:8006      ← Uvicorn Process 7         │
│                                              │
└─────────────────────────────────────────────┘
```

### Production Considerations

For production deployment:
1. **Containerization:** Docker containers for each service
2. **Orchestration:** Kubernetes cluster management
3. **Load Balancing:** Multiple instances per service
4. **Service Mesh:** Istio for advanced networking
5. **Monitoring:** Prometheus for metrics, Grafana for visualization
6. **Logging:** Centralized logging with ELK stack
7. **Database:** Persistent storage for each service (database per service pattern)

---

## 8. Scalability & Future Improvements

### Current Capabilities
- ✅ Horizontal scalability (add more instances)
- ✅ Service independence
- ✅ API Gateway as single entry point
- ✅ Stateless services

### Recommended Future Improvements
1. **Caching Layer** — Redis for session and data caching
2. **Message Queue** — RabbitMQ/Kafka for asynchronous operations
3. **Database per Service** — Separate databases instead of shared
4. **Circuit Breaker** — Handle service failures gracefully
5. **Service Mesh** — Advanced traffic management with Istio
6. **Distributed Tracing** — Jaeger for request tracking
7. **API Versioning** — Support multiple API versions
8. **Rate Limiting** — Prevent abuse with request throttling

---

## 9. Summary

The Hospital Microservices Architecture demonstrates modern software engineering practices:

| Aspect | Benefit | Implementation |
|---|---|---|
| **Modularity** | Easy to understand and maintain | Separate service per business domain |
| **Scalability** | Handle growth independently | Add instances per service |
| **Reliability** | Failures don't cascade | Isolated service failures |
| **Team Productivity** | Parallel development | Each team owns one service |
| **Technology Freedom** | Choose best tools per need | Different tech per service if needed |
| **Deployment Flexibility** | Update services independently | No big coupling between services |

This architecture provides the foundation for a production-grade healthcare system.

---

**Document Version:** 1.0  
**Last Updated:** March 30, 2026  
**Next Review:** After production deployment
