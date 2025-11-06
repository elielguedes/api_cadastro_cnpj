# run-local.ps1
# Convenience wrapper that calls start.ps1. Kept separate for discoverability.

if (-not (Test-Path .\start.ps1)) {
    Write-Error "start.ps1 not found in project root."
    exit 1
}

.\start.ps1<#


param(
    [switch]$AutoLoad
)

Write-Host "[run-local] iniciando..." -ForegroundColor Cyan

$projectRoot = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
Set-Location $projectRoot

# Verifica Python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Python não encontrado no PATH. Instale Python 3.10+ e reabra o PowerShell."
    exit 1
}

# Cria virtualenv se não existir
if (-not (Test-Path ".venv")) {
    Write-Host "Criando virtualenv .venv..."
    python -m venv .venv
}

Write-Host "Ativando virtualenv..."
& .\.venv\Scripts\Activate.ps1

Write-Host "Atualizando pip e instalando dependências (requirements.txt)..."
pip install --upgrade pip
pip install -r requirements.txt

if ($AutoLoad) {
    Write-Host "AUTO_LOAD ativado - a aplicação irá tentar carregar CSV no startup" -ForegroundColor Yellow
    $env:AUTO_LOAD = 'true'
}

Write-Host "Iniciando Uvicorn em http://127.0.0.1:8000 (CTRL+C para parar)" -ForegroundColor Green
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
