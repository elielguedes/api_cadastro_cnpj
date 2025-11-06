# Script PowerShell para Deploy Automatico
# Executa: .\deploy-setup.ps1

Write-Host "CONFIGURANDO DEPLOY GRATUITO - API FASTAPI" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green

# Verifica se Git esta instalado
if (!(Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "Git nao encontrado! Instale: https://git-scm.com" -ForegroundColor Red
    exit 1
}

# Verifica se esta em repositorio Git
if (!(Test-Path .git)) {
    Write-Host "Inicializando repositorio Git..." -ForegroundColor Yellow
    git init
    git add .
    git commit -m "Initial commit - FastAPI Empresas API"
}

Write-Host "Projeto configurado para deploy!" -ForegroundColor Green
Write-Host ""

Write-Host "OPCOES DE DEPLOY GRATUITO:" -ForegroundColor Cyan
Write-Host "==========================" -ForegroundColor Cyan
Write-Host ""

Write-Host "1. RENDER (RECOMENDADO)" -ForegroundColor Green
Write-Host "   - 750 horas/mes GRATIS"
Write-Host "   - Deploy automatico via GitHub"
Write-Host "   - URL: https://render.com"
Write-Host "   - Comando: pip install -r requirements.txt"
Write-Host "   - Start: uvicorn app.main:app --host 0.0.0.0 --port" '$PORT'
Write-Host ""

Write-Host "2. RAILWAY" -ForegroundColor Blue
Write-Host "   - 5 dolares/mes credito GRATIS"
Write-Host "   - Deploy em segundos"
Write-Host "   - URL: https://railway.app"
Write-Host ""

Write-Host "3. FLY.IO" -ForegroundColor Magenta
Write-Host "   - 3 apps gratuitas"
Write-Host "   - Regiao Sao Paulo"
Write-Host "   - URL: https://fly.io"
Write-Host ""

Write-Host "PROXIMOS PASSOS:" -ForegroundColor Yellow
Write-Host "=================" -ForegroundColor Yellow
Write-Host "1. Envie codigo para GitHub:"
Write-Host "   git remote add origin https://github.com/SEU_USUARIO/SEU_REPO.git"
Write-Host "   git branch -M main"
Write-Host "   git push -u origin main"
Write-Host ""
Write-Host "2. Escolha uma plataforma acima"
Write-Host "3. Conecte seu repositorio GitHub"
Write-Host "4. Configure conforme instrucoes"
Write-Host "5. Deploy automatico!"
Write-Host ""

Write-Host "Leia o guia completo em: DEPLOY_GRATUITO.md" -ForegroundColor Cyan
Write-Host ""

Write-Host "TUDO PRONTO! Sua API FastAPI esta configurada para deploy gratuito!" -ForegroundColor Green

# Pausa para ver as instrucoes
Read-Host "Pressione Enter para continuar..."