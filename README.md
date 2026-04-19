# Appointment Service - Hospital Microservices

This is a standalone microservice component for managing hospital appointments.

## Description

The Appointment Service handles:
- Appointment scheduling
- Appointment status management
- Patient appointment history
- Doctor availability tracking

## Technology Stack

- FastAPI (0.115.0)
- Uvicorn (0.30.6)
- Pydantic (2.9.2)

## Running the Service

### Using Python directly:
```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8003
```

### Using the start script:

**Windows:**
```powershell
.\start.ps1
```

**Linux/macOS:**
```bash
bash start.sh
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/appointments` | Get all appointments |
| GET | `/appointments/{id}` | Get appointment by ID |
| GET | `/appointments/patient/{patient_id}` | Get appointments by patient |
| POST | `/appointments` | Create new appointment |
| PUT | `/appointments/{id}/status` | Update appointment status |
| DELETE | `/appointments/{id}` | Cancel appointment |

## Default Port

This service runs on port **8003**.

## Integration

This service can be used in two ways:
1. **Standalone** - Run directly on port 8003
2. **Via API Gateway** - Routes through the API Gateway on port 8000

---

**Developer:** Laksopan R  
**Part of:** Hospital Management System - MTIT Assignment