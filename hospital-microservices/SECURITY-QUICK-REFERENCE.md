# 🔐 API Security - Quick Reference Guide

## 📚 Table of Contents
1. [Authentication](#authentication)
2. [Available Roles](#available-roles)
3. [Common API Calls](#common-api-calls)
4. [Error Handling](#error-handling)

---

## 🔑 Authentication

### Get JWT Token

```bash
# Admin Authentication
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
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsInJvbGUiOiJhZG1pbiIsImV4cCI6MTc0MzMxNzk5MS41Njc5MTV9.VeZy...",
  "token_type": "bearer",
  "user_role": "admin"
}
```

---

## 👥 Available Roles

### 1. **Admin Role** (Full Access)
- Create/Update/Delete all resources
- Manage users and permissions
- Access all endpoints

```bash
ADMIN_TOKEN=$(curl -s -X POST http://localhost:8000/authenticate \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' | jq -r '.access_token')

curl -H "Authorization: Bearer $ADMIN_TOKEN" \
  http://localhost:8000/patients
```

### 2. **Doctor Role** (Medical Operations)
- View patients
- Create prescriptions and lab tests
- Update appointments
- Create/Update bills

```bash
DOCTOR_TOKEN=$(curl -s -X POST http://localhost:8000/authenticate \
  -H "Content-Type: application/json" \
  -d '{"username":"doctor","password":"doctor123"}' | jq -r '.access_token')

# Doctor can order lab tests
curl -X POST http://localhost:8000/tests \
  -H "Authorization: Bearer $DOCTOR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": 1,
    "test_name": "Blood Test",
    "ordered_by": 1,
    "date": "2026-03-30",
    "status": "pending"
  }'
```

### 3. **Patient Role** (Limited Access)
- View own data
- Book appointments
- View personal appointments

```bash
PATIENT_TOKEN=$(curl -s -X POST http://localhost:8000/authenticate \
  -H "Content-Type: application/json" \
  -d '{"username":"patient","password":"patient123"}' | jq -r '.access_token')

# Patient can book appointments
curl -X POST http://localhost:8000/appointments \
  -H "Authorization: Bearer $PATIENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": 1,
    "doctor_id": 1,
    "date": "2026-04-15",
    "time": "2:00 PM",
    "reason": "Checkup"
  }'
```

---

## 📋 Common API Calls with Security

### Health Check (Requires Auth)

```bash
TOKEN=$(curl -s -X POST http://localhost:8000/authenticate \
  -d '{"username":"admin","password":"admin123"}' \
  -H "Content-Type: application/json" | jq -r '.access_token')

curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/health
```

**Response:**
```json
{
  "gateway": "running",
  "authenticated_user": "admin",
  "user_role": "admin",
  "services": {
    "patient-service": "✅ running",
    "doctor-service": "✅ running",
    ...
  }
}
```

### Get All Patients

```bash
TOKEN=$(curl -s -X POST http://localhost:8000/authenticate \
  -d '{"username":"doctor","password":"doctor123"}' \
  -H "Content-Type: application/json" | jq -r '.access_token')

curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/patients
```

### Create Patient (Admin Only)

```bash
ADMIN_TOKEN=$(curl -s -X POST http://localhost:8000/authenticate \
  -d '{"username":"admin","password":"admin123"}' \
  -H "Content-Type: application/json" | jq -r '.access_token')

curl -X POST http://localhost:8000/patients \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe",
    "age": 32,
    "gender": "Female",
    "blood_type": "A+",
    "phone": "0779876543",
    "address": "Kandy",
    "admitted_date": "2026-03-30"
  }'
```

### Create Prescription (Doctor Only)

```bash
DOCTOR_TOKEN=$(curl -s -X POST http://localhost:8000/authenticate \
  -d '{"username":"doctor","password":"doctor123"}' \
  -H "Content-Type: application/json" | jq -r '.access_token')

curl -X POST http://localhost:8000/prescriptions \
  -H "Authorization: Bearer $DOCTOR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": 1,
    "doctor_id": 1,
    "medicines": ["Paracetamol", "Amoxicillin"],
    "date": "2026-03-30",
    "status": "pending"
  }'
```

### Order Lab Test (Doctor Only)

```bash
DOCTOR_TOKEN=$(curl -s -X POST http://localhost:8000/authenticate \
  -d '{"username":"doctor","password":"doctor123"}' \
  -H "Content-Type: application/json" | jq -r '.access_token')

curl -X POST http://localhost:8000/tests \
  -H "Authorization: Bearer $DOCTOR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": 1,
    "test_name": "MRI Brain",
    "ordered_by": 1,
    "date": "2026-03-30",
    "status": "pending"
  }'
```

---

## ❌ Error Handling

### 1. Missing Authentication

```bash
curl http://localhost:8000/patients
```

**Response (401 Unauthorized):**
```json
{
  "detail": "Not authenticated"
}
```

### 2. Invalid Token

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

### 3. Insufficient Permissions

```bash
# Patient tries to create patient (Admin only)
PATIENT_TOKEN=$(curl -s -X POST http://localhost:8000/authenticate \
  -d '{"username":"patient","password":"patient123"}' \
  -H "Content-Type: application/json" | jq -r '.access_token')

curl -X POST http://localhost:8000/patients \
  -H "Authorization: Bearer $PATIENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{...}'
```

**Response (403 Forbidden):**
```json
{
  "detail": "Only admins can create patients"
}
```

### 4. Expired Token

After 30 minutes, tokens expire:

```json
{
  "detail": "Invalid or expired token"
}
```

**Solution:** Get a new token using `/authenticate`

---

## 🛡️ Security Best Practices

✅ **Always use HTTPS in production**
✅ **Store tokens securely** (not in plain text)
✅ **Use token expiration** (30 minutes recommended)
✅ **Validate on every request** (done automatically)
✅ **Change default SECRET_KEY** before deployment
✅ **Log authentication events** for audit trails

---

## 🔗 Related Documentation

- **Detailed Security Guide:** See [SECURITY.md](./SECURITY.md)
- **API Gateway Details:** See [API Gateway Documentation](./api-gateway/README.md)
- **FastAPI Security:** https://fastapi.tiangolo.com/tutorial/security/

---

## 💡 Tips

### Save Token to Variable (Bash)
```bash
TOKEN=$(curl -s -X POST http://localhost:8000/authenticate \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' | jq -r '.access_token')

echo "Token: $TOKEN"
```

### Test with Swagger UI
1. Open: `http://localhost:8000/docs`
2. Click **"Authorize"** button (top right)
3. Enter credentials
4. All subsequent requests will use token

### Decode JWT (to see contents)
```bash
# Install: npm install -g jwt-cli
jwt decode "TOKEN_HERE"
```

---

## ❓ FAQ

**Q: How long are tokens valid?**  
A: 30 minutes. After expiration, authenticate again.

**Q: Can I change my password?**  
A: In this demo, passwords are hardcoded. In production, use a proper user management system.

**Q: What if I forget my token?**  
A: Don't worry! Just authenticate again with `/authenticate` endpoint.

**Q: Is HTTPS required?**  
A: Not for local development. Yes for production!

**Q: Can patients see other patients' data?**  
A: No. Patients can only book appointments (not view other patients).
