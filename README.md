# 🏥 Hospital Management System — Microservices Architecture

## IT4020 Assignment 2 | SLIIT | 2026

---

## 📋 Assignment Overview

This project implements a **microservices-based backend** for a Hospital Management System using modern architectural patterns and best practices.

### Business Domain: Healthcare Management
**Real-World Scenario:** Hospital operations management requires handling multiple independent business functions simultaneously. The Hospital Management System separates these functions into autonomous microservices that communicate through a centralized API Gateway, enabling scalability, maintainability, and independent deployment.

### Why Microservices for Healthcare?
- **Patient Privacy:** Isolate sensitive patient data in dedicated service
- **Scalability:** High-traffic services (appointments) can scale independently  
- **Resilience:** Outage in one service doesn't crash entire system
- **Team Autonomy:** Each team owns and develops their microservice independently
- **Technology Flexibility:** Each service can use different databases or languages

---

## 📁 Project Structure

```
hospital-microservices/
├── patient-service/        # Meyrushan N — Patient CRUD
│   └── main.py
├── doctor-service/         # Laxshika S — Doctor CRUD
│   └── main.py
├── appointment-service/    # Laksopan R — Appointment CRUD
│   └── main.py
├── pharmacy-service/       # Viththakan N — Medicine & Prescriptions
│   └── main.py
├── billing-service/        # Hariyah L — Billing & Payments
│   └── main.py
├── lab-service/            # Nilakshan V — Lab Tests & Results
│   └── main.py
├── api-gateway/            # API Gateway (routes all traffic)
│   └── main.py
├── requirements.txt
├── start_all.sh
└── README.md
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.9+
- pip (Python package manager)

### Installation Steps

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Start all services (from project root)
# On Linux/macOS:
bash start_all.sh

# On Windows PowerShell:
.\start_all.ps1
```

### Dependencies Overview

The system uses modern security and microservices libraries:

| Package | Version | Purpose |
|---|---|---|
| **fastapi** | 0.115.0 | Web framework for building APIs |
| **uvicorn** | 0.30.6 | ASGI server for running services |
| **pydantic** | 2.9.2 | Data validation and schema generation |
| **PyJWT** | 2.8.1 | JWT token creation & verification |
| **python-jose** | 3.3.0 | JWT & cryptographic operations |
| **passlib** | 1.7.4 | Password hashing utilities |
| **bcrypt** | 4.1.2 | Secure password hashing algorithm |
| **httpx** | 0.27.0 | HTTP client for service-to-service calls |

---

## 🔐 Security Architecture

### Overview of Security Implementation

The Hospital Management System implements **enterprise-grade security** with:

✅ **JWT Token-Based Authentication** — Stateless, secure token validation  
✅ **Role-Based Access Control (RBAC)** — Fine-grained permission management  
✅ **Bcrypt Password Hashing** — Cryptographically secure password storage  
✅ **Token Expiration & Refresh** — Automatic session management  
✅ **API Gateway Authorization** — Centralized security enforcement  

### Security Features (NEW)

This system now includes **JWT Authentication** and **Role-Based Access Control (RBAC)**.

#### How It Works

1. **User Authentication** — User submits credentials → System validates against secure password hash → JWT token issued
2. **Token Validation** — Every request includes token in Authorization header → API Gateway verifies token signature & expiration
3. **Role Verification** — Token contains user role → Endpoints check if role has permission for the action
4. **Secure Communication** — All microservices communicate through the API Gateway with token validation

#### Authentication Flow

```
User → /authenticate → API Gateway → Verify Credentials → Generate JWT → Return Token
                                           ↓
                                    [Password matched with bcrypt hash]

Subsequent Request → API Gateway → Verify JWT Signature & Expiration → Route to Service
                                           ↓
                                    [Token valid & not expired]
```

### Quick Start with Security

1. **Get JWT Token:**
   ```bash
   curl -X POST http://localhost:8000/authenticate \
     -H "Content-Type: application/json" \
     -d '{"username":"admin","password":"admin123"}'
   ```

2. **Use Token in Requests:**
   ```bash
   curl -H "Authorization: Bearer <token>" \
     http://localhost:8000/patients
   ```

### Test Users
| Username | Password | Role |
|---|---|---|
| admin | admin123 | Full access |
| doctor | doctor123 | Medical operations |
| patient | patient123 | Limited access |

### Role Permissions Summary

