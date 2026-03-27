#!/bin/bash
# ============================================================
#  Hospital Microservices - Start All Services
#  Run this script from the project root folder
# ============================================================

echo "🏥 Starting Hospital Microservices System..."
echo ""

# Start each microservice in background
echo "▶ Starting Patient Service     → http://localhost:8001/docs"
uvicorn main:app --app-dir patient-service --host 0.0.0.0 --port 8001 --reload &

echo "▶ Starting Doctor Service      → http://localhost:8002/docs"
uvicorn main:app --app-dir doctor-service --host 0.0.0.0 --port 8002 --reload &

echo "▶ Starting Appointment Service → http://localhost:8003/docs"
uvicorn main:app --app-dir appointment-service --host 0.0.0.0 --port 8003 --reload &

echo "▶ Starting Pharmacy Service    → http://localhost:8004/docs"
uvicorn main:app --app-dir pharmacy-service --host 0.0.0.0 --port 8004 --reload &

echo "▶ Starting Billing Service     → http://localhost:8005/docs"
uvicorn main:app --app-dir billing-service --host 0.0.0.0 --port 8005 --reload &

echo "▶ Starting Lab Service         → http://localhost:8006/docs"
uvicorn main:app --app-dir lab-service --host 0.0.0.0 --port 8006 --reload &

sleep 2

echo "▶ Starting API Gateway         → http://localhost:8000/docs"
uvicorn main:app --app-dir api-gateway --host 0.0.0.0 --port 8000 --reload &

echo ""
echo "✅ All services started!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  DIRECT ACCESS (Native Swagger):"
echo "  Patient:     http://localhost:8001/docs"
echo "  Doctor:      http://localhost:8002/docs"
echo "  Appointment: http://localhost:8003/docs"
echo "  Pharmacy:    http://localhost:8004/docs"
echo "  Billing:     http://localhost:8005/docs"
echo "  Lab:         http://localhost:8006/docs"
echo ""
echo "  VIA GATEWAY (Single Entry Point):"
echo "  Gateway:     http://localhost:8000/docs"
echo "  Health:      http://localhost:8000/health"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Press Ctrl+C to stop all services"

wait
