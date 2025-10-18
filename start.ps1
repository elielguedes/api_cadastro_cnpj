# start.ps1
# Helper to activate the project's virtualenv, apply migrations and run the app locally.
# Usage (PowerShell):
#   .\start.ps1

Write-Host "== start.ps1: starting local app helper =="

$venvActivate = Join-Path -Path (Resolve-Path .).Path -ChildPath ".venv\Scripts\Activate.ps1"
if (Test-Path $venvActivate) {
    Write-Host "Activating virtualenv: $venvActivate"
    & $venvActivate
} else {
    Write-Host ".venv not found. Creating virtualenv and installing dependencies..."
    python -m venv .venv
    & $venvActivate
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
}

# ensure imports work for local runs
$env:PYTHONPATH = (Resolve-Path .).Path

Write-Host "Applying Alembic migrations (if any)"
try {
    python -m alembic upgrade head
} catch {
    Write-Warning "Alembic upgrade failed or not configured in this environment: $_"
}

Write-Host "Starting uvicorn on http://127.0.0.1:8000 (use Ctrl+C to stop)"
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
<#
Start.ps1 — script de inicialização inteligente para Windows PowerShell

Comportamento:
- Tenta usar Docker (daemon) executando `docker info`.
- Se o daemon estiver OK, executa `docker compose -f .\docker-compose.yml up --build`.
- Caso contrário, cria/ativa um ambiente virtual `.venv`, instala dependências e inicia `uvicorn` localmente.

Uso:
- Executar com PowerShell (recomendado abrir o terminal como Administrador se quiser usar Docker Desktop):
    .\start.ps1             # tenta Docker, senão fallback local
    .\start.ps1 -AutoLoad   # seta AUTO_LOAD=true antes de iniciar a app (carrega CSV no startup)

Observações:
- Este script NÃO apaga ou modifica arquivos Docker do projeto — apenas os usa quando o daemon está disponível.
- Requer Python 3.x no PATH.
#>

param(
    [switch]$AutoLoad
)

Write-Host "[start.ps1] Iniciando modo local (venv + uvicorn)..."

# Criar venv se não existir
if (-not (Test-Path -Path .\.venv)) {
    Write-Host "[start.ps1] Criando virtualenv ./.venv..."
    python -m venv .\.venv
}

Write-Host "[start.ps1] Ativando .venv..."
& .\.venv\Scripts\Activate.ps1

Write-Host "[start.ps1] Instalando dependências (requirements.txt)..."
pip install --upgrade pip
pip install -r requirements.txt

if ($AutoLoad) {
    Write-Host "[start.ps1] AUTO_LOAD habilitado"
    $env:AUTO_LOAD = "true"
}

Write-Host "[start.ps1] Iniciando uvicorn: app.main:app em 0.0.0.0:8000"
uvicorn app.main:app --host 0.0.0.0 --port 8000
