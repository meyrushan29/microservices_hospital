# 🏥 Hospital Management System — Microservices Architecture

## IT4020 Assignment 2 | SLIIT | 2026

---

## 📁 Project Structure

```
hospital-microservices/
├── patient-service/        # Member 1 — Patient CRUD
│   └── main.py
├── doctor-service/         # Member 2 — Doctor CRUD
│   └── main.py
├── appointment-service/    # Member 3 — Appointment CRUD
│   └── main.py
├── pharmacy-service/       # Member 4 — Medicine & Prescriptions
│   └── main.py
├── billing-service/        # Member 5 — Billing & Payments
│   └── main.py
├── lab-service/            # Member 6 — Lab Tests & Results
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
| Member 1 | Patient Service | 8001 |
| Member 2 | Doctor Service | 8002 |
| Member 3 | Appointment Service | 8003 |
| Member 4 | Pharmacy Service | 8004 |
| Member 5 | Billing Service | 8005 |
| Member 6 | Lab Service | 8006 |
| All | API Gateway | 8000 |
