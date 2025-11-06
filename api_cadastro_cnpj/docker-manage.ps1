# Script PowerShell para gerenciar Docker Compose da API FastAPI
# Usage: .\docker-manage.ps1 [up|down|rebuild|logs]

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("up", "down", "rebuild", "logs", "status", "db-only", "basic", "check", "install-wsl")]
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
    "basic" {
        Write-Host "[BASIC] Iniciando versão básica (sem health checks)..." -ForegroundColor Cyan
        docker-compose -f docker-compose.basic.yml up --build
    }
    "check" {
        Write-Host "[CHECK] Verificando configuração Docker/WSL..." -ForegroundColor Magenta
        Write-Host "=== WSL Status ===" -ForegroundColor Yellow
        wsl --version
        wsl --list
        Write-Host "=== Docker Status ===" -ForegroundColor Yellow
        docker --version
        docker info
        Write-Host "=== Docker Compose Test ===" -ForegroundColor Yellow
        docker-compose config
    }
    "install-wsl" {
        Write-Host "[INSTALL] Configurando WSL2 para Docker..." -ForegroundColor Green
        Write-Host "1. Habilitando Plataforma VM..." -ForegroundColor Yellow
        Enable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform -All -NoRestart
        Write-Host "2. Baixando kernel WSL2..." -ForegroundColor Yellow
        Invoke-WebRequest -Uri "https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi" -OutFile "wsl_update_x64.msi"
        Write-Host "3. Instalando kernel..." -ForegroundColor Yellow
        Start-Process msiexec.exe -Wait -ArgumentList '/i wsl_update_x64.msi /quiet'
        Write-Host "4. Configurando WSL2..." -ForegroundColor Yellow
        wsl --set-default-version 2
        Write-Host "[OK] WSL2 configurado! Reinicie o Docker Desktop." -ForegroundColor Green
    }
}

if ($LASTEXITCODE -eq 0) {
    Write-Host "[SUCCESS] Operação concluída com sucesso!" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Erro durante a operação" -ForegroundColor Red
}