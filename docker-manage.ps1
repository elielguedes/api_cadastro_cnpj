# Script PowerShell para gerenciar Docker Compose da API FastAPI
# Usage: .\docker-manage.ps1 [up|down|rebuild|logs]

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("up", "down", "rebuild", "logs", "status")]
    [string]$Action = "up"
)

Write-Host "🐳 FastAPI Docker Manager" -ForegroundColor Cyan
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
    Write-Host "❌ Docker Desktop não está rodando!" -ForegroundColor Red
    Write-Host "📋 Para iniciar o Docker Desktop:" -ForegroundColor Yellow
    Write-Host "   1. Abra o Docker Desktop" -ForegroundColor White
    Write-Host "   2. Aguarde ele inicializar completamente" -ForegroundColor White
    Write-Host "   3. Execute este script novamente" -ForegroundColor White
    
    # Tentar iniciar Docker Desktop automaticamente
    $dockerPath = "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    if (Test-Path $dockerPath) {
        Write-Host "🚀 Tentando iniciar Docker Desktop..." -ForegroundColor Green
        Start-Process $dockerPath
        Write-Host "⏳ Aguarde alguns segundos e execute o script novamente" -ForegroundColor Yellow
    }
    exit 1
}

Write-Host "✅ Docker Desktop está rodando" -ForegroundColor Green

# Executar ações
switch ($Action) {
    "up" {
        Write-Host "🚀 Iniciando containers..." -ForegroundColor Green
        docker-compose up --build
    }
    "down" {
        Write-Host "🛑 Parando containers..." -ForegroundColor Yellow
        docker-compose down
    }
    "rebuild" {
        Write-Host "🔄 Rebuild completo..." -ForegroundColor Blue
        docker-compose down -v
        if ($LASTEXITCODE -eq 0) {
            docker-compose up --build
        }
    }
    "logs" {
        Write-Host "📋 Mostrando logs..." -ForegroundColor Cyan
        docker-compose logs -f
    }
    "status" {
        Write-Host "📊 Status dos containers..." -ForegroundColor Magenta
        docker-compose ps
    }
}

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Operação concluída com sucesso!" -ForegroundColor Green
} else {
    Write-Host "❌ Erro durante a operação" -ForegroundColor Red
}