# 🔐 Security Implementation Guide

## Overview

The Hospital Management System now includes **JWT Token-Based Authentication** and **Role-Based Access Control (RBAC)**.

---

## 🔑 Authentication

### Step 1: Get JWT Token

First, authenticate with your credentials:

```bash
curl -X POST http://localhost:8000/authenticate \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_role": "admin"
}
```

### Step 2: Use Token in Requests

Include the token in the `Authorization` header:

```bash
curl -X GET http://localhost:8000/patients \
  -H "Authorization: Bearer <your_access_token>"
```

---

## 👥 Test Users

| Username | Password | Role | Permissions |
|---|---|---|---|
| **admin** | admin123 | admin | Full access to all endpoints |
| **doctor** | doctor123 | doctor | View patients, create prescriptions, order tests, manage appointments |
| **patient** | patient123 | patient | View own data, book appointments |

---

## 🛡️ Role-Based Access Control (RBAC)

### Permission Matrix

| Endpoint | GET | POST | PUT | DELETE | Required Role |
|---|---|---|---|---|---|
| `/patients` | ✅ All | ❌ Admin Only | ⚠️ Admin/Doctor | ❌ Admin Only | Authenticated |
| `/doctors` | ✅ All | ❌ Admin Only | ❌ Admin Only | ❌ Admin Only | Authenticated |
| `/appointments` | ✅ All | ✅ All | ⚠️ Admin/Doctor | ⚠️ Admin/Doctor | Authenticated |
| `/medicines` | ✅ All | ❌ Admin Only | ❌ N/A | ❌ N/A | Authenticated |
| `/prescriptions` | ✅ All | ⚠️ Admin/Doctor | ❌ N/A | ❌ N/A | Authenticated |
| `/bills` | ✅ All | ⚠️ Admin/Doctor | ❌ Admin Only | ❌ Admin Only | Authenticated |
| `/tests` | ✅ All | ⚠️ Admin/Doctor | ⚠️ Admin/Doctor | ❌ Admin Only | Authenticated |

---

## 📋 Complete Workflow Example

### 1️⃣ Admin Creates Patient

```bash
# Step 1: Get Admin Token
TOKEN=$(curl -s -X POST http://localhost:8000/authenticate \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }' | jq -r '.access_token')

# Step 2: Create Patient (Admin Only)
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

### 2️⃣ Doctor Books Appointment

```bash
# Step 1: Get Doctor Token
TOKEN=$(curl -s -X POST http://localhost:8000/authenticate \
  -H "Content-Type: application/json" \
  -d '{
    "username": "doctor",
    "password": "doctor123"
  }' | jq -r '.access_token')

# Step 2: Book Appointment
curl -X POST http://localhost:8000/appointments \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": 1,
    "doctor_id": 1,
    "date": "2026-04-15",
    "time": "2:00 PM",
    "reason": "Checkup",
    "status": "pending"
  }'
```

### 3️⃣ Doctor Orders Lab Test

```bash
# Get Doctor Token
TOKEN=$(curl -s -X POST http://localhost:8000/authenticate \
  -H "Content-Type: application/json" \
  -d '{
    "username": "doctor",
    "password": "doctor123"
  }' | jq -r '.access_token')

# Order Test
curl -X POST http://localhost:8000/tests \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": 1,
    "test_name": "Blood Count",
    "ordered_by": 1,
    "date": "2026-03-30",
    "status": "pending"
  }'
```

---

## ❌ Error Examples

### Missing Authentication

```bash
curl http://localhost:8000/patients
```

**Response (401 Unauthorized):**
```json
{
  "detail": "Not authenticated"
}
```

### Invalid Token

```bash
curl -H "Authorization: Bearer invalid_token" \
  http://localhost:8000/patients
```

**Response (401 Unauthorized):**
```json
{
  "detail": "Invalid or expired token"
}
```

### Insufficient Permissions

```bash
# Patient tries to create patient (Admin only)
TOKEN=$(curl -s -X POST http://localhost:8000/authenticate \
  -d '{"username":"patient","password":"patient123"}' \
  -H "Content-Type: application/json" | jq -r '.access_token')

curl -X POST http://localhost:8000/patients \
  -H "Authorization: Bearer $TOKEN"
```

**Response (403 Forbidden):**
```json
{
  "detail": "Only admins can create patients"
}
```

---

## 🔄 Token Information

- **Token Type:** JWT (JSON Web Token)
- **Algorithm:** HS256
- **Expiration:** 30 minutes
- **Issued At:** On each authentication
- **Payload Contains:**
  - `sub` (subject): Username
  - `role`: User role (admin/doctor/patient)
  - `exp` (expiration): Token expiry timestamp

---

## 🔒 Security Features Implemented

✅ **JWT Authentication** - Tokens required for all endpoints  
✅ **Role-Based Access Control (RBAC)** - Different permissions per role  
✅ **Token Expiration** - Tokens expire after 30 minutes  
✅ **User Context Tracking** - Headers include user info for audit trails  
✅ **Error Handling** - Clear error messages for auth failures  

---

## ⚠️ Important Notes

### For Production:

1. **Change Secret Key**
   ```python
   # api-gateway/main.py
   SECRET_KEY = "your-secret-key-change-in-production"
   ```
   Change to a strong, random key!

2. **Use HTTPS**
   ```bash
   uvicorn main:app --ssl-keyfile=key.pem --ssl-certfile=cert.pem
   ```

3. **Database Integration**
   - Store users in a real database
   - Hash passwords with bcrypt
   - Implement password reset functionality

4. **Rate Limiting**
   - Add request throttling to prevent brute force attacks

5. **Audit Logging**
   - Log all authentication attempts
   - Track user actions with timestamps

---

## 🚀 Testing the Security

### Using Postman or Swagger UI

1. Go to: `http://localhost:8000/docs`
2. Click **"Authorize"** button
3. Enter test user credentials
4. Test endpoints with protection

### Using cURL

```bash
# Authenticate
curl -X POST http://localhost:8000/authenticate \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Use the returned token
curl -H "Authorization: Bearer <token>" \
  http://localhost:8000/health
```

---

## 📞 Support

For issues or questions about security implementation, refer to:
- [FastAPI Security Docs](https://fastapi.tiangolo.com/tutorial/security/)
- [JWT Documentation](https://python-jose.readthedocs.io/)
