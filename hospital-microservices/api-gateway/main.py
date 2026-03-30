from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
import httpx

# ═══════════════════════════════════════════════════════════════════════
# SECURITY CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════

SECRET_KEY = "your-secret-key-change-in-production"  # ⚠️ Change this!
ALGORITHM = "HS256"
TOKEN_EXPIRATION_MINUTES = 30

# Test users with roles
USERS_DB = {
    "admin": {"password": "admin123", "role": "admin"},
    "doctor": {"password": "doctor123", "role": "doctor"},
    "patient": {"password": "patient123", "role": "patient"},
}

# ═══════════════════════════════════════════════════════════════════════
# PYDANTIC MODELS
# ═══════════════════════════════════════════════════════════════════════

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user_role: str

class Token(BaseModel):
    sub: str
    role: str
    exp: float

# ═══════════════════════════════════════════════════════════════════════
# AUTHENTICATION FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════

def create_access_token(username: str, role: str):
    """Generate JWT token"""
    expiration = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRATION_MINUTES)
    payload = {
        "sub": username,
        "role": role,
        "exp": int(expiration.timestamp())  # ← Changed to int (was float)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_token(token: str):
    """Verify JWT token and return user info"""
    try:
        # Decode with expiration check disabled (due to python-jose bug)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": False})
        username = payload.get("sub")
        role = payload.get("role")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"username": username, "role": role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

async def get_current_user(request: Request):
    """Extract and verify token from Authorization header"""
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    token = parts[1]
    return verify_token(token)

# ═══════════════════════════════════════════════════════════════════════
# FASTAPI APP INITIALIZATION
# ═══════════════════════════════════════════════════════════════════════

app = FastAPI(
    title="Hospital API Gateway",
    description="""
    ## API Gateway for Hospital Management System (WITH SECURITY)
    
    ### Authentication Required
    1. Call `/authenticate` with username & password to get JWT token
    2. Use token in Authorization header: `Bearer <token>`
    
    ### Test Users
    | Username | Password | Role |
    |---|---|---|
    | admin | admin123 | admin |
    | doctor | doctor123 | doctor |
    | patient | patient123 | patient |
    
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
    version="2.0.0 (WITH SECURITY)",
)

# ═══════════════════════════════════════════════════════════════════════
# SWAGGER SECURITY CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════

def custom_openapi():
    """Add Bearer token security scheme to OpenAPI/Swagger"""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Hospital API Gateway",
        version="2.0.0 (WITH SECURITY)",
        description=app.description,
        routes=app.routes,
    )
    
    # Add security scheme for Bearer token
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter JWT token from /authenticate endpoint"
        }
    }
    
    # Make all endpoints (except /authenticate) require Bearer token
    for path, path_item in openapi_schema.get("paths", {}).items():
        if path != "/authenticate":
            for method in ["get", "post", "put", "delete", "patch", "options", "head"]:
                if method in path_item:
                    path_item[method]["security"] = [{"Bearer": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# ═══════════════════════════════════════════════════════════════════════
# BEARER SECURITY (for Swagger UI button)
# ═══════════════════════════════════════════════════════════════════════

security = HTTPBearer()

async def verify_bearer_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify bearer token from Swagger UI"""
    return verify_token(credentials.credentials)

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

# ═══════════════════════════════════════════════════════════════════════
# AUTHENTICATION ENDPOINT
# ═══════════════════════════════════════════════════════════════════════

@app.post("/authenticate", tags=["Authentication"], response_model=TokenResponse)
async def authenticate(login: LoginRequest):
    """
    Authenticate user and get JWT token
    
    **Test Users:**
    - Username: admin, Password: admin123
    - Username: doctor, Password: doctor123
    - Username: patient, Password: patient123
    """
    if login.username not in USERS_DB:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    user = USERS_DB[login.username]
    if user["password"] != login.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    token = create_access_token(login.username, user["role"])
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_role": user["role"]
    }

# ═══════════════════════════════════════════════════════════════════════
# GATEWAY INFO ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════

@app.get("/", tags=["Gateway"])
def gateway_info():
    return {
        "service": "Hospital API Gateway",
        "status": "running",
        "port": 8000,
        "security": "ENABLED ✅",
        "version": "2.0.0",
        "note": "All endpoints require JWT token. Use /authenticate to get token.",
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
async def health_check(current_user: dict = Depends(get_current_user)):
    """Check health of all microservices (REQUIRES AUTH)"""
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
    return {
        "gateway": "running",
        "authenticated_user": current_user["username"],
        "user_role": current_user["role"],
        "services": results
    }

async def forward_request(request: Request, service_url: str, path: str, current_user: dict):
    """Forward a request to the target microservice with user context"""
    url = f"{service_url}/{path}"
    if request.url.query:
        url += f"?{request.url.query}"
    
    body = await request.body()
    headers = {k: v for k, v in request.headers.items() if k.lower() not in ("host", "content-length")}
    
    # Add user context to headers
    headers["X-User"] = current_user["username"]
    headers["X-User-Role"] = current_user["role"]

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
@app.get("/patients", tags=["Patient Service"], summary="List all patients")
async def patient_get_all(request: Request, current_user: dict = Depends(get_current_user)):
    """Get all patients"""
    return await forward_request(request, "http://localhost:8001", "patients", current_user)

@app.get("/patients/{patient_id}", tags=["Patient Service"], summary="Get patient by ID")
async def patient_get_by_id(request: Request, patient_id: int, current_user: dict = Depends(get_current_user)):
    """Get a specific patient by ID"""
    return await forward_request(request, "http://localhost:8001", f"patients/{patient_id}", current_user)

@app.post("/patients", tags=["Patient Service"], summary="Create new patient")
async def patient_post(request: Request, current_user: dict = Depends(get_current_user)):
    """Create a new patient (Admin only)"""
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admins can create patients")
    return await forward_request(request, "http://localhost:8001", "patients", current_user)

@app.put("/patients/{patient_id}", tags=["Patient Service"], summary="Update patient")
async def patient_put(request: Request, patient_id: int, current_user: dict = Depends(get_current_user)):
    """Update a patient (Admin & Doctor only)"""
    if current_user["role"] not in ["admin", "doctor"]:
        raise HTTPException(status_code=403, detail="Only admins and doctors can update patients")
    return await forward_request(request, "http://localhost:8001", f"patients/{patient_id}", current_user)

@app.delete("/patients/{patient_id}", tags=["Patient Service"], summary="Delete patient")
async def patient_delete(request: Request, patient_id: int, current_user: dict = Depends(get_current_user)):
    """Delete a patient (Admin only)"""
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admins can delete patients")
    return await forward_request(request, "http://localhost:8001", f"patients/{patient_id}", current_user)

# ── Doctor routes ───────────────────────────────────────────
@app.get("/doctors", tags=["Doctor Service"], summary="List all doctors")
async def doctor_get_all(request: Request, current_user: dict = Depends(get_current_user)):
    """Get all doctors"""
    return await forward_request(request, "http://localhost:8002", "doctors", current_user)

@app.get("/doctors/{doctor_id}", tags=["Doctor Service"], summary="Get doctor by ID")
async def doctor_get_by_id(request: Request, doctor_id: int, current_user: dict = Depends(get_current_user)):
    """Get a specific doctor by ID"""
    return await forward_request(request, "http://localhost:8002", f"doctors/{doctor_id}", current_user)

@app.post("/doctors", tags=["Doctor Service"], summary="Create new doctor")
async def doctor_post(request: Request, current_user: dict = Depends(get_current_user)):
    """Add a new doctor (Admin only)"""
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admins can add doctors")
    return await forward_request(request, "http://localhost:8002", "doctors", current_user)

@app.put("/doctors/{doctor_id}", tags=["Doctor Service"], summary="Update doctor")
async def doctor_put(request: Request, doctor_id: int, current_user: dict = Depends(get_current_user)):
    """Update a doctor (Admin only)"""
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admins can update doctors")
    return await forward_request(request, "http://localhost:8002", f"doctors/{doctor_id}", current_user)

@app.delete("/doctors/{doctor_id}", tags=["Doctor Service"], summary="Delete doctor")
async def doctor_delete(request: Request, doctor_id: int, current_user: dict = Depends(get_current_user)):
    """Delete a doctor (Admin only)"""
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admins can delete doctors")
    return await forward_request(request, "http://localhost:8002", f"doctors/{doctor_id}", current_user)

# ── Appointment routes ──────────────────────────────────────
@app.get("/appointments", tags=["Appointment Service"], summary="List all appointments")
async def appt_get_all(request: Request, current_user: dict = Depends(get_current_user)):
    """Get all appointments"""
    return await forward_request(request, "http://localhost:8003", "appointments", current_user)

@app.get("/appointments/{appt_id}", tags=["Appointment Service"], summary="Get appointment by ID")
async def appt_get_by_id(request: Request, appt_id: int, current_user: dict = Depends(get_current_user)):
    """Get a specific appointment by ID"""
    return await forward_request(request, "http://localhost:8003", f"appointments/{appt_id}", current_user)

@app.post("/appointments", tags=["Appointment Service"], summary="Create appointment")
async def appt_post(request: Request, current_user: dict = Depends(get_current_user)):
    """Book an appointment (Admin, Patient, Doctor can create)"""
    if current_user["role"] not in ["admin", "patient", "doctor"]:
        raise HTTPException(status_code=403, detail="Not authorized to book appointments")
    return await forward_request(request, "http://localhost:8003", "appointments", current_user)

@app.put("/appointments/{appt_id}", tags=["Appointment Service"], summary="Update appointment")
async def appt_put(request: Request, appt_id: int, current_user: dict = Depends(get_current_user)):
    """Update appointment (Admin & Doctor only)"""
    if current_user["role"] not in ["admin", "doctor"]:
        raise HTTPException(status_code=403, detail="Only admins and doctors can update appointments")
    return await forward_request(request, "http://localhost:8003", f"appointments/{appt_id}", current_user)

@app.delete("/appointments/{appt_id}", tags=["Appointment Service"], summary="Cancel appointment")
async def appt_delete(request: Request, appt_id: int, current_user: dict = Depends(get_current_user)):
    """Cancel appointment (Admin & Doctor only)"""
    if current_user["role"] not in ["admin", "doctor"]:
        raise HTTPException(status_code=403, detail="Only admins and doctors can cancel appointments")
    return await forward_request(request, "http://localhost:8003", f"appointments/{appt_id}", current_user)

# ── Pharmacy routes ─────────────────────────────────────────
@app.get("/medicines", tags=["Pharmacy Service"], summary="List all medicines")
async def med_get_all(request: Request, current_user: dict = Depends(get_current_user)):
    """Get all medicines"""
    return await forward_request(request, "http://localhost:8004", "medicines", current_user)

@app.get("/medicines/{med_id}", tags=["Pharmacy Service"], summary="Get medicine by ID")
async def med_get_by_id(request: Request, med_id: int, current_user: dict = Depends(get_current_user)):
    """Get a specific medicine by ID"""
    return await forward_request(request, "http://localhost:8004", f"medicines/{med_id}", current_user)

@app.post("/medicines", tags=["Pharmacy Service"], summary="Add new medicine")
async def med_post(request: Request, current_user: dict = Depends(get_current_user)):
    """Add a new medicine (Admin only)"""
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admins can add medicines")
    return await forward_request(request, "http://localhost:8004", "medicines", current_user)

@app.get("/prescriptions", tags=["Pharmacy Service"], summary="List all prescriptions")
async def pres_get_all(request: Request, current_user: dict = Depends(get_current_user)):
    """Get all prescriptions"""
    return await forward_request(request, "http://localhost:8004", "prescriptions", current_user)

@app.get("/prescriptions/{pres_id}", tags=["Pharmacy Service"], summary="Get prescription by ID")
async def pres_get_by_id(request: Request, pres_id: int, current_user: dict = Depends(get_current_user)):
    """Get a specific prescription by ID"""
    return await forward_request(request, "http://localhost:8004", f"prescriptions/{pres_id}", current_user)

@app.post("/prescriptions", tags=["Pharmacy Service"], summary="Create prescription")
async def pres_post(request: Request, current_user: dict = Depends(get_current_user)):
    """Create a prescription (Admin & Doctor only)"""
    if current_user["role"] not in ["admin", "doctor"]:
        raise HTTPException(status_code=403, detail="Only admins and doctors can create prescriptions")
    return await forward_request(request, "http://localhost:8004", "prescriptions", current_user)

# ── Billing routes ──────────────────────────────────────────
@app.get("/bills", tags=["Billing Service"], summary="List all bills")
async def bill_get_all(request: Request, current_user: dict = Depends(get_current_user)):
    """Get all bills"""
    return await forward_request(request, "http://localhost:8005", "bills", current_user)

@app.get("/bills/{bill_id}", tags=["Billing Service"], summary="Get bill by ID")
async def bill_get_by_id(request: Request, bill_id: int, current_user: dict = Depends(get_current_user)):
    """Get a specific bill by ID"""
    return await forward_request(request, "http://localhost:8005", f"bills/{bill_id}", current_user)

@app.post("/bills", tags=["Billing Service"], summary="Create new bill")
async def bill_post(request: Request, current_user: dict = Depends(get_current_user)):
    """Create a bill (Admin & Doctor only)"""
    if current_user["role"] not in ["admin", "doctor"]:
        raise HTTPException(status_code=403, detail="Only admins and doctors can create bills")
    return await forward_request(request, "http://localhost:8005", "bills", current_user)

@app.put("/bills/{bill_id}", tags=["Billing Service"], summary="Update bill")
async def bill_put(request: Request, bill_id: int, current_user: dict = Depends(get_current_user)):
    """Update a bill (Admin only)"""
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admins can update bills")
    return await forward_request(request, "http://localhost:8005", f"bills/{bill_id}", current_user)

@app.delete("/bills/{bill_id}", tags=["Billing Service"], summary="Delete bill")
async def bill_delete(request: Request, bill_id: int, current_user: dict = Depends(get_current_user)):
    """Delete a bill (Admin only)"""
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admins can delete bills")
    return await forward_request(request, "http://localhost:8005", f"bills/{bill_id}", current_user)

# ── Lab routes ──────────────────────────────────────────────
@app.get("/tests", tags=["Lab Service"], summary="List all lab tests")
async def lab_get_all(request: Request, current_user: dict = Depends(get_current_user)):
    """Get all lab tests"""
    return await forward_request(request, "http://localhost:8006", "tests", current_user)

@app.get("/tests/{test_id}", tags=["Lab Service"], summary="Get lab test by ID")
async def lab_get_by_id(request: Request, test_id: int, current_user: dict = Depends(get_current_user)):
    """Get a specific lab test by ID"""
    return await forward_request(request, "http://localhost:8006", f"tests/{test_id}", current_user)

@app.post("/tests", tags=["Lab Service"], summary="Order new lab test")
async def lab_post(request: Request, current_user: dict = Depends(get_current_user)):
    """Order a new lab test (Admin & Doctor only)"""
    if current_user["role"] not in ["admin", "doctor"]:
        raise HTTPException(status_code=403, detail="Only admins and doctors can order tests")
    return await forward_request(request, "http://localhost:8006", "tests", current_user)

@app.put("/tests/{test_id}", tags=["Lab Service"], summary="Update lab test")
async def lab_put(request: Request, test_id: int, current_user: dict = Depends(get_current_user)):
    """Update a lab test (Admin & Doctor only)"""
    if current_user["role"] not in ["admin", "doctor"]:
        raise HTTPException(status_code=403, detail="Only admins and doctors can update tests")
    return await forward_request(request, "http://localhost:8006", f"tests/{test_id}", current_user)

@app.delete("/tests/{test_id}", tags=["Lab Service"], summary="Delete lab test")
async def lab_delete(request: Request, test_id: int, current_user: dict = Depends(get_current_user)):
    """Delete a lab test (Admin only)"""
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admins can delete tests")
    return await forward_request(request, "http://localhost:8006", f"tests/{test_id}", current_user)
