# 🔑 Como Obter Credenciais AWS
**Sua instância**: i-063d58d8309714c44  
**Account ID**: 217466752219  
**Região**: us-east-2

## 🎯 **VOCÊ JÁ TEM AWS! Só falta conectar**

Como você tem uma EC2 rodando, significa que já tem conta AWS configurada. Só precisamos obter as credenciais.

---

## 🔧 **MÉTODO 1: AWS Console (Mais Fácil)**

### **1. Login AWS Console**
- Acesse: https://aws.amazon.com/console/
- Faça login na sua conta

### **2. Criar Access Key**
1. **IAM** → **Users** (no menu esquerdo)
2. Clique no seu usuário OU **Create User** se não houver
3. **Security credentials** tab
4. **Create access key**
5. **Command Line Interface (CLI)**
6. **Create**
7. **Download** ou copiar:
   - Access Key ID
   - Secret Access Key

### **3. Configurar no terminal**
```powershell
aws configure

# Quando solicitado:
AWS Access Key ID: [cole sua access key]
AWS Secret Access Key: [cole sua secret key]
Default region name: us-east-2
Default output format: json
```

---

## 🔧 **MÉTODO 2: AWS CloudShell (Alternativo)**

### **1. Abrir CloudShell**
- No AWS Console, clique no ícone **CloudShell** (terminal)
- Ou pesquise "CloudShell"

### **2. Deploy direto no CloudShell**
```bash
# No CloudShell (navegador):
git clone https://github.com/elielguedes/Relatorio_Eliel_Guedes.git
cd Relatorio_Eliel_Guedes/framework_udf/lambda_functions

# Deploy Lambda
chmod +x deploy.sh
./deploy.sh
```

---

## 🔧 **MÉTODO 3: Usar AWS CLI v2 Web**

### **1. Acesso via Session Manager**
```powershell
# Se tiver Session Manager configurado:
aws ssm start-session --target i-063d58d8309714c44
```

---

## ⚡ **DEPLOY RÁPIDO - CREDENCIAIS TEMPORÁRIAS**

Se estiver usando AWS Academy/Educate:

### **1. AWS Academy**
1. Canvas → AWS Academy
2. **AWS Details**
3. **AWS CLI** tab
4. **Copy** credenciais

### **2. Colar no terminal**
```powershell
# Colar as 3 linhas:
set AWS_ACCESS_KEY_ID=AKIA...
set AWS_SECRET_ACCESS_KEY=...
set AWS_SESSION_TOKEN=...

# OU no PowerShell:
$env:AWS_ACCESS_KEY_ID="AKIA..."
$env:AWS_SECRET_ACCESS_KEY="..."
$env:AWS_SESSION_TOKEN="..."
```

### **3. Testar e deploy**
```powershell
aws sts get-caller-identity
cd lambda_functions
.\deploy.ps1
```

---

## 🎯 **DEPOIS DE CONFIGURAR**

### **Verificar funcionamento:**
```powershell
# Testar credenciais
aws sts get-caller-identity

# Verificar sua EC2
aws ec2 describe-instances --instance-ids i-063d58d8309714c44

# Listar funções Lambda (depois do deploy)
aws lambda list-functions
```

### **Deploy Lambda:**
```powershell
cd C:\Users\eliel\.vscode\framework_udf\lambda_functions
.\deploy.ps1
```

---

## 🚀 **SCRIPT DE DEPLOY COMPLETO**

Salve como `deploy_aws_complete.ps1`:

```powershell
# Verificar credenciais
Write-Host "🔍 Verificando credenciais AWS..." -ForegroundColor Yellow
try {
    $identity = aws sts get-caller-identity --output json | ConvertFrom-Json
    Write-Host "✅ AWS configurado: $($identity.UserId)" -ForegroundColor Green
    Write-Host "📍 Account: $($identity.Account)" -ForegroundColor Cyan
    Write-Host "📍 Region: us-east-2" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Credenciais AWS não configuradas!" -ForegroundColor Red
    Write-Host "🔧 Execute: aws configure" -ForegroundColor Yellow
    exit 1
}

# Verificar EC2
Write-Host "🖥️  Verificando sua EC2..." -ForegroundColor Yellow
try {
    aws ec2 describe-instances --instance-ids i-063d58d8309714c44 --query 'Reservations[0].Instances[0].State.Name' --output text
    Write-Host "✅ EC2 acessível: i-063d58d8309714c44" -ForegroundColor Green
} catch {
    Write-Host "⚠️  EC2 não acessível, mas Lambda ainda pode ser deployada" -ForegroundColor Yellow
}

# Deploy Lambda
Write-Host "🚀 Fazendo deploy das funções Lambda..." -ForegroundColor Green
cd lambda_functions
.\deploy.ps1

Write-Host "🎉 Deploy concluído!" -ForegroundColor Green
Write-Host "🔗 Teste em: http://localhost:8000/lambda/functions/status" -ForegroundColor Cyan
```

---

## 📞 **PRÓXIMOS PASSOS**

### **1. Obter credenciais (escolha um método):**
- AWS Console → IAM → Create Access Key
- AWS Academy → AWS CLI credentials  
- AWS CloudShell (deploy direto)

### **2. Configurar:**
```powershell
aws configure
# Inserir credenciais obtidas
```

### **3. Deploy:**
```powershell
cd lambda_functions
.\deploy.ps1
```

### **4. Testar:**
```powershell
# Local com Lambda real
http://localhost:8000/lambda/functions/status
```

---

**🎯 Com sua EC2 já rodando, falta só obter as credenciais e fazer deploy das Lambda functions!**