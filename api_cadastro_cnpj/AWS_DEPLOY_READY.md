# 🔐 Configuração AWS - Credenciais Específicas
**Account ID**: 217466752219  
**Região**: us-east-2  
**Status**: Root account detectado

## 🎯 **CONFIGURAÇÃO RÁPIDA**

### **MÉTODO 1: AWS Console (Recomendado)**

#### **1. Acesso AWS Console**
- **URL**: https://console.aws.amazon.com/
- **Login**: Root account (email da conta)

#### **2. Criar IAM User (Segurança)**
```bash
# No AWS Console:
1. Procurar "IAM" no search
2. Users → Create User
3. Username: "lambda-deploy-user"
4. ✅ Programmatic access
5. Attach policies:
   - AWSLambdaFullAccess
   - IAMFullAccess
   - AmazonS3FullAccess
6. Create User
7. Download CSV ou copiar:
   - Access Key ID
   - Secret Access Key
```

#### **3. Configurar no terminal**
```powershell
aws configure

# Inserir:
AWS Access Key ID: [access key do IAM user]
AWS Secret Access Key: [secret key do IAM user]
Default region name: us-east-2
Default output format: json
```

---

## 🚀 **MÉTODO 2: CloudShell (Mais Rápido)**

#### **1. Abrir CloudShell**
- No AWS Console → Procurar "CloudShell"
- Ou clicar no ícone do terminal

#### **2. Deploy direto no CloudShell**
```bash
# No CloudShell (já tem credenciais):
git clone https://github.com/elielguedes/Relatorio_Eliel_Guedes.git
cd Relatorio_Eliel_Guedes/framework_udf/lambda_functions

# Criar role IAM
aws iam create-role --role-name lambda-execution-role --assume-role-policy-document '{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {"Service": "lambda.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }
  ]
}'

# Anexar policy
aws iam attach-role-policy --role-name lambda-execution-role --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

# Deploy funções Lambda
chmod +x deploy.sh
./deploy.sh
```

---

## ⚡ **MÉTODO 3: Credenciais Temporárias (Root)**

**⚠️ Não recomendado para produção, mas funciona para teste:**

#### **1. Criar Access Key temporária**
```bash
# AWS Console → Security Credentials → Access Keys
1. Create New Access Key
2. Download ou copiar credenciais
3. ⚠️ IMPORTANTE: Deletar depois do teste
```

#### **2. Configurar temporariamente**
```powershell
# No seu terminal:
$env:AWS_ACCESS_KEY_ID = "AKIA..."
$env:AWS_SECRET_ACCESS_KEY = "..."
$env:AWS_DEFAULT_REGION = "us-east-2"

# Testar
aws sts get-caller-identity
```

---

## 🧪 **TESTE RÁPIDO DE CONFIGURAÇÃO**

### **Verificar acesso:**
```powershell
# 1. Identidade
aws sts get-caller-identity

# 2. Sua EC2
aws ec2 describe-instances --instance-ids i-063d58d8309714c44 --region us-east-2

# 3. Funções Lambda existentes
aws lambda list-functions --region us-east-2
```

### **Se funcionar, fazer deploy:**
```powershell
cd C:\Users\eliel\.vscode\framework_udf\lambda_functions
.\deploy.ps1
```

---

## 🎯 **DEPLOY AUTOMÁTICO (Depois de configurar)**

```powershell
# Script completo de verificação e deploy
Write-Host "🔍 Verificando configuração AWS..." -ForegroundColor Yellow

try {
    $identity = aws sts get-caller-identity --output json | ConvertFrom-Json
    Write-Host "✅ AWS configurado!" -ForegroundColor Green
    Write-Host "   Account: $($identity.Account)" -ForegroundColor Cyan
    Write-Host "   User: $($identity.Arn)" -ForegroundColor Cyan
    
    # Verificar região
    $region = aws configure get region
    Write-Host "   Region: $region" -ForegroundColor Cyan
    
    if ($region -ne "us-east-2") {
        Write-Host "⚠️  Ajustando região para us-east-2..." -ForegroundColor Yellow
        aws configure set region us-east-2
    }
    
    # Deploy Lambda
    Write-Host "🚀 Iniciando deploy Lambda..." -ForegroundColor Green
    cd lambda_functions
    .\deploy.ps1
    
} catch {
    Write-Host "❌ Erro na configuração AWS" -ForegroundColor Red
    Write-Host "🔧 Execute: aws configure" -ForegroundColor Yellow
}
```

---

## 📊 **PRÓXIMOS PASSOS**

### **1. Configurar credenciais (escolha um método):**
- ✅ **CloudShell** (mais rápido, já logado)
- ✅ **IAM User** (mais seguro)
- ⚠️ **Root Access Key** (apenas para teste)

### **2. Fazer deploy:**
```powershell
cd lambda_functions
.\deploy.ps1
```

### **3. Configurar FastAPI:**
```python
# app/services/lambda_service.py
lambda_service = LambdaService(simulate=False)
```

### **4. Testar integração:**
```bash
# Local com Lambda real
http://localhost:8000/lambda/functions/status
```

---

**🎯 Recomendação: Use CloudShell (Método 2) para deploy mais rápido!**