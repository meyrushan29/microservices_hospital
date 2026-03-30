# 🏥 Hospital Management System — Microservices Architecture

## IT4020 Assignment 2 | SLIIT | 2026

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

## 🌐 Access URLs

### Direct (Native Swagger)
| Service | URL |
|---|---|
| Patient Service | http://localhost:8001/docs |
| Doctor Service | http://localhost:8002/docs |
| Appointment Service | http://localhost:8003/docs |
| Pharmacy Service | http://localhost:8004/docs |
| Billing Service | http://localhost:8005/docs |
| Lab Service | http://localhost:8006/docs |

### Via API Gateway
| Endpoint | URL |
|---|---|
| Gateway Swagger | http://localhost:8000/docs |
| Health Check | http://localhost:8000/health |
| Patients | http://localhost:8000/patients |
| Doctors | http://localhost:8000/doctors |
| Appointments | http://localhost:8000/appointments |
| Medicines | http://localhost:8000/medicines |
| Bills | http://localhost:8000/bills |
| Lab Tests | http://localhost:8000/tests |

---

## 👥 Group Members & Contributions

| Member | Service | Port |
|---|---|---|
| Meyrushan N | Patient Service | 8001 |
| Laxshika S | Doctor Service | 8002 |
| Laksopan R | Appointment Service | 8003 |
| Viththakan N | Pharmacy Service | 8004 |
| Hariyah L  | Billing Service | 8005 |
| Nilakshan V | Lab Service | 8006 |
| All | API Gateway | 8000 |
