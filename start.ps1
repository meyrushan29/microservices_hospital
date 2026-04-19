$port = 8003
$host = "0.0.0.0"
$title = "Appointment Service"

Write-Host "Starting $title on port $port..."
$process = Start-Process -FilePath "uvicorn" -ArgumentList "main:app","--host",$host,"--port",$port,"--reload" -NoNewWindow -PassThru

Start-Sleep 2

if (!$process.HasExited) {
    Write-Host "$title started successfully on http://localhost:$port"
    Write-Host "Swagger UI: http://localhost:$port/docs"
} else {
    Write-Host "Failed to start $title"
    exit 1
}