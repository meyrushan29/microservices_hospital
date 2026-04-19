from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

app = FastAPI(
    title="Patient Service",
    description="Microservice for managing hospital patients",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# In-memory database
patients_db = {
    1: {"id": 1, "name": "Arun Kumar", "age": 35, "gender": "Male", "blood_type": "O+", "phone": "0771234567", "address": "Colombo 03", "admitted_date": "2026-03-01"},
    2: {"id": 2, "name": "Priya Nair", "age": 28, "gender": "Female", "blood_type": "A+", "phone": "0777654321", "address": "Kandy", "admitted_date": "2026-03-10"},
}
next_id = 3

class PatientCreate(BaseModel):
    name: str
    age: int
    gender: str
    blood_type: str
    phone: str
    address: str
    admitted_date: str

class Patient(PatientCreate):
    id: int

@app.get("/", tags=["Health"])
def health():
    return {"service": "Patient Service", "status": "running", "port": 8001}

@app.get("/patients", response_model=List[dict], tags=["Patients"])
def get_all_patients():
    """Get all patients in the hospital"""
    return list(patients_db.values())

@app.get("/patients/{patient_id}", tags=["Patients"])
def get_patient(patient_id: int):
    """Get a specific patient by ID"""
    if patient_id not in patients_db:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patients_db[patient_id]

@app.post("/patients", tags=["Patients"])
def create_patient(patient: PatientCreate):
    """Register a new patient"""
    global next_id
    new_patient = {"id": next_id, **patient.dict()}
    patients_db[next_id] = new_patient
    next_id += 1
    return {"message": "Patient registered successfully", "patient": new_patient}

@app.put("/patients/{patient_id}", tags=["Patients"])
def update_patient(patient_id: int, patient: PatientCreate):
    """Update patient details"""
    if patient_id not in patients_db:
        raise HTTPException(status_code=404, detail="Patient not found")
    patients_db[patient_id] = {"id": patient_id, **patient.dict()}
    return {"message": "Patient updated successfully", "patient": patients_db[patient_id]}

@app.delete("/patients/{patient_id}", tags=["Patients"])
def delete_patient(patient_id: int):
    """Discharge/remove a patient"""
    if patient_id not in patients_db:
        raise HTTPException(status_code=404, detail="Patient not found")
    del patients_db[patient_id]
    return {"message": f"Patient {patient_id} discharged successfully"}
