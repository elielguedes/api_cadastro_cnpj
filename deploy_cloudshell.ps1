# 🚀 Deploy AWS Lambda - Sem configurar credenciais locais
# Execução via CloudShell (mais rápido e direto)

Write-Host "🔥 DEPLOY AWS LAMBDA - CLOUDSHELL" -ForegroundColor Red
Write-Host "=================================" -ForegroundColor Yellow

Write-Host ""
Write-Host "🎯 INSTRUÇÕES RÁPIDAS:" -ForegroundColor Green
Write-Host "1. Vou abrir o AWS Console CloudShell" -ForegroundColor Cyan
Write-Host "2. Copie e cole o script que vou mostrar" -ForegroundColor Cyan
Write-Host "3. Aguarde o deploy automático" -ForegroundColor Cyan
Write-Host "4. Configure o FastAPI para usar Lambda real" -ForegroundColor Cyan

Write-Host ""
Write-Host "⏳ Aguarde 3 segundos..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# Abrir AWS Console CloudShell
Write-Host "🌐 Abrindo AWS Console CloudShell..." -ForegroundColor Green
Start-Process "https://console.aws.amazon.com/cloudshell/home?region=us-east-2"

Write-Host ""
Write-Host "📋 SCRIPT PARA CLOUDSHELL:" -ForegroundColor Yellow
Write-Host "==========================" -ForegroundColor Yellow

$script_content = @"
# Cole este script no CloudShell:

# 1. Download do script
curl -L -o deploy.sh https://raw.githubusercontent.com/elielguedes/Relatorio_Eliel_Guedes/main/framework_udf/cloudshell_deploy.sh

# 2. Tornar executável
chmod +x deploy.sh

# 3. Executar deploy
./deploy.sh
"@

Write-Host $script_content -ForegroundColor White

Write-Host ""
Write-Host "📋 ALTERNATIVA (SCRIPT DIRETO):" -ForegroundColor Yellow
Write-Host "===============================" -ForegroundColor Yellow

# Ler o conteúdo do script para mostrar
$deploy_script = Get-Content "cloudshell_deploy.sh" -Raw

Write-Host "# Cole este script completo no CloudShell:" -ForegroundColor Cyan
Write-Host $deploy_script -ForegroundColor White

Write-Host ""
Write-Host "✅ APÓS O DEPLOY NO CLOUDSHELL:" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Yellow

Write-Host "1. Configure o FastAPI para usar Lambda real:" -ForegroundColor Cyan
Write-Host "   Arquivo: app/services/lambda_service.py" -ForegroundColor Gray
Write-Host "   Mude: simulate=False" -ForegroundColor Gray

Write-Host ""
Write-Host "2. Restart o FastAPI:" -ForegroundColor Cyan
Write-Host "   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000" -ForegroundColor Gray

Write-Host ""
Write-Host "3. Teste as funções Lambda:" -ForegroundColor Cyan
Write-Host "   http://localhost:8000/lambda/functions/status" -ForegroundColor Gray

Write-Host ""
Write-Host "🎯 PRESSIONE QUALQUER TECLA PARA CONTINUAR..." -ForegroundColor Red
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Write-Host ""
Write-Host "🔧 Configurando FastAPI para usar Lambda real..." -ForegroundColor Green

# Configurar o FastAPI automaticamente
$lambda_service_path = "app\services\lambda_service.py"

if (Test-Path $lambda_service_path) {
    Write-Host "📝 Atualizando lambda_service.py..." -ForegroundColor Yellow
    
    # Ler o arquivo
    $content = Get-Content $lambda_service_path -Raw
    
    # Substituir simulate=True por simulate=False
    $updated_content = $content -replace "simulate\s*=\s*True", "simulate=False"
    
    # Salvar o arquivo
    Set-Content $lambda_service_path -Value $updated_content
    
    Write-Host "✅ FastAPI configurado para usar Lambda real!" -ForegroundColor Green
} else {
    Write-Host "⚠️  Arquivo lambda_service.py não encontrado" -ForegroundColor Yellow
    Write-Host "   Verifique se o caminho está correto" -ForegroundColor Gray
}

Write-Host ""
Write-Host "🚀 PRONTO PARA INICIAR FASTAPI?" -ForegroundColor Green
Write-Host "Pressione ENTER para iniciar ou CTRL+C para cancelar"
Read-Host

# Iniciar FastAPI
Write-Host "Iniciando FastAPI com Lambda AWS..." -ForegroundColor Red
& python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000