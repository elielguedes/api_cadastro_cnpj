# 🚀 Deploy AWS Lambda - PowerShell Script
# Projeto: Framework UDF
# Autor: Eliel Guedes

Write-Host "🚀 Iniciando deploy das funções AWS Lambda..." -ForegroundColor Green

# Verificar se AWS CLI está instalado
try {
    aws --version
    Write-Host "✅ AWS CLI detectado" -ForegroundColor Green
} catch {
    Write-Host "❌ AWS CLI não encontrado. Instale primeiro: winget install Amazon.AWSCLI" -ForegroundColor Red
    exit 1
}

# Verificar credenciais AWS
Write-Host "🔍 Verificando credenciais AWS..."
try {
    $identity = aws sts get-caller-identity --output json | ConvertFrom-Json
    Write-Host "✅ Conectado como: $($identity.UserId)" -ForegroundColor Green
} catch {
    Write-Host "❌ Credenciais AWS não configuradas. Execute: aws configure" -ForegroundColor Red
    exit 1
}

# Criar diretório temporário
$tempDir = ".\temp_lambda_deploy"
if (Test-Path $tempDir) {
    Remove-Item $tempDir -Recurse -Force
}
New-Item -ItemType Directory -Path $tempDir | Out-Null

Write-Host "📦 Preparando funções Lambda..."

# Função 1: Validador CNPJ
Write-Host "📋 Deploy: validate-cnpj-api"
Copy-Item "validate_cnpj.py" "$tempDir\"
Set-Location $tempDir
Compress-Archive -Path "validate_cnpj.py" -DestinationPath "validate-cnpj.zip" -Force

try {
    aws lambda create-function `
        --function-name validate-cnpj-api `
        --runtime python3.9 `
        --role "arn:aws:iam::${identity.Account}:role/lambda-execution-role" `
        --handler validate_cnpj.lambda_handler `
        --zip-file fileb://validate-cnpj.zip `
        --timeout 30 `
        --memory-size 128 `
        --description "Validação de CNPJ via ReceitaWS API"
    Write-Host "✅ validate-cnpj-api deployada" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Função validate-cnpj-api pode já existir, tentando update..." -ForegroundColor Yellow
    aws lambda update-function-code `
        --function-name validate-cnpj-api `
        --zip-file fileb://validate-cnpj.zip
}

Set-Location ..

# Função 2: Processador CSV
Write-Host "📋 Deploy: import-csv-processor"
Set-Location $tempDir
Remove-Item * -Force
Copy-Item "..\import_csv.py" .
Copy-Item "..\requirements.txt" .

# Instalar dependências
pip install -r requirements.txt -t . --quiet

Compress-Archive -Path "*" -DestinationPath "import-csv.zip" -Force

try {
    aws lambda create-function `
        --function-name import-csv-processor `
        --runtime python3.9 `
        --role "arn:aws:iam::${identity.Account}:role/lambda-execution-role" `
        --handler import_csv.lambda_handler `
        --zip-file fileb://import-csv.zip `
        --timeout 300 `
        --memory-size 512 `
        --description "Processamento de arquivos CSV com S3"
    Write-Host "✅ import-csv-processor deployada" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Função import-csv-processor pode já existir, tentando update..." -ForegroundColor Yellow
    aws lambda update-function-code `
        --function-name import-csv-processor `
        --zip-file fileb://import-csv.zip
}

Set-Location ..

# Função 3: Gerador de Relatórios
Write-Host "📋 Deploy: generate-reports"
Set-Location $tempDir
Remove-Item * -Force
Copy-Item "..\generate_reports.py" .

Compress-Archive -Path "generate_reports.py" -DestinationPath "generate-reports.zip" -Force

try {
    aws lambda create-function `
        --function-name generate-reports `
        --runtime python3.9 `
        --role "arn:aws:iam::${identity.Account}:role/lambda-execution-role" `
        --handler generate_reports.lambda_handler `
        --zip-file fileb://generate-reports.zip `
        --timeout 120 `
        --memory-size 256 `
        --description "Geração de relatórios estatísticos com SNS"
    Write-Host "✅ generate-reports deployada" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Função generate-reports pode já existir, tentando update..." -ForegroundColor Yellow
    aws lambda update-function-code `
        --function-name generate-reports `
        --zip-file fileb://generate-reports.zip
}

Set-Location ..

# Limpeza
Remove-Item $tempDir -Recurse -Force

Write-Host ""
Write-Host "🎉 Deploy concluído!" -ForegroundColor Green
Write-Host "📋 Funções criadas:"
Write-Host "   • validate-cnpj-api" -ForegroundColor Cyan
Write-Host "   • import-csv-processor" -ForegroundColor Cyan  
Write-Host "   • generate-reports" -ForegroundColor Cyan

Write-Host ""
Write-Host "🔧 Próximo passo: Configurar FastAPI para usar Lambda real"
Write-Host "   1. Editar app/services/lambda_service.py"
Write-Host "   2. Trocar simulate=True por simulate=False"
Write-Host "   3. Reiniciar servidor FastAPI"

Write-Host ""
Write-Host "🧪 Teste as funções em: http://127.0.0.1:8000/docs" -ForegroundColor Yellow

# Listar funções deployadas
Write-Host ""
Write-Host "📊 Status das funções Lambda:" -ForegroundColor Yellow
aws lambda list-functions --query 'Functions[?starts_with(FunctionName, `validate-cnpj`) || starts_with(FunctionName, `import-csv`) || starts_with(FunctionName, `generate-reports`)].{Name:FunctionName,Runtime:Runtime,LastModified:LastModified}' --output table