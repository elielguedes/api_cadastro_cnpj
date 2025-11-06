# 🚀 Configuração AWS - SOLUÇÃO ESPECÍFICA

**Sua Conta AWS**: 217466752219  
**EC2**: i-063d58d8309714c44 (us-east-2)  
**Status**: Root account sem Access Keys ativas

## 🎯 **PASSO A PASSO PARA CONFIGURAR**

### **📋 Situação Atual:**
- ✅ Conta AWS ativa (Account: 217466752219)
- ✅ EC2 rodando (18.118.167.28)
- ❌ Access Keys não configuradas
- ❌ AWS CLI sem credenciais

---

## 🔧 **SOLUÇÃO 1: AWS Console (5 minutos)**

### **1. Login AWS Console**
```
🌐 URL: https://console.aws.amazon.com/
📧 Login: Email da conta root
🔑 Senha: Senha da conta AWS
```

### **2. Criar Access Key**
```
1. No AWS Console, clicar no nome do usuário (canto superior direito)
2. "Security Credentials"
3. "Access Keys" section
4. "Create New Access Key"
5. ⚠️ Warning sobre root account - "Continue to Create Access Key"
6. Copiar ou Download:
   - Access Key ID (ex: AKIA...)
   - Secret Access Key (ex: ...)
```

### **3. Configurar no seu PC**
```powershell
aws configure

# Quando aparecer cada prompt:
AWS Access Key ID [None]: [colar Access Key ID]
AWS Secret Access Key [None]: [colar Secret Access Key]  
Default region name [None]: us-east-2
Default output format [None]: json
```

### **4. Testar configuração**
```powershell
aws sts get-caller-identity
# Deve retornar: Account: 217466752219
```

---

## 🔧 **SOLUÇÃO 2: CloudShell (2 minutos)**

### **1. Abrir CloudShell no AWS Console**
```
1. Login no AWS Console
2. Procurar "CloudShell" na barra de pesquisa
3. Ou clicar no ícone de terminal (>_)
4. Aguardar carregar o terminal web
```

### **2. Deploy direto no CloudShell**
```bash
# Já tem credenciais automaticamente!
git clone https://github.com/elielguedes/Relatorio_Eliel_Guedes.git
cd Relatorio_Eliel_Guedes/framework_udf/lambda_functions

# Executar deploy
chmod +x deploy.sh
./deploy.sh
```

---

## ⚡ **DEPLOY IMEDIATO (Após configurar)**

### **Script automático:**
```powershell
# Salvar como deploy_now.ps1
Write-Host "🚀 Deploy AWS Lambda - Account 217466752219" -ForegroundColor Green

# Verificar credenciais
try {
    $identity = aws sts get-caller-identity --output json | ConvertFrom-Json
    if ($identity.Account -eq "217466752219") {
        Write-Host "✅ Credenciais corretas!" -ForegroundColor Green
        Write-Host "📍 Account: $($identity.Account)" -ForegroundColor Cyan
        Write-Host "📍 Region: us-east-2" -ForegroundColor Cyan
    } else {
        Write-Host "❌ Account incorreto: $($identity.Account)" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ Credenciais AWS não configuradas!" -ForegroundColor Red
    Write-Host "🔧 Execute: aws configure" -ForegroundColor Yellow
    Write-Host "📖 Ou use CloudShell no AWS Console" -ForegroundColor Yellow
    exit 1
}

# Criar IAM role para Lambda
Write-Host "🔧 Criando IAM role..." -ForegroundColor Yellow
try {
    aws iam create-role --role-name lambda-execution-role --assume-role-policy-document '{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"Service": "lambda.amazonaws.com"},
                "Action": "sts:AssumeRole"
            }
        ]
    }' --region us-east-2
    
    aws iam attach-role-policy --role-name lambda-execution-role --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole --region us-east-2
    
    Write-Host "✅ IAM role criada!" -ForegroundColor Green
} catch {
    Write-Host "⚠️  IAM role pode já existir" -ForegroundColor Yellow
}

# Deploy Lambda functions
Write-Host "🚀 Deploy das funções Lambda..." -ForegroundColor Green
cd lambda_functions

# Função 1: Validador CNPJ
Write-Host "📋 Deploy: validate-cnpj-api" -ForegroundColor Cyan
Compress-Archive -Path validate_cnpj.py -DestinationPath validate-cnpj.zip -Force

aws lambda create-function `
    --function-name validate-cnpj-api `
    --runtime python3.9 `
    --role "arn:aws:iam::217466752219:role/lambda-execution-role" `
    --handler validate_cnpj.lambda_handler `
    --zip-file fileb://validate-cnpj.zip `
    --timeout 30 `
    --memory-size 128 `
    --region us-east-2

# Função 2: Processador CSV  
Write-Host "📋 Deploy: import-csv-processor" -ForegroundColor Cyan
pip install requests boto3 -t . --quiet
Compress-Archive -Path import_csv.py,requests,boto3 -DestinationPath import-csv.zip -Force

aws lambda create-function `
    --function-name import-csv-processor `
    --runtime python3.9 `
    --role "arn:aws:iam::217466752219:role/lambda-execution-role" `
    --handler import_csv.lambda_handler `
    --zip-file fileb://import-csv.zip `
    --timeout 300 `
    --memory-size 512 `
    --region us-east-2

# Função 3: Gerador Relatórios
Write-Host "📋 Deploy: generate-reports" -ForegroundColor Cyan  
Compress-Archive -Path generate_reports.py -DestinationPath generate-reports.zip -Force

aws lambda create-function `
    --function-name generate-reports `
    --runtime python3.9 `
    --role "arn:aws:iam::217466752219:role/lambda-execution-role" `
    --handler generate_reports.lambda_handler `
    --zip-file fileb://generate-reports.zip `
    --timeout 120 `
    --memory-size 256 `
    --region us-east-2

Write-Host "🎉 Deploy concluído!" -ForegroundColor Green
Write-Host "📋 Verificar funções:" -ForegroundColor Yellow
aws lambda list-functions --region us-east-2 --query 'Functions[].FunctionName'

Write-Host "🔗 Próximo: Configurar FastAPI para usar Lambda real" -ForegroundColor Cyan
```

---

## 🧪 **VERIFICAR DEPLOY**

### **Após configurar credenciais:**
```powershell
# Testar acesso
aws sts get-caller-identity

# Verificar EC2
aws ec2 describe-instances --instance-ids i-063d58d8309714c44 --region us-east-2

# Executar deploy
cd C:\Users\eliel\.vscode\framework_udf
.\deploy_now.ps1

# Verificar funções criadas
aws lambda list-functions --region us-east-2
```

---

## 🎯 **PRÓXIMOS PASSOS**

### **1. Configurar credenciais (escolha):**
- **AWS Console** → Security Credentials → Create Access Key
- **CloudShell** → Deploy direto no navegador

### **2. Deploy Lambda:**
- Executar script `deploy_now.ps1`

### **3. Configurar FastAPI:**
```python
# app/services/lambda_service.py
lambda_service = LambdaService(simulate=False)
```

### **4. Testar:**
```powershell
# Reiniciar FastAPI
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Testar Lambda real
http://localhost:8000/lambda/functions/status
```

---

**🎯 Recomendação: Use CloudShell se quiser deploy em 2 minutos sem configurar nada!**