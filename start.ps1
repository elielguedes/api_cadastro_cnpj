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
