# 🚀 Start FastAPI Application
# Executa a aplicação FastAPI com SQLite local

Write-Host "🚀 Iniciando aplicação FastAPI..." -ForegroundColor Green
Write-Host "📍 Diretório: $PWD" -ForegroundColor Yellow

# Configurar para usar SQLite (remove DATABASE_URL)
Remove-Item Env:DATABASE_URL -ErrorAction SilentlyContinue
$env:DATABASE_URL = $null

# Verificar se está no ambiente virtual
if ($env:VIRTUAL_ENV) {
    Write-Host "✅ Ambiente virtual ativo: $env:VIRTUAL_ENV" -ForegroundColor Green
} else {
    Write-Host "⚠️  Ambiente virtual não detectado" -ForegroundColor Yellow
}

# Iniciar aplicação
Write-Host "🔧 Forçando uso do SQLite..." -ForegroundColor Cyan
Write-Host "⚡ Iniciando servidor na porta 8000..." -ForegroundColor Cyan
Write-Host "📖 Documentação estará em: http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host ""

python -m uvicorn app.main:app --reload --port 8000 --host 0.0.0.0

Write-Host "❌ Aplicação encerrada." -ForegroundColor Red