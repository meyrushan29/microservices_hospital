from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import httpx

app = FastAPI(
    title="Hospital API Gateway",
    description="""
    ## API Gateway for Hospital Management System
    
    This gateway routes all requests to the appropriate microservices.
    
    ### Available Services
    | Service | Gateway Path | Direct Port |
    |---|---|---|
    | Patient Service | /patients/** | :8001 |
    | Doctor Service | /doctors/** | :8002 |
    | Appointment Service | /appointments/** | :8003 |
    | Pharmacy Service | /pharmacy/** | :8004 |
    | Billing Service | /billing/** | :8005 |
    | Lab Service | /lab/** | :8006 |
    """,
    version="1.0.0",
)

# Service registry - maps gateway paths to microservice URLs
SERVICE_REGISTRY = {
    "patients":     "http://localhost:8001",
    "doctors":      "http://localhost:8002",
    "appointments": "http://localhost:8003",
    "medicines":    "http://localhost:8004",
    "prescriptions":"http://localhost:8004",
    "bills":        "http://localhost:8005",
    "tests":        "http://localhost:8006",
}

@app.get("/", tags=["Gateway"])
def gateway_info():
    return {
        "service": "Hospital API Gateway",
        "status": "running",
        "port": 8000,
        "routes": {
            "/patients/**":     "Patient Service     → localhost:8001",
            "/doctors/**":      "Doctor Service      → localhost:8002",
            "/appointments/**": "Appointment Service → localhost:8003",
            "/medicines/**":    "Pharmacy Service    → localhost:8004",
            "/bills/**":        "Billing Service     → localhost:8005",
            "/tests/**":        "Lab Service         → localhost:8006",
        }
    }

@app.get("/health", tags=["Gateway"])
async def health_check():
    """Check health of all microservices"""
    results = {}
    async with httpx.AsyncClient(timeout=3.0) as client:
        for name, url in [
            ("patient-service",     "http://localhost:8001"),
            ("doctor-service",      "http://localhost:8002"),
            ("appointment-service", "http://localhost:8003"),
            ("pharmacy-service",    "http://localhost:8004"),
            ("billing-service",     "http://localhost:8005"),
            ("lab-service",         "http://localhost:8006"),
        ]:
            try:
                r = await client.get(f"{url}/")
                results[name] = "✅ running"
            except Exception:
                results[name] = "❌ unreachable"
    return {"gateway": "running", "services": results}

async def forward_request(request: Request, service_url: str, path: str):
    """Forward a request to the target microservice"""
    url = f"{service_url}/{path}"
    if request.url.query:
        url += f"?{request.url.query}"
    
    body = await request.body()
    headers = {k: v for k, v in request.headers.items() if k.lower() not in ("host", "content-length")}

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.request(
                method=request.method,
                url=url,
                content=body,
                headers=headers,
            )
            return JSONResponse(content=response.json(), status_code=response.status_code)
        except httpx.ConnectError:
            raise HTTPException(status_code=503, detail=f"Service at {service_url} is unavailable")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

# ── Patient routes ──────────────────────────────────────────
@app.get("/patients", tags=["Patient Service"])
@app.get("/patients/{path:path}", tags=["Patient Service"])
async def patient_get(request: Request, path: str = ""):
    return await forward_request(request, "http://localhost:8001", f"patients/{path}".rstrip("/"))

@app.post("/patients", tags=["Patient Service"])
async def patient_post(request: Request):
    return await forward_request(request, "http://localhost:8001", "patients")

@app.put("/patients/{path:path}", tags=["Patient Service"])
async def patient_put(request: Request, path: str):
    return await forward_request(request, "http://localhost:8001", f"patients/{path}")

@app.delete("/patients/{path:path}", tags=["Patient Service"])
async def patient_delete(request: Request, path: str):
    return await forward_request(request, "http://localhost:8001", f"patients/{path}")

# ── Doctor routes ───────────────────────────────────────────
@app.get("/doctors", tags=["Doctor Service"])
@app.get("/doctors/{path:path}", tags=["Doctor Service"])
async def doctor_get(request: Request, path: str = ""):
    return await forward_request(request, "http://localhost:8002", f"doctors/{path}".rstrip("/"))

