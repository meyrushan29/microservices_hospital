# 🧪 Complete Testing Guide — Via Gateway & Direct Access

This document provides comprehensive testing scenarios demonstrating that all microservices work perfectly both through the API Gateway and through direct service access. This directly fulfills the assignment requirement of "endpoints accessible by using the API gateway as well as separately."

---

## 📋 Quick Test Checklist

Use this to verify your system is working correctly:

- [ ] All services start without errors (via start_all.ps1 or start_all.sh)
- [ ] API Gateway responds at http://localhost:8000/docs
- [ ] Each service responds at its native port (8001-8006)
- [ ] Authentication endpoint works and returns JWT token
- [ ] Can create patient via gateway (POST /patients)
- [ ] Can read patient via gateway (GET /patients)
- [ ] Can create patient directly on port 8001
- [ ] Can read patient directly on port 8001
- [ ] RBAC denies unauthorized access
- [ ] All 6 services routing correctly through gateway

---

## 🚀 Pre-Testing Setup

### 1. Start All Services

**Windows PowerShell:**
```powershell
cd hospital-microservices
.\start_all.ps1
```

**Linux/macOS:**
```bash
cd hospital-microservices
bash start_all.sh
```

**Expected Output:**
```
Starting API Gateway on port 8000...
Starting Patient Service on port 8001...
Starting Doctor Service on port 8002...
Starting Appointment Service on port 8003...
Starting Pharmacy Service on port 8004...
Starting Billing Service on port 8005...
Starting Lab Service on port 8006...

All services started successfully!
```

### 2. Verify All Services Running

Open a new terminal and check each service:

```bash
# Windows
netstat -ano | findstr "8000\|8001\|8002\|8003\|8004\|8005\|8006"

# Linux/macOS
lsof -i :8000-8006
```

You should see 7 processes listening on ports 8000-8006.

### 3. Save Authentication Token to Environment Variable

```bash
# Get token
export TOKEN=$(curl -s -X POST http://localhost:8000/authenticate \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

# Verify token is saved (should print the token)
echo $TOKEN

# Windows PowerShell (use this instead)
$TOKEN = (curl -s -X POST http://localhost:8000/authenticate `
  -H "Content-Type: application/json" `
  -d '{"username":"admin","password":"admin123"}' | ConvertFrom-Json).access_token
echo $TOKEN
```

Save this token for all subsequent tests.

---

## 🔐 1. Authentication Testing

### Test 1.1: Authenticate with Valid Credentials

**Endpoint:** `POST /authenticate` (Via Gateway)

```bash
curl -X POST http://localhost:8000/authenticate \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

**Expected Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_role": "admin"
}
```

✅ **What this proves:** Authentication system working, JWT tokens generated correctly.

---

### Test 1.2: Authenticate with Invalid Credentials

```bash
curl -X POST http://localhost:8000/authenticate \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "wrongpassword"
  }'
```

**Expected Response (401 Unauthorized):**
```json
{
  "detail": "Invalid credentials"
}
```

✅ **What this proves:** Security working, invalid credentials rejected.

---

### Test 1.3: Get Token for Different Roles

**Doctor Token:**
```bash
curl -X POST http://localhost:8000/authenticate \
  -H "Content-Type: application/json" \
  -d '{"username":"doctor","password":"doctor123"}'
```

**Patient Token:**
```bash
curl -X POST http://localhost:8000/authenticate \
  -H "Content-Type: application/json" \
  -d '{"username":"patient","password":"patient123"}'
```

✅ **What this proves:** Multiple user roles supported.

---

## 👥 2. Patient Service Testing (Meyrushan N)

### Test 2.1: Create Patient via API Gateway

**Endpoint:** `POST /patients` (Via Gateway - Port 8000)

```bash
curl -X POST http://localhost:8000/patients \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "age": 45,
    "gender": "Male",
    "blood_type": "O+",
    "phone": "0771234567",
    "address": "Colombo",
    "admitted_date": "2026-03-30"
  }'
```

**Expected Response (201 Created):**
```json
{
  "id": 1,
  "name": "John Doe",
  "age": 45,
  "gender": "Male",
  "blood_type": "O+",
  "phone": "0771234567",
  "address": "Colombo",
  "admitted_date": "2026-03-30"
}
```

