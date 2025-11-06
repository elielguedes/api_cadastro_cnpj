# 🌐 Create ngrok Tunnel
# Cria túnel público para aplicação local

Write-Host "🌐 Criando túnel público com ngrok..." -ForegroundColor Green

# Verificar se ngrok existe
if (Test-Path "ngrok.exe") {
    Write-Host "✅ ngrok encontrado!" -ForegroundColor Green
} elseif (Get-Command ngrok -ErrorAction SilentlyContinue) {
    Write-Host "✅ ngrok instalado no sistema!" -ForegroundColor Green
} else {
    Write-Host "❌ ngrok não encontrado!" -ForegroundColor Red
    Write-Host "📥 Baixe em: https://ngrok.com/download" -ForegroundColor Yellow
    Write-Host "📂 Extraia neste diretório ou instale globalmente" -ForegroundColor Yellow
    Read-Host "Pressione Enter para continuar mesmo assim..."
}

Write-Host "🔗 Criando túnel para porta 8000..." -ForegroundColor Cyan
Write-Host "⚡ Aguarde o link público aparecer..." -ForegroundColor Cyan
Write-Host ""
Write-Host "🎯 Depois de ver o link, acesse:" -ForegroundColor Yellow
Write-Host "   📖 Documentação: https://seu-link.ngrok.io/docs" -ForegroundColor White
Write-Host "   ⚡ Lambda Status: https://seu-link.ngrok.io/lambda/functions/status" -ForegroundColor White
Write-Host ""

# Tentar executar ngrok
try {
    if (Test-Path "ngrok.exe") {
        .\ngrok.exe http 8000
    } else {
        ngrok http 8000
    }
} catch {
    Write-Host "❌ Erro ao executar ngrok: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "📥 Baixe ngrok em: https://ngrok.com/download" -ForegroundColor Yellow
}