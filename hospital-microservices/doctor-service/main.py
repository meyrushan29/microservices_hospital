from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="Doctor Service",
    description="Microservice for managing hospital doctors",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

doctors_db = {
    1: {"id": 1, "name": "Dr. Suresh Perera", "specialization": "Cardiology", "phone": "0112345678", "available": True, "experience_years": 15},
    2: {"id": 2, "name": "Dr. Meena Rajah", "specialization": "Neurology", "phone": "0119876543", "available": True, "experience_years": 10},
    3: {"id": 3, "name": "Dr. Kamal Silva", "specialization": "Orthopedics", "phone": "0115551234", "available": False, "experience_years": 8},
}
next_id = 4

class DoctorCreate(BaseModel):
    name: str
    specialization: str
    phone: str
    available: bool
    experience_years: int


@app.get("/", tags=["Health"])
def health():
    return {"service": "Doctor Service", "status": "running", "port": 8002}

@app.get("/doctors", tags=["Doctors"])
def get_all_doctors():
    """Get all doctors"""
    return list(doctors_db.values())

@app.get("/doctors/available", tags=["Doctors"])
def get_available_doctors():
    """Get all currently available doctors"""
    return [d for d in doctors_db.values() if d["available"]]

@app.get("/doctors/{doctor_id}", tags=["Doctors"])
def get_doctor(doctor_id: int):
    """Get a specific doctor by ID"""
    if doctor_id not in doctors_db:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctors_db[doctor_id]

@app.post("/doctors", tags=["Doctors"])
def create_doctor(doctor: DoctorCreate):
    """Add a new doctor"""
    global next_id
    new_doctor = {"id": next_id, **doctor.dict()}
    doctors_db[next_id] = new_doctor
    next_id += 1
    return {"message": "Doctor added successfully", "doctor": new_doctor}


@app.put("/doctors/{doctor_id}", tags=["Doctors"])
def update_doctor(doctor_id: int, doctor: DoctorCreate):
    """Update doctor details"""
    if doctor_id not in doctors_db:
        raise HTTPException(status_code=404, detail="Doctor not found")
    doctors_db[doctor_id] = {"id": doctor_id, **doctor.dict()}
    return {"message": "Doctor updated", "doctor": doctors_db[doctor_id]}

@app.delete("/doctors/{doctor_id}", tags=["Doctors"])
def delete_doctor(doctor_id: int):
    """Remove a doctor"""
    if doctor_id not in doctors_db:
        raise HTTPException(status_code=404, detail="Doctor not found")
    del doctors_db[doctor_id]
    return {"message": f"Doctor {doctor_id} removed successfully"}