@app.post("/doctors", tags=["Doctor Service"])
async def doctor_post(request: Request):
    return await forward_request(request, "http://localhost:8002", "doctors")

@app.put("/doctors/{path:path}", tags=["Doctor Service"])
async def doctor_put(request: Request, path: str):
    return await forward_request(request, "http://localhost:8002", f"doctors/{path}")

@app.delete("/doctors/{path:path}", tags=["Doctor Service"])
async def doctor_delete(request: Request, path: str):
    return await forward_request(request, "http://localhost:8002", f"doctors/{path}")

# ── Appointment routes ──────────────────────────────────────
@app.get("/appointments", tags=["Appointment Service"])
@app.get("/appointments/{path:path}", tags=["Appointment Service"])
async def appt_get(request: Request, path: str = ""):
    return await forward_request(request, "http://localhost:8003", f"appointments/{path}".rstrip("/"))

@app.post("/appointments", tags=["Appointment Service"])
async def appt_post(request: Request):
    return await forward_request(request, "http://localhost:8003", "appointments")

@app.put("/appointments/{path:path}", tags=["Appointment Service"])
async def appt_put(request: Request, path: str):
    return await forward_request(request, "http://localhost:8003", f"appointments/{path}")

@app.delete("/appointments/{path:path}", tags=["Appointment Service"])
async def appt_delete(request: Request, path: str):
    return await forward_request(request, "http://localhost:8003", f"appointments/{path}")

# ── Pharmacy routes ─────────────────────────────────────────
@app.get("/medicines", tags=["Pharmacy Service"])
@app.get("/medicines/{path:path}", tags=["Pharmacy Service"])
async def med_get(request: Request, path: str = ""):
    return await forward_request(request, "http://localhost:8004", f"medicines/{path}".rstrip("/"))

@app.post("/medicines", tags=["Pharmacy Service"])
async def med_post(request: Request):
    return await forward_request(request, "http://localhost:8004", "medicines")

@app.get("/prescriptions", tags=["Pharmacy Service"])
@app.get("/prescriptions/{path:path}", tags=["Pharmacy Service"])
async def pres_get(request: Request, path: str = ""):
    return await forward_request(request, "http://localhost:8004", f"prescriptions/{path}".rstrip("/"))

@app.post("/prescriptions", tags=["Pharmacy Service"])
async def pres_post(request: Request):
    return await forward_request(request, "http://localhost:8004", "prescriptions")

# ── Billing routes ──────────────────────────────────────────
@app.get("/bills", tags=["Billing Service"])
@app.get("/bills/{path:path}", tags=["Billing Service"])
async def bill_get(request: Request, path: str = ""):
    return await forward_request(request, "http://localhost:8005", f"bills/{path}".rstrip("/"))

@app.post("/bills", tags=["Billing Service"])
async def bill_post(request: Request):
    return await forward_request(request, "http://localhost:8005", "bills")

@app.put("/bills/{path:path}", tags=["Billing Service"])
async def bill_put(request: Request, path: str):
    return await forward_request(request, "http://localhost:8005", f"bills/{path}")

@app.delete("/bills/{path:path}", tags=["Billing Service"])
async def bill_delete(request: Request, path: str):
    return await forward_request(request, "http://localhost:8005", f"bills/{path}")

# ── Lab routes ──────────────────────────────────────────────
@app.get("/tests", tags=["Lab Service"])
@app.get("/tests/{path:path}", tags=["Lab Service"])
async def lab_get(request: Request, path: str = ""):
    return await forward_request(request, "http://localhost:8006", f"tests/{path}".rstrip("/"))

@app.post("/tests", tags=["Lab Service"])
async def lab_post(request: Request):
    return await forward_request(request, "http://localhost:8006", "tests")

@app.put("/tests/{path:path}", tags=["Lab Service"])
async def lab_put(request: Request, path: str):
    return await forward_request(request, "http://localhost:8006", f"tests/{path}")

@app.delete("/tests/{path:path}", tags=["Lab Service"])
async def lab_delete(request: Request, path: str):
    return await forward_request(request, "http://localhost:8006", f"tests/{path}")
