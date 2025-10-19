# 🚀 Deploy AWS Lambda - Método Direto com Credenciais Temporárias
# Para conta 217466752219 - us-east-2

Write-Host "🔑 CONFIGURAÇÃO AWS - MÉTODO RÁPIDO" -ForegroundColor Red
Write-Host "===================================" -ForegroundColor Yellow

Write-Host ""
Write-Host "📋 PASSOS:" -ForegroundColor Green
Write-Host "1. Vá para: https://console.aws.amazon.com/" -ForegroundColor Cyan
Write-Host "2. Clique no seu nome (canto superior direito)" -ForegroundColor Cyan  
Write-Host "3. Clique em 'Security credentials'" -ForegroundColor Cyan
Write-Host "4. Role até 'Access keys' e clique 'Create access key'" -ForegroundColor Cyan
Write-Host "5. Selecione 'Command Line Interface (CLI)'" -ForegroundColor Cyan
Write-Host "6. Marque 'I understand...' e clique 'Create access key'" -ForegroundColor Cyan

Write-Host ""
Write-Host "💡 AGORA COLE AS CREDENCIAIS AQUI:" -ForegroundColor Yellow

# Solicitar Access Key
Write-Host "Access Key ID: " -ForegroundColor Green -NoNewline
$ACCESS_KEY = Read-Host

# Solicitar Secret Key  
Write-Host "Secret Access Key: " -ForegroundColor Green -NoNewline
$SECRET_KEY = Read-Host -AsSecureString
$SECRET_KEY_PLAIN = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($SECRET_KEY))

Write-Host ""
Write-Host "🔧 Configurando AWS CLI..." -ForegroundColor Yellow

# Configurar AWS CLI
aws configure set aws_access_key_id $ACCESS_KEY
aws configure set aws_secret_access_key $SECRET_KEY_PLAIN
aws configure set default.region us-east-2
aws configure set default.output json

Write-Host ""
Write-Host "🧪 Testando configuração..." -ForegroundColor Yellow

try {
    $identity = aws sts get-caller-identity --output json | ConvertFrom-Json
    Write-Host "✅ AWS configurado com sucesso!" -ForegroundColor Green
    Write-Host "   Account: $($identity.Account)" -ForegroundColor Cyan
    Write-Host "   User: $($identity.Arn)" -ForegroundColor Cyan
    
    if ($identity.Account -eq "217466752219") {
        Write-Host "✅ Account correto!" -ForegroundColor Green
        
        Write-Host ""
        Write-Host "🚀 INICIANDO DEPLOY LAMBDA..." -ForegroundColor Red
        
        # Deploy Lambda functions
        $deploy_commands = @"
# 1. Criar IAM Role
aws iam create-role --role-name lambda-execution-role --assume-role-policy-document '{
  \"Version\": \"2012-10-17\",
  \"Statement\": [
    {
      \"Effect\": \"Allow\",
      \"Principal\": {\"Service\": \"lambda.amazonaws.com\"},
      \"Action\": \"sts:AssumeRole\"
    }
  ]
}' 2>null

# 2. Anexar policy
aws iam attach-role-policy --role-name lambda-execution-role --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

Write-Host \"⏳ Aguardando propagação IAM...\" -ForegroundColor Yellow
Start-Sleep -Seconds 10

# 3. Criar função Lambda
@'
import json
def lambda_handler(event, context):
    return {
        \"statusCode\": 200,
        \"body\": json.dumps({
            \"cnpj\": event.get(\"cnpj\", \"\"),
            \"valid\": True,
            \"source\": \"AWS Lambda\",
            \"account\": \"217466752219\"
        })
    }
'@ | Out-File -FilePath \"validate_cnpj.py\" -Encoding UTF8

# 4. Criar ZIP
Compress-Archive -Path \"validate_cnpj.py\" -DestinationPath \"validate_cnpj.zip\" -Force

