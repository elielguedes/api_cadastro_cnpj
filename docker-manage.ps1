# Script PowerShell para gerenciar Docker Compose da API FastAPI
# Usage: .\docker-manage.ps1 [up|down|rebuild|logs]

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("up", "down", "rebuild", "logs", "status", "db-only")]
    [string]$Action = "up"
)

Write-Host "[DOCKER] FastAPI Docker Manager" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

# Função para verificar se Docker Desktop está rodando
function Test-DockerRunning {
    try {
        docker version | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

# Verificar se Docker está rodando
if (-not (Test-DockerRunning)) {
    Write-Host "[ERROR] Docker Desktop não está rodando!" -ForegroundColor Red
    Write-Host "[HELP] Para iniciar o Docker Desktop:" -ForegroundColor Yellow
    Write-Host "   1. Abra o Docker Desktop" -ForegroundColor White
    Write-Host "   2. Aguarde ele inicializar completamente" -ForegroundColor White
    Write-Host "   3. Execute este script novamente" -ForegroundColor White
    
    # Tentar iniciar Docker Desktop automaticamente
    $dockerPath = "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    if (Test-Path $dockerPath) {
        Write-Host "[AUTO] Tentando iniciar Docker Desktop..." -ForegroundColor Green
        Start-Process $dockerPath
        Write-Host "[WAIT] Aguarde alguns segundos e execute o script novamente" -ForegroundColor Yellow
    }
    exit 1
}

Write-Host "[OK] Docker Desktop está rodando" -ForegroundColor Green

# Executar ações
switch ($Action) {
    "up" {
        Write-Host "[START] Iniciando containers..." -ForegroundColor Green
        docker-compose up --build
    }
    "down" {
        Write-Host "[STOP] Parando containers..." -ForegroundColor Yellow
        docker-compose down
    }
    "rebuild" {
        Write-Host "[REBUILD] Rebuild completo..." -ForegroundColor Blue
        docker-compose down -v
        if ($LASTEXITCODE -eq 0) {
            docker-compose up --build
        }
    }
    "logs" {
        Write-Host "[LOGS] Mostrando logs..." -ForegroundColor Cyan
        docker-compose logs -f
    }
    "status" {
        Write-Host "[STATUS] Status dos containers..." -ForegroundColor Magenta
        docker-compose ps
    }
    "db-only" {
        Write-Host "[DB] Iniciando apenas PostgreSQL..." -ForegroundColor Blue
        docker-compose -f docker-compose.simple.yml up -d
    }
}

if ($LASTEXITCODE -eq 0) {
    Write-Host "[SUCCESS] Operação concluída com sucesso!" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Erro durante a operação" -ForegroundColor Red
}