from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="Appointment Service",
    description="Microservice for managing hospital appointments - Standalone Component",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

appointments_db = {
    1: {"id": 1, "patient_id": 1, "doctor_id": 1, "date": "2026-03-20", "time": "10:00 AM", "reason": "Chest pain checkup", "status": "confirmed"},
    2: {"id": 2, "patient_id": 2, "doctor_id": 2, "date": "2026-03-21", "time": "2:00 PM", "reason": "Headache consultation", "status": "pending"},
}
next_id = 3

class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    date: str
    time: str
    reason: str
    status: str = "pending"

@app.get("/", tags=["Health"])
def health():
    return {"service": "Appointment Service", "status": "running", "port": 8003, "standalone": True}

@app.get("/appointments", tags=["Appointments"])
def get_all_appointments():
    """Get all appointments"""
    return list(appointments_db.values())

@app.get("/appointments/{appointment_id}", tags=["Appointments"])
def get_appointment(appointment_id: int):
    """Get a specific appointment"""
    if appointment_id not in appointments_db:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointments_db[appointment_id]

@app.get("/appointments/patient/{patient_id}", tags=["Appointments"])
def get_appointments_by_patient(patient_id: int):
    """Get all appointments for a patient"""
    return [a for a in appointments_db.values() if a["patient_id"] == patient_id]

@app.post("/appointments", tags=["Appointments"])
def create_appointment(appointment: AppointmentCreate):
    """Book a new appointment"""
    global next_id
    new_appt = {"id": next_id, **appointment.dict()}
    appointments_db[next_id] = new_appt
    next_id += 1
    return {"message": "Appointment booked successfully", "appointment": new_appt}

@app.put("/appointments/{appointment_id}/status", tags=["Appointments"])
def update_status(appointment_id: int, status: str):
    """Update appointment status (confirmed/cancelled/completed)"""
    if appointment_id not in appointments_db:
        raise HTTPException(status_code=404, detail="Appointment not found")
    appointments_db[appointment_id]["status"] = status
    return {"message": "Status updated", "appointment": appointments_db[appointment_id]}

@app.delete("/appointments/{appointment_id}", tags=["Appointments"])
def cancel_appointment(appointment_id: int):
    """Cancel an appointment"""
    if appointment_id not in appointments_db:
        raise HTTPException(status_code=404, detail="Appointment not found")
    del appointments_db[appointment_id]
    return {"message": f"Appointment {appointment_id} cancelled"}