✅ **What this proves:** API Gateway routing works, patient creation via gateway successful.

---

### Test 2.2: Create Patient DIRECTLY on Patient Service (Port 8001)

**Same endpoint but direct access - No Gateway**

```bash
curl -X POST http://localhost:8001/patients \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Smith",
    "age": 38,
    "gender": "Female",
    "blood_type": "A+",
    "phone": "0779876543",
    "address": "Kandy",
    "admitted_date": "2026-03-28"
  }'
```

**Expected Response (201 Created):** *(Same structure as above)*

✅ **What this proves:** Service works independently, can be accessed directly without gateway.

---

### Test 2.3: Get All Patients via Gateway

**Endpoint:** `GET /patients` (Via Gateway)

```bash
curl -X GET http://localhost:8000/patients \
  -H "Authorization: Bearer $TOKEN"
```

**Expected Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "age": 45,
    ...
  },
  {
    "id": 2,
    "name": "Jane Smith",
    "age": 38,
    ...
  }
]
```

✅ **What this proves:** Gateway retrieves data from service correctly.

---

### Test 2.4: Get All Patients DIRECTLY from Patient Service (Port 8001)

```bash
curl -X GET http://localhost:8001/patients \
  -H "Authorization: Bearer $TOKEN"
```

**Expected Response:** *(Same as Test 2.3)*

✅ **What this proves:** Same data accessible both ways (via gateway and directly).

---

### Test 2.5: Get Specific Patient via Gateway

```bash
curl -X GET http://localhost:8000/patients/1 \
  -H "Authorization: Bearer $TOKEN"
```

**Expected Response (200 OK):**
```json
{
  "id": 1,
  "name": "John Doe",
  "age": 45,
  ...
}
```

---

### Test 2.6: Get Specific Patient DIRECTLY (Port 8001)

```bash
curl -X GET http://localhost:8001/patients/1 \
  -H "Authorization: Bearer $TOKEN"
```

**Expected Response:** *(Same as Test 2.5)*

---

### Test 2.7: Update Patient via Gateway

```bash
curl -X PUT http://localhost:8000/patients/1 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 46
  }'
```

**Expected Response (200 OK):**
```json
{
  "id": 1,
  "name": "John Doe",
  "age": 46,  ← Updated
  ...
}
```

---

## 👨‍⚕️ 3. Doctor Service Testing (Laxshika S)

### Test 3.1: Create Doctor via API Gateway

**Endpoint:** `POST /doctors` (Via Gateway - Port 8000)

```bash
curl -X POST http://localhost:8000/doctors \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Dr. Smith",
    "specialization": "Cardiology",
    "phone": "0771111111",
    "email": "dr.smith@hospital.com",
    "qualification": "MBBS, MD",
    "experience_years": 10,
    "is_available": true
  }'
```

**Expected Response (201 Created):**
```json
{
  "id": 1,
  "name": "Dr. Smith",
  "specialization": "Cardiology",
  ...
}
```

✅ **What this proves:** Doctor service routing via gateway works.

---

### Test 3.2: Create Doctor DIRECTLY on Doctor Service (Port 8002)

```bash
curl -X POST http://localhost:8002/doctors \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Dr. Johnson",
    "specialization": "Neurology",
    "phone": "0772222222",
    "email": "dr.johnson@hospital.com",
    "qualification": "MBBS, MD",
    "experience_years": 8,
    "is_available": true
  }'
```

**Expected Response:** *(Same structure)*

✅ **What this proves:** Doctor service accessible directly without gateway.

---

### Test 3.3: Get All Doctors via Gateway

```bash
curl -X GET http://localhost:8000/doctors \
  -H "Authorization: Bearer $TOKEN"
```

---

### Test 3.4: Get All Doctors DIRECTLY from Doctor Service

```bash
curl -X GET http://localhost:8002/doctors \
  -H "Authorization: Bearer $TOKEN"