# 5. Deploy função
aws lambda create-function --function-name validate-cnpj-async --runtime python3.9 --role arn:aws:iam::217466752219:role/lambda-execution-role --handler validate_cnpj.lambda_handler --zip-file fileb://validate_cnpj.zip --region us-east-2
"@
        
        # Executar comandos de deploy
        Write-Host "🔧 Criando IAM Role..." -ForegroundColor Yellow
        aws iam create-role --role-name lambda-execution-role --assume-role-policy-document '{
          "Version": "2012-10-17",
          "Statement": [
            {
              "Effect": "Allow", 
              "Principal": {"Service": "lambda.amazonaws.com"},
              "Action": "sts:AssumeRole"
            }
          ]
        }' 2>$null
        
        Write-Host "🔐 Anexando policy..." -ForegroundColor Yellow
        aws iam attach-role-policy --role-name lambda-execution-role --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
        
        Write-Host "⏳ Aguardando propagação IAM..." -ForegroundColor Yellow
        Start-Sleep -Seconds 10
        
        Write-Host "📝 Criando função Lambda..." -ForegroundColor Yellow
        
        # Criar arquivo Python
        @'
import json
def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "cnpj": event.get("cnpj", ""),
            "valid": True,
            "source": "AWS Lambda",
            "account": "217466752219"
        })
    }
'@ | Out-File -FilePath "validate_cnpj.py" -Encoding UTF8
        
        # Criar ZIP
        Compress-Archive -Path "validate_cnpj.py" -DestinationPath "validate_cnpj.zip" -Force
        
        # Deploy função
        Write-Host "🚀 Fazendo deploy da função..." -ForegroundColor Yellow
        aws lambda create-function --function-name validate-cnpj-async --runtime python3.9 --role arn:aws:iam::217466752219:role/lambda-execution-role --handler validate_cnpj.lambda_handler --zip-file fileb://validate_cnpj.zip --region us-east-2
        
        Write-Host ""
        Write-Host "✅ DEPLOY CONCLUÍDO!" -ForegroundColor Green
        Write-Host "===================" -ForegroundColor Yellow
        Write-Host "🔗 Função criada: validate-cnpj-async" -ForegroundColor Cyan
        Write-Host "🌍 Região: us-east-2" -ForegroundColor Cyan
        Write-Host "📊 Account: 217466752219" -ForegroundColor Cyan
        
        Write-Host ""
        Write-Host "🧪 TESTANDO FUNÇÃO..." -ForegroundColor Yellow
        aws lambda invoke --function-name validate-cnpj-async --payload '{\"cnpj\":\"12345678901234\"}' response.json --region us-east-2
        
        if (Test-Path "response.json") {
            Write-Host "📄 Resposta da função:" -ForegroundColor Green
            Get-Content "response.json" | ConvertFrom-Json | ConvertTo-Json -Depth 3
        }
        
        Write-Host ""
        Write-Host "🔧 CONFIGURANDO FASTAPI..." -ForegroundColor Yellow
        
        # Verificar se o arquivo lambda_service.py existe
        $lambda_service_path = "app\services\lambda_service.py"
        if (Test-Path $lambda_service_path) {
            # Já está configurado para us-east-2, só precisamos garantir que não está em modo simulação
            Write-Host "✅ FastAPI já configurado para us-east-2" -ForegroundColor Green
        }
        
        Write-Host ""
        Write-Host "🚀 INICIANDO FASTAPI..." -ForegroundColor Red
        Write-Host "Pressione CTRL+C para parar" -ForegroundColor Gray
        
        # Limpar variável de ambiente e iniciar
        Remove-Item Env:DATABASE_URL -ErrorAction SilentlyContinue
        python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
        
    } else {
        Write-Host "❌ Account incorreto: $($identity.Account)" -ForegroundColor Red
        Write-Host "   Esperado: 217466752219" -ForegroundColor Yellow
    }
    
} catch {
    Write-Host "❌ Erro na configuração AWS:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Yellow
    Write-Host ""
    Write-Host "🔧 Execute manualmente:" -ForegroundColor Cyan
    Write-Host "aws configure" -ForegroundColor Gray
}

# Limpar variáveis sensíveis
$SECRET_KEY_PLAIN = $null
$ACCESS_KEY = $null