# Hospital Microservices — start all services (Windows / PowerShell)
# Run from project root:  .\start_all.ps1

$ErrorActionPreference = "Stop"
$root = $PSScriptRoot
Set-Location $root

$py = (Get-Command python -ErrorAction Stop).Source

Write-Host "Starting Hospital Microservices..." -ForegroundColor Cyan
Write-Host ""

$microservices = @(
    @{ Name = "Patient";     Dir = "patient-service";     Port = 8001 },
    @{ Name = "Doctor";      Dir = "doctor-service";      Port = 8002 },
    @{ Name = "Appointment"; Dir = "appointment-service"; Port = 8003 },
    @{ Name = "Pharmacy";    Dir = "pharmacy-service";    Port = 8004 },
    @{ Name = "Billing";     Dir = "billing-service";     Port = 8005 },
    @{ Name = "Lab";         Dir = "lab-service";         Port = 8006 }
)

foreach ($svc in $microservices) {
    Write-Host ("Starting {0} Service -> http://localhost:{1}/docs" -f $svc.Name, $svc.Port)
    Start-Process -FilePath $py -ArgumentList @(
        "-m", "uvicorn", "main:app",
        "--app-dir", $svc.Dir,
        "--host", "0.0.0.0",
        "--port", "$($svc.Port)",
        "--reload"
    ) -WorkingDirectory $root -WindowStyle Minimized
}

Start-Sleep -Seconds 2

Write-Host "Starting API Gateway -> http://localhost:8000/docs"
Start-Process -FilePath $py -ArgumentList @(
    "-m", "uvicorn", "main:app",
    "--app-dir", "api-gateway",
    "--host", "0.0.0.0",
    "--port", "8000",
    "--reload"
) -WorkingDirectory $root -WindowStyle Minimized

Write-Host ""
Write-Host "All services launched in minimized windows. Close those console windows to stop a service." -ForegroundColor Green
Write-Host "Gateway: http://localhost:8000/docs   Health: http://localhost:8000/health" -ForegroundColor Green