```

✅ **What this proves:** Both access methods return same data.

---

## 📅 4. Appointment Service Testing (Laksopan R)

### Test 4.1: Book Appointment via API Gateway

**Endpoint:** `POST /appointments` (Via Gateway)

```bash
curl -X POST http://localhost:8000/appointments \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": 1,
    "doctor_id": 1,
    "date": "2026-04-15",
    "time": "2:00 PM",
    "reason": "Cardiac checkup",
    "status": "pending"
  }'
```

**Expected Response (201 Created):**
```json
{
  "id": 1,
  "patient_id": 1,
  "doctor_id": 1,
  "date": "2026-04-15",
  "time": "2:00 PM",
  "reason": "Cardiac checkup",
  "status": "pending"
}
```

---

### Test 4.2: Book Appointment DIRECTLY on Appointment Service (Port 8003)

```bash
curl -X POST http://localhost:8003/appointments \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": 2,
    "doctor_id": 1,
    "date": "2026-04-16",
    "time": "3:00 PM",
    "reason": "Follow-up",
    "status": "pending"
  }'
```

---

### Test 4.3: Get All Appointments via Gateway

```bash
curl -X GET http://localhost:8000/appointments \
  -H "Authorization: Bearer $TOKEN"
```

---

### Test 4.4: Get All Appointments DIRECTLY (Port 8003)

```bash
curl -X GET http://localhost:8003/appointments \
  -H "Authorization: Bearer $TOKEN"
```

---

## 💊 5. Pharmacy Service Testing (Viththakan N)

### Test 5.1: Add Medicine via API Gateway

**Endpoint:** `POST /medicines` (Via Gateway)

```bash
curl -X POST http://localhost:8000/medicines \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Aspirin",
    "generic_name": "Acetylsalicylic acid",
    "manufacturer": "Bayer",
    "dosage": "500mg",
    "unit_price": 50.00,
    "stock_quantity": 100,
    "expiry_date": "2027-12-31"
  }'
```

**Expected Response (201 Created):**
```json
{
  "id": 1,
  "name": "Aspirin",
  "generic_name": "Acetylsalicylic acid",
  "stock_quantity": 100,
  ...
}
```

---

### Test 5.2: Add Medicine DIRECTLY to Pharmacy Service (Port 8004)

```bash
curl -X POST http://localhost:8004/medicines \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ibuprofen",
    "generic_name": "Ibuprofen",
    "manufacturer": "Pfizer",
    "dosage": "200mg",
    "unit_price": 30.00,
    "stock_quantity": 150,
    "expiry_date": "2027-10-31"
  }'
```

---

### Test 5.3: Get All Medicines via Gateway

```bash
curl -X GET http://localhost:8000/medicines \
  -H "Authorization: Bearer $TOKEN"
```

---

### Test 5.4: Get All Medicines DIRECTLY (Port 8004)

```bash
curl -X GET http://localhost:8004/medicines \
  -H "Authorization: Bearer $TOKEN"
```

---

## 💰 6. Billing Service Testing (Hariyah L)

### Test 6.1: Create Bill via API Gateway

**Endpoint:** `POST /bills` (Via Gateway)

```bash
curl -X POST http://localhost:8000/bills \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": 1,
    "appointment_id": 1,
    "medicine_cost": 500.00,
    "lab_test_cost": 1000.00,
    "consultation_fee": 2000.00,
    "total_amount": 3500.00,
    "due_date": "2026-04-15",
    "status": "pending",
    "payment_method": "Cash"
  }'
```

**Expected Response (201 Created):**
```json
{
  "id": 1,
  "patient_id": 1,
  "total_amount": 3500.00,
  "status": "pending",
  ...
}
```

---

### Test 6.2: Create Bill DIRECTLY on Billing Service (Port 8005)

```bash
curl -X POST http://localhost:8005/bills \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": 2,
    "appointment_id": 2,
    "medicine_cost": 300.00,
    "lab_test_cost": 800.00,
    "consultation_fee": 1500.00,
    "total_amount": 2600.00,
    "due_date": "2026-04-20",
    "status": "pending",
    "payment_method": "Card"
  }'
```

---

### Test 6.3: Get All Bills via Gateway

```bash
curl -X GET http://localhost:8000/bills \
  -H "Authorization: Bearer $TOKEN"
