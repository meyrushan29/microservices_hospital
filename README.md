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

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Start all services (from project root)
bash start_all.sh
```
# 2. Start all services (from project root)
.\start_all.ps1

---

## 🔐 Security Features (NEW)

This system now includes **JWT Authentication** and **Role-Based Access Control (RBAC)**.

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

**See [SECURITY.md](./hospital-microservices/SECURITY.md) for detailed security documentation.**
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