| Role | Capabilities |
|---|---|
| **admin** | Create/update/delete patients, doctors, medicines, bills, tests, view all data |
| **doctor** | View patients, create prescriptions, order lab tests, manage appointments |
| **patient** | View own appointment data, book appointments, view test results |

⚠️ **Important Security Notes:**
- Test users are for development only — change credentials in production
- Tokens expire after 30 minutes — request new token if expired
- All requests through API Gateway are logged and validated
- Passwords are hashed using bcrypt (salted, not reversible)

**See [SECURITY.md](./hospital-microservices/SECURITY.md) for detailed security documentation.**

---

## 🛠️ Security Troubleshooting

### Common Authentication Issues

**401 Unauthorized — "Invalid token"**
- Solution: Get a new token from `/authenticate` endpoint
- Check: Copy token correctly without extra spaces

**403 Forbidden — "Insufficient permissions"**
- Solution: Check your user role against endpoint requirements
- Example: Only admins can create new patients

**Token Expired**
- Solution: Re-authenticate to get a new token
- Tokens last 30 minutes (check SECURITY.md for renewal)

**CORS Errors**
- Solution: All requests must go through API Gateway (http://localhost:8000)
- Don't call services directly on ports 8001-8006 from browser

---

## 🧪 Testing Guide: Direct vs Gateway Access

This section demonstrates that all endpoints work both directly and via the API Gateway (fulfilling assignment requirement).

### Step 1: Authenticate to Get JWT Token

```bash
# Get token from API Gateway
curl -X POST http://localhost:8000/authenticate \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Response contains token:
# {
#   "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
#   "token_type": "bearer"
# }

# Save token for use in requests
export TOKEN="<your_access_token_here>"
```

### Step 2: Test Endpoints via API Gateway (Recommended)

#### Create a Patient (via Gateway)
```bash
curl -X POST http://localhost:8000/patients \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "age": 45,
    "gender": "Male",
    "blood_type": "O+",
    "phone": "0771234567",
    "address": "Colombo",
    "admitted_date": "2026-03-30"
  }'
```

#### Get Patients List (via Gateway)
```bash
curl -X GET http://localhost:8000/patients \
  -H "Authorization: Bearer $TOKEN"
```

#### Create a Doctor (via Gateway)
```bash
curl -X POST http://localhost:8000/doctors \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Dr. Smith",
    "specialization": "Cardiology",
    "phone": "0771111111",
    "email": "dr.smith@hospital.com"
  }'
```

#### Book an Appointment (via Gateway)
```bash
curl -X POST http://localhost:8000/appointments \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": 1,
    "doctor_id": 1,
    "date": "2026-04-15",
    "time": "2:00 PM",
    "reason": "Checkup",
    "status": "pending"
  }'
```

### Step 3: Test Same Endpoints Directly (Development Only)

#### Get Patients List (Direct from Patient Service - Port 8001)
```bash
curl -X GET http://localhost:8001/patients \
  -H "Authorization: Bearer $TOKEN"
```

#### Get Doctors List (Direct from Doctor Service - Port 8002)
```bash
curl -X GET http://localhost:8002/doctors \
  -H "Authorization: Bearer $TOKEN"
```

#### Get Appointments List (Direct from Appointment Service - Port 8003)
```bash
curl -X GET http://localhost:8003/appointments \
  -H "Authorization: Bearer $TOKEN"
```

#### Get Medicines (Direct from Pharmacy Service - Port 8004)
```bash
curl -X GET http://localhost:8004/medicines \
  -H "Authorization: Bearer $TOKEN"
```

#### Get Bills (Direct from Billing Service - Port 8005)
```bash
curl -X GET http://localhost:8005/bills \
  -H "Authorization: Bearer $TOKEN"
```

#### Get Lab Tests (Direct from Lab Service - Port 8006)
```bash
curl -X GET http://localhost:8006/tests \
  -H "Authorization: Bearer $TOKEN"
```

### Expected Results

✅ **Via API Gateway:** All endpoints at `http://localhost:8000/` work with single authentication  
✅ **Direct Access:** Individual services at `http://localhost:8001/` through `8006/` also work  
✅ **Proof:** Both approaches return the same data, demonstrating gateway routing functionality  

---

## 📊 Microservices Architecture Diagram

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       │ All requests here (single port 8000)
       ↓
┌───────────────────────────────────────────┐
│       API GATEWAY (Port 8000)              │
│  - JWT Authentication                      │
│  - Request Routing                         │
│  - RBAC Enforcement                        │
└─┬──────┬──────┬──────┬──────┬──────┬──────┘
  │      │      │      │      │      │
  ↓      ↓      ↓      ↓      ↓      ↓
┌──────┐┌──────┐┌──────┐┌──────┐┌──────┐┌──────┐
│Pat.  ││Doc.  ││Appt. ││Pharm.││Bill. ││Lab   │
│Svc.  ││Svc.  ││Svc.  ││Svc.  ││Svc.  ││Svc.  │
│:8001 ││:8002 ││:8003 ││:8004 ││:8005 ││:8006 │
└──────┘└──────┘└──────┘└──────┘└──────┘└──────┘
```

---

## ✅ Assignment Fulfillment Checklist

### Required Deliverables

- [x] **Business Domain Definition** — Hospital Management System with clear real-world scenario
- [x] **Microservices Identification** — 6 microservices defined with individual member assignments
- [x] **API Gateway Implementation** — Single entry point (port 8000) handling all routing and authentication
- [x] **Folder Structure** — Organized microservices directory with separate main.py files
- [x] **Security Implementation** — JWT Authentication and RBAC with role-based permissions
- [x] **Testing Documentation** — Instructions for testing both direct and gateway access
- [x] **Individual Contributions** — Each member assigned specific microservice with clear responsibilities
- [x] **No Build Breaks** — All services start successfully via start_all.sh or start_all.ps1
- [x] **Dual Access** — Endpoints accessible both directly and via gateway

### For Slide Deck Preparation

**Content to Include:**

1. **Title Slide** — Group name, course (IT4020), assignment number, university (SLIIT)

2. **Business Domain Slide**
   - Real-world scenario: Hospital operations management
   - Why microservices helps (scalability, resilience, team autonomy)

3. **System Architecture Slide**
   - Include the diagram above
   - Show how API Gateway centralizes requests

4. **Individual Microservices Slide** (detailed)
   - Member name → Service name → Key responsibilities → Example endpoints
   - Create for each of the 6 services

5. **API Gateway Importance Slide**
   - Problem: Multiple ports (8001-8006)
   - Solution: Single entry point (8000)
   - Benefits: Authentication, routing, load balancing

6. **Live Demo Screenshots** (MOST IMPORTANT)
   - Screenshot of: `curl` command request to `/patients` via API Gateway
   - Screenshot of: Response from API Gateway
   - Screenshot of: Same curl command directly to patient service (port 8001)
   - Screenshot of: Response from direct service
   - Repeat for 2-3 services to show both work

7. **Security Implementation Slide**
   - JWT token authentication flow
   - Role-based access control matrix
   - Test users and permissions

8. **Team Contributions Slide**
   - Clear breakdown of who worked on what
   - Microservices owned by each member

9. **Conclusion Slide**
   - Key learnings about microservices
   - API Gateway role in enterprise architecture

**How to Capture Screenshots:**

1. Open PowerShell/Terminal showing startup commands
2. Open second terminal showing curl requests
3. Show both gateway access and direct service access
4. Include Swagger UI screenshots from both gateway and services
5. Paste both into PowerPoint slide deck

---

## 🌐 API Gateway: Access URLs & Routing

### How the API Gateway Avoids Multiple Ports

**Problem:** Without a gateway, clients must manage 6 different service URLs and ports, making integrations complex.

**Solution:** All requests go through a single entry point (Port 8000) that intelligently routes to the correct microservice.

```
Client Request → API Gateway (8000)
                    ↓
            Route Analysis & Auth
                    ↓
    ┌───────────────┬───────────────┬───────────────┐
    ↓               ↓               ↓               ↓
Patient (8001)  Doctor (8002)  Billng (8005)  Lab (8006)
```

### API Gateway Benefits (from Assignment Perspective)

| Benefit | Impact |
|---|---|
| **Single Entry Point** | Clients only need to know one URL: `http://localhost:8000` |
| **Centralized Authentication** | JWT tokens validated once at gateway, not in each service |
| **Request Routing** | Gateway automatically routes `/patients` → Patient Service (8001) |
| **Load Balancing** | Can distribute requests across multiple instances of a service |
| **Cross-Cutting Concerns** | Logging, rate limiting, CORS handled at gateway level |
| **Service Discovery** | Clients don't need to know individual service locations |
| **API Versioning** | Can route `/v1/patients` and `/v2/patients` to different implementations |

### Access URLs

#### ✅ Unified Access (Via API Gateway - RECOMMENDED)
| Resource | Gateway URL |
|---|---|
| Gateway Documentation | http://localhost:8000/docs |
| Health Check | http://localhost:8000/health |
| Patients | http://localhost:8000/patients |
| Doctors | http://localhost:8000/doctors |
| Appointments | http://localhost:8000/appointments |
| Medicines | http://localhost:8000/medicines |
| Bills | http://localhost:8000/bills |
| Lab Tests | http://localhost:8000/tests |

#### 🔧 Direct Access (For Development Only - Not Recommended for Production)
| Service | Native URL |
|---|---|
| Patient Service | http://localhost:8001/docs |
| Doctor Service | http://localhost:8002/docs |
| Appointment Service | http://localhost:8003/docs |
| Pharmacy Service | http://localhost:8004/docs |
| Billing Service | http://localhost:8005/docs |
| Lab Service | http://localhost:8006/docs |

---

## 👥 Group Members & Individual Microservice Contributions

| Member Name | Assigned Service | Port | Responsibilities | Key Endpoints |
|---|---|---|---|---|
| **Meyrushan N** | Patient Service | 8001 | Patient registration, profile management, admission records | `POST /patients`, `GET /patients/{id}`, `PUT /patients/{id}` |
| **Laxshika S** | Doctor Service | 8002 | Doctor registration, specialization management, availability | `POST /doctors`, `GET /doctors`, `PUT /doctors/{id}` |
| **Laksopan R** | Appointment Service | 8003 | Schedule management, appointment booking, status tracking | `POST /appointments`, `GET /appointments`, `PUT /appointments/{id}` |
| **Viththakan N** | Pharmacy Service | 8004 | Medicine inventory, prescription processing, stock management | `GET /medicines`, `POST /prescriptions`, `PUT /medicines/{id}` |
| **Hariyah L** | Billing Service | 8005 | Invoice generation, payment processing, billing reports | `POST /bills`, `GET /bills/{id}`, `PUT /bills/{id}/payment` |
| **Nilakshan V** | Lab Service | 8006 | Lab test orders, result management, test scheduling | `POST /tests`, `GET /test-results`, `PUT /tests/{id}` |
| **All Members** | API Gateway | 8000 | Route requests, handle authentication, enforce RBAC | All `/` endpoints route here |

---

## 📚 Complete Documentation Suite

This project includes comprehensive documentation to support the assignment requirements and production implementation:

### 📖 Core Documentation
- **[ARCHITECTURE.md](./hospital-microservices/ARCHITECTURE.md)** — Detailed system design, service specifications, gateway architecture, and technical diagrams
- **[SECURITY.md](./hospital-microservices/SECURITY.md)** — Complete security implementation guide with JWT flow, RBAC matrix, and real-world examples
- **[SECURITY-QUICK-REFERENCE.md](./hospital-microservices/SECURITY-QUICK-REFERENCE.md)** — Quick security reference for developers

### 📋 Assignment-Specific Documentation
- **[TESTING.md](./hospital-microservices/TESTING.md)** — Comprehensive testing guide with 40+ test cases proving endpoints work via **gateway AND directly**
- **[ASSIGNMENT.md](./hospital-microservices/ASSIGNMENT.md)** — Complete assignment requirements fulfillment checklist and slide deck preparation guide

### 🎯 Quick Links by Use Case

| I need to... | Read this |
|---|---|
| Get started quickly | [Setup & Installation](#-setup--installation) above |
| Learn system architecture | [ARCHITECTURE.md](./hospital-microservices/ARCHITECTURE.md) |
| Understand security | [SECURITY.md](./hospital-microservices/SECURITY.md) or [Quick Ref](./hospital-microservices/SECURITY-QUICK-REFERENCE.md) |
| Test all features | [TESTING.md](./hospital-microservices/TESTING.md) |
| Prepare assignment | [ASSIGNMENT.md](./hospital-microservices/ASSIGNMENT.md) |
| Prepare slide deck | [ASSIGNMENT.md Checklist](./hospital-microservices/ASSIGNMENT.md#-assignment-submission-checklist) |
| See what tests to run | [TESTING.md - Complete Testing](./hospital-microservices/TESTING.md#-testing-guide-direct-vs-gateway-access) |

---