```

---

### Test 6.4: Get All Bills DIRECTLY (Port 8005)

```bash
curl -X GET http://localhost:8005/bills \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🧬 7. Lab Service Testing (Nilakshan V)

### Test 7.1: Order Lab Test via API Gateway

**Endpoint:** `POST /tests` (Via Gateway)

```bash
curl -X POST http://localhost:8000/tests \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": 1,
    "doctor_id": 1,
    "test_type": "Blood Count",
    "ordered_date": "2026-03-30",
    "scheduled_date": "2026-03-31",
    "status": "pending"
  }'
```

**Expected Response (201 Created):**
```json
{
  "id": 1,
  "patient_id": 1,
  "test_type": "Blood Count",
  "status": "pending",
  ...
}
```

---

### Test 7.2: Order Lab Test DIRECTLY on Lab Service (Port 8006)

```bash
curl -X POST http://localhost:8006/tests \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": 2,
    "doctor_id": 1,
    "test_type": "Urinalysis",
    "ordered_date": "2026-03-30",
    "scheduled_date": "2026-04-01",
    "status": "pending"
  }'
```

---

### Test 7.3: Get All Tests via Gateway

```bash
curl -X GET http://localhost:8000/tests \
  -H "Authorization: Bearer $TOKEN"
```

---

### Test 7.4: Get All Tests DIRECTLY (Port 8006)

