from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Lab Service",
    description="Microservice for managing laboratory tests and results",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

tests_db = {
    1: {"id": 1, "patient_id": 1, "test_name": "Blood Count (CBC)", "ordered_by": 1, "date": "2026-03-18", "status": "completed", "result": "Normal - WBC: 7.2, RBC: 5.1, Hb: 14.2"},
    2: {"id": 2, "patient_id": 2, "test_name": "MRI Brain", "ordered_by": 2, "date": "2026-03-19", "status": "pending", "result": None},

}
next_id = 3

class LabTestCreate(BaseModel):
    patient_id: int
    test_name: str
    ordered_by: int
    date: str
    status: str = "pending"
    result: str = None

@app.get("/", tags=["Health"])
def health():
    return {"service": "Lab Service", "status": "running", "port": 8006}

@app.get("/tests", tags=["Lab Tests"])
def get_all_tests():
    """Get all lab tests"""
    return list(tests_db.values())

@app.get("/tests/{test_id}", tags=["Lab Tests"])
def get_test(test_id: int):
    """Get a specific lab test"""
    if test_id not in tests_db:
        raise HTTPException(status_code=404, detail="Lab test not found")
    return tests_db[test_id]

@app.get("/tests/patient/{patient_id}", tags=["Lab Tests"])
def get_tests_by_patient(patient_id: int):
    """Get all lab tests for a patient"""
    return [t for t in tests_db.values() if t["patient_id"] == patient_id]

@app.post("/tests", tags=["Lab Tests"])
def create_test(test: LabTestCreate):
    """Order a new lab test"""
    global next_id
    new_test = {"id": next_id, **test.dict()}
    tests_db[next_id] = new_test
    next_id += 1
    return {"message": "Lab test ordered successfully", "test": new_test}

@app.put("/tests/{test_id}/result", tags=["Lab Tests"])
def update_result(test_id: int, result: str):
    """Update lab test result"""
    if test_id not in tests_db:
        raise HTTPException(status_code=404, detail="Lab test not found")
    tests_db[test_id]["result"] = result
    tests_db[test_id]["status"] = "completed"
    return {"message": "Result updated", "test": tests_db[test_id]}

@app.delete("/tests/{test_id}", tags=["Lab Tests"])
def delete_test(test_id: int):
    if test_id not in tests_db:
        raise HTTPException(status_code=404, detail="Lab test not found")
    del tests_db[test_id]
    return {"message": f"Lab test {test_id} deleted"}
