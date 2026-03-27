from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Billing Service",
    description="Microservice for managing hospital billing and payments",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

bills_db = {
    1: {"id": 1, "patient_id": 1, "amount": 5500.00, "items": ["Consultation: 2000", "Medicine: 1500", "Lab Test: 2000"], "status": "paid", "date": "2026-03-18"},
    2: {"id": 2, "patient_id": 2, "amount": 3200.00, "items": ["Consultation: 2000", "Medicine: 1200"], "status": "pending", "date": "2026-03-19"},
}
next_id = 3

class BillCreate(BaseModel):
    patient_id: int
    amount: float
    items: list
    status: str = "pending"
    date: str

@app.get("/", tags=["Health"])
def health():
    return {"service": "Billing Service", "status": "running", "port": 8005}

@app.get("/bills", tags=["Bills"])
def get_all_bills():
    """Get all hospital bills"""
    return list(bills_db.values())

@app.get("/bills/{bill_id}", tags=["Bills"])
def get_bill(bill_id: int):
    """Get a specific bill"""
    if bill_id not in bills_db:
        raise HTTPException(status_code=404, detail="Bill not found")
    return bills_db[bill_id]

@app.get("/bills/patient/{patient_id}", tags=["Bills"])
def get_patient_bills(patient_id: int):
    """Get all bills for a specific patient"""
    return [b for b in bills_db.values() if b["patient_id"] == patient_id]

@app.post("/bills", tags=["Bills"])
def create_bill(bill: BillCreate):
    """Generate a new bill"""
    global next_id
    new_bill = {"id": next_id, **bill.dict()}
    bills_db[next_id] = new_bill
    next_id += 1
    return {"message": "Bill generated successfully", "bill": new_bill}

@app.put("/bills/{bill_id}/pay", tags=["Bills"])
def pay_bill(bill_id: int):
    """Mark a bill as paid"""
    if bill_id not in bills_db:
        raise HTTPException(status_code=404, detail="Bill not found")
    bills_db[bill_id]["status"] = "paid"
    return {"message": f"Bill {bill_id} marked as paid", "bill": bills_db[bill_id]}

@app.delete("/bills/{bill_id}", tags=["Bills"])
def delete_bill(bill_id: int):
    if bill_id not in bills_db:
        raise HTTPException(status_code=404, detail="Bill not found")
    del bills_db[bill_id]
    return {"message": f"Bill {bill_id} deleted"}