```bash
curl -X GET http://localhost:8006/tests \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🔒 8. RBAC / Permission Testing

### Test 8.1: Admin Can Create Patient

```bash
# Get admin token
ADMIN_TOKEN=$(curl -s -X POST http://localhost:8000/authenticate \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

# Create patient (should succeed)
curl -X POST http://localhost:8000/patients \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Patient","age":30,"gender":"M","blood_type":"O+","phone":"123","address":"Test","admitted_date":"2026-03-30"}'
```

**Expected:** 201 Created ✅

---

### Test 8.2: Doctor Can View Patients

```bash
# Get doctor token
DOCTOR_TOKEN=$(curl -s -X POST http://localhost:8000/authenticate \
  -H "Content-Type: application/json" \
  -d '{"username":"doctor","password":"doctor123"}' | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

# View patients (should succeed)
curl -X GET http://localhost:8000/patients \
  -H "Authorization: Bearer $DOCTOR_TOKEN"
```

**Expected:** 200 OK (list of patients) ✅

---

### Test 8.3: Patient Cannot Create Patients

```bash
# Get patient token
PATIENT_TOKEN=$(curl -s -X POST http://localhost:8000/authenticate \
  -H "Content-Type: application/json" \
  -d '{"username":"patient","password":"patient123"}' | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

# Try to create patient (should fail)
curl -X POST http://localhost:0000/patients \
  -H "Authorization: Bearer $PATIENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Unauthorized","age":25,"gender":"F","blood_type":"A+","phone":"456","address":"Test","admitted_date":"2026-03-30"}'
```

**Expected:** 403 Forbidden ✅

---

### Test 8.4: No Token = Unauthorized

```bash
# Try without token (should fail)
curl -X GET http://localhost:8000/patients
```

**Expected:** 401 Unauthorized ✅

---

## 🎯 9. Complete Business Workflow Test

This demonstrates a real-world scenario:

**Scenario:** Admin creates patient, doctor books appointment, lab orders test

### Step 1: Admin Authenticates

```bash
ADMIN=$(curl -s -X POST http://localhost:8000/authenticate \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
```

### Step 2: Admin Creates Patient (via Gateway)

```bash
curl -X POST http://localhost:8000/patients \
  -H "Authorization: Bearer $ADMIN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Michael Brown",
    "age": 55,
    "gender": "Male",
    "blood_type": "B+",
    "phone": "0775555555",
    "address": "Galle",
    "admitted_date": "2026-03-30"
  }'
```

*Expected:* Patient created with ID (e.g., ID: 5)

### Step 3: Doctor Books Appointment (via Gateway)

```bash
DOCTOR=$(curl -s -X POST http://localhost:8000/authenticate \
  -H "Content-Type: application/json" \
  -d '{"username":"doctor","password":"doctor123"}' | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

curl -X POST http://localhost:8000/appointments \
  -H "Authorization: Bearer $DOCTOR" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": 5,
    "doctor_id": 1,
    "date": "2026-04-05",
    "time": "10:00 AM",
    "reason": "General checkup",
    "status": "confirmed"
  }'
```

*Expected:* Appointment created with ID (e.g., ID: 3)

### Step 4: Doctor Orders Lab Test (DIRECTLY on Lab Service - Port 8006)

```bash
curl -X POST http://localhost:8006/tests \
  -H "Authorization: Bearer $DOCTOR" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": 5,
    "doctor_id": 1,
    "test_type": "CBC (Complete Blood Count)",
    "ordered_date": "2026-03-30",
    "scheduled_date": "2026-04-01",
    "status": "pending"
  }'
```

*Expected:* Lab test created with ID (e.g., ID: 3)

### Step 5: Verify Data Consistency (Access SAME data from Gateway vs Direct)

**Check patient via Gateway:**
```bash
curl -X GET http://localhost:8000/patients/5 \
  -H "Authorization: Bearer $ADMIN"
```

**Check patient DIRECTLY (Port 8001):**
```bash
curl -X GET http://localhost:8001/patients/5 \
  -H "Authorization: Bearer $ADMIN"
```

*Expected:* Both return identical patient data ✅

---

## 📋 Summary: Test Result Checklist

After running all tests, you should verify:

```
✅ Authentication Tests
   - Valid credentials return token
   - Invalid credentials rejected
   - Multiple users (admin, doctor, patient) work
   
✅ Patient Service  (Meyrushan N)
   - Create via Gateway
   - Create Directly (Port 8001)
   - Read via Gateway
   - Read Directly (Port 8001)
   - Both return same data

✅ Doctor Service  (Laxshika S)
   - Create via Gateway
   - Create Directly (Port 8002)
   - Read via Gateway (Port 8000)
   - Read Directly (Port 8002)
   - Both return same data

✅ Appointment Service  (Laksopan R)
   - Create via Gateway
   - Create Directly (Port 8003)
   - Read via Gateway
   - Read Directly (Port 8003)
   - Both return same data

✅ Pharmacy Service  (Viththakan N)
   - Create via Gateway
   - Create Directly (Port 8004)
   - Read via Gateway
   - Read Directly (Port 8004)
   - Both return same data

✅ Billing Service  (Hariyah L)
   - Create via Gateway
   - Create Directly (Port 8005)
   - Read via Gateway
   - Read Directly (Port 8005)
   - Both return same data

✅ Lab Service  (Nilakshan V)
   - Create via Gateway
   - Create Directly (Port 8006)
   - Read via Gateway
   - Read Directly (Port 8006)
   - Both return same data

✅ RBAC/Security
   - Admin can create resources
   - Doctor can view and create appointments
   - Patient has limited read access
   - No token = 401 Unauthorized
   - Invalid role = 403 Forbidden

✅ Business Workflow
   - Complete end-to-end scenario works
   - Data consistent across access methods
```

---

## 🎬 Screenshots for Slide Deck

Capture these screenshots for your presentation:

1. **Terminal showing all services starting**
   - `start_all.ps1` or `start_all.sh` output
   - All 7 services should show startup messages

2. **API Gateway Swagger UI**
   - http://localhost:8000/docs screenshot
   - Show all available endpoints

3. **Patient Service Swagger UI (Direct)**
   - http://localhost:8001/docs screenshot
   - Show endpoints available directly

4. **Curl request to create patient via Gateway**
   - Command and response (201 Created)
   - Clearly show request to localhost:8000

5. **Curl request to create patient directly**
   - Same data, but request to localhost:8001
   - Show both work identically

6. **Get patients via Gateway**
   - Table of patients created via gateway
   - Show authorization header

7. **Get patients from direct service**
   - Same data from port 8001
   - Prove both access methods work

8. **RBAC test - missing token error**
   - Show 401 Unauthorized response

9. **RBAC test - insufficient permissions**
   - Show 403 Forbidden response

10. **All six services returning data**
    - Screenshots from ports 8001-8006
    - Prove each service works independently

---

**Testing Document Version:** 1.0  
**Last Updated:** March 30, 2026  
**For Assignment Submission:** Include test result screenshots in slide deck

