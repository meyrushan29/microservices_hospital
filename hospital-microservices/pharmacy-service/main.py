from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Pharmacy Service",
    description="Microservice for managing medicines and prescriptions",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

medicines_db = {
    1: {"id": 1, "name": "Paracetamol", "stock": 500, "price": 5.00, "category": "Painkiller"},
    2: {"id": 2, "name": "Amoxicillin", "stock": 200, "price": 25.00, "category": "Antibiotic"},
    3: {"id": 3, "name": "Metformin", "stock": 300, "price": 15.00, "category": "Diabetes"},
}
prescriptions_db = {
    1: {"id": 1, "patient_id": 1, "doctor_id": 1, "medicines": ["Paracetamol", "Amoxicillin"], "date": "2026-03-18", "status": "dispensed"},
}
next_med_id = 4
next_pres_id = 2

class MedicineCreate(BaseModel):
    name: str
    stock: int
    price: float
    category: str

class PrescriptionCreate(BaseModel):
    patient_id: int
    doctor_id: int
    medicines: list
    date: str
    status: str = "pending"

@app.get("/", tags=["Health"])
def health():
    return {"service": "Pharmacy Service", "status": "running", "port": 8004}

@app.get("/medicines", tags=["Medicines"])
def get_all_medicines():
    """Get all medicines in stock"""
    return list(medicines_db.values())

@app.get("/medicines/{medicine_id}", tags=["Medicines"])
def get_medicine(medicine_id: int):
    if medicine_id not in medicines_db:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return medicines_db[medicine_id]

@app.post("/medicines", tags=["Medicines"])
def add_medicine(medicine: MedicineCreate):
    """Add a new medicine to inventory"""
    global next_med_id
    new_med = {"id": next_med_id, **medicine.dict()}
    medicines_db[next_med_id] = new_med
    next_med_id += 1
    return {"message": "Medicine added", "medicine": new_med}

@app.get("/prescriptions", tags=["Prescriptions"])
def get_all_prescriptions():
    """Get all prescriptions"""
    return list(prescriptions_db.values())

@app.post("/prescriptions", tags=["Prescriptions"])
def create_prescription(prescription: PrescriptionCreate):
    """Create a new prescription"""
    global next_pres_id
    new_pres = {"id": next_pres_id, **prescription.dict()}
    prescriptions_db[next_pres_id] = new_pres
    next_pres_id += 1
    return {"message": "Prescription created", "prescription": new_pres}

@app.delete("/medicines/{medicine_id}", tags=["Medicines"])
def delete_medicine(medicine_id: int):
    if medicine_id not in medicines_db:
        raise HTTPException(status_code=404, detail="Medicine not found")
    del medicines_db[medicine_id]
    return {"message": f"Medicine {medicine_id} removed"}
