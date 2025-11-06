# One-click start: FastAPI + ngrok
# Windows PowerShell

param(
  [switch]$NoBrowser
)

$ErrorActionPreference = 'Stop'

Write-Host "[1/4] Activating virtualenv..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1

Write-Host "[2/4] Starting FastAPI (Uvicorn)..." -ForegroundColor Yellow
Start-Process powershell -WindowStyle Hidden -ArgumentList "-NoProfile -Command python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
Start-Sleep -Seconds 3

Write-Host "[3/4] Starting ngrok..." -ForegroundColor Yellow
Start-Process powershell -WindowStyle Hidden -ArgumentList "-NoProfile -Command ngrok http 8000"
Start-Sleep -Seconds 4

Write-Host "[4/4] Fetching public URL..." -ForegroundColor Yellow
$base = "http://127.0.0.1:4040/api/tunnels"
$tunnels = $null
for ($i=0; $i -lt 10; $i++) {
  try { $tunnels = Invoke-RestMethod $base; if ($tunnels.tunnels.Count -gt 0) { break } } catch { }
  Start-Sleep -Milliseconds 800
}

if (-not $tunnels -or $tunnels.tunnels.Count -eq 0) {
  Write-Host "❌ Não foi possível obter a URL do ngrok." -ForegroundColor Red
  exit 1
}

$publicUrl = $tunnels.tunnels[0].public_url
Write-Host ""; Write-Host "✅ Público: $publicUrl" -ForegroundColor Green
Write-Host "Swagger: $publicUrl/docs" -ForegroundColor Cyan

if (-not $NoBrowser) {
  Start-Process "$publicUrl/docs"
}
