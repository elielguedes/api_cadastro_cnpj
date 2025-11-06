# 🚀 Deploy AWS Produção - Passo a Passo
**Sistema FastAPI + Lambda**  
**Deploy Produção AWS**  
**Data: Outubro 2025**

## 🎯 **Objetivo: Deploy Completo AWS**

### ✅ **O que vamos fazer:**
1. **Instalar AWS CLI**
2. **Configurar credenciais AWS**
3. **Deploy 3 funções Lambda**
4. **Configurar FastAPI para usar Lambda real**
5. **Testar integração completa**

---

## 📋 **PASSO 1: Instalar AWS CLI**

### **Opção A: Via winget (Recomendado)**
```powershell
winget install Amazon.AWSCLI
```

### **Opção B: Download direto**
- Baixar: https://awscli.amazonaws.com/AWSCLIV2.msi
- Instalar executável
- Reiniciar terminal

### **Verificar instalação:**
```powershell
aws --version
# Resultado esperado: aws-cli/2.x.x
```

---

## 🔑 **PASSO 2: Configurar Credenciais AWS**

### **2.1 Criar conta AWS (se não tiver)**
- Acesse: https://aws.amazon.com/
- Create Account (Free Tier 12 meses)
- Verificar email e cartão

### **2.2 Obter credenciais**
1. Login AWS Console
2. **IAM** → **Users** → **Create User**
3. Nome: `lambda-deploy-user`
4. **Attach policies directly**:
   - `AWSLambdaFullAccess`
   - `IAMFullAccess`
   - `AmazonS3FullAccess`
   - `AmazonSNSFullAccess`
5. **Create user**
6. **Security credentials** → **Create access key**
7. **CLI access** → **Create**
8. **Salvar Access Key + Secret Key**

### **2.3 Configurar AWS CLI**
```powershell
aws configure

# Inserir:
AWS Access Key ID: [sua access key]
AWS Secret Access Key: [sua secret key]  
Default region name: us-east-1
Default output format: json
```

### **2.4 Testar configuração**
```powershell
aws sts get-caller-identity
# Deve retornar dados do usuário
```

---

## ⚡ **PASSO 3: Deploy Lambda Functions**

### **3.1 Verificar arquivos Lambda**
```powershell
cd C:\Users\eliel\.vscode\framework_udf\lambda_functions
dir
# Deve mostrar: validate_cnpj.py, import_csv.py, generate_reports.py
```

### **3.2 Executar deploy automático**
```powershell
cd C:\Users\eliel\.vscode\framework_udf\lambda_functions
.\deploy.ps1
```

### **3.3 OU deploy manual**

#### **Função 1: Validador CNPJ**
```powershell
# Criar IAM Role primeiro
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

# Criar ZIP
Compress-Archive -Path validate_cnpj.py -DestinationPath validate-cnpj.zip -Force

# Deploy função
aws lambda create-function \
  --function-name validate-cnpj-api \
  --runtime python3.9 \
  --role arn:aws:iam::$(aws sts get-caller-identity --query Account --output text):role/lambda-execution-role \
  --handler validate_cnpj.lambda_handler \
  --zip-file fileb://validate-cnpj.zip \
  --timeout 30 \
  --memory-size 128 \
  --description "Validação de CNPJ via ReceitaWS API"
```

#### **Função 2: Processador CSV**
```powershell
# Instalar deps
pip install requests boto3 -t .

# Criar ZIP
Compress-Archive -Path import_csv.py,requests,boto3,urllib3,certifi -DestinationPath import-csv.zip -Force

# Deploy
aws lambda create-function \
  --function-name import-csv-processor \
  --runtime python3.9 \
  --role arn:aws:iam::$(aws sts get-caller-identity --query Account --output text):role/lambda-execution-role \
  --handler import_csv.lambda_handler \
  --zip-file fileb://import-csv.zip \
  --timeout 300 \
  --memory-size 512 \
  --description "Processamento de arquivos CSV com S3"
```

#### **Função 3: Gerador Relatórios**
```powershell
# Criar ZIP
Compress-Archive -Path generate_reports.py -DestinationPath generate-reports.zip -Force

# Deploy
aws lambda create-function \
  --function-name generate-reports \
  --runtime python3.9 \
  --role arn:aws:iam::$(aws sts get-caller-identity --query Account --output text):role/lambda-execution-role \
  --handler generate_reports.lambda_handler \
  --zip-file fileb://generate-reports.zip \
  --timeout 120 \
  --memory-size 256 \
  --description "Geração de relatórios estatísticos com SNS"
```

---

## 🔧 **PASSO 4: Configurar FastAPI para Produção**

### **4.1 Ativar Lambda real**
Editar `app/services/lambda_service.py`:
```python
# Trocar de:
lambda_service = LambdaService(simulate=True)

# Para:
lambda_service = LambdaService(simulate=False)
```

### **4.2 Configurar variáveis de ambiente**
```powershell
# Criar arquivo .env
echo "AWS_REGION=us-east-1" > .env
echo "LAMBDA_VALIDATE_CNPJ=validate-cnpj-api" >> .env  
echo "LAMBDA_IMPORT_CSV=import-csv-processor" >> .env
echo "LAMBDA_GENERATE_REPORTS=generate-reports" >> .env
```

### **4.3 Reiniciar aplicação**
```powershell
cd C:\Users\eliel\.vscode\framework_udf
Remove-Item Env:DATABASE_URL -ErrorAction SilentlyContinue
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 🧪 **PASSO 5: Testar Integração**

### **5.1 Verificar funções Lambda**
```powershell
aws lambda list-functions --query 'Functions[].FunctionName'
```

### **5.2 Testar via API local**
```bash
# Status das funções
GET http://localhost:8000/lambda/functions/status

# Validação CNPJ real
POST http://localhost:8000/lambda/validate-cnpj-async
Authorization: Bearer test-token
{
  "cnpj": "11.222.333/0001-81"
}
```

### **5.3 Verificar logs CloudWatch**
```powershell
aws logs describe-log-groups --log-group-name-prefix "/aws/lambda/"
```

---

## 💰 **PASSO 6: Monitorar Custos**

### **Free Tier AWS (12 meses):**
- ✅ **Lambda**: 1M invocações gratuitas/mês
- ✅ **S3**: 5GB armazenamento gratuito
- ✅ **SNS**: 1.000 notificações gratuitas

### **Estimativa pós Free Tier:**
- **Lambda**: ~$0.20 por 1M invocações
- **S3**: ~$0.023 por GB/mês
- **SNS**: ~$0.50 por 1M mensagens
- **Total estimado**: < $5.00/mês

---

## 🎯 **Deploy Completo - Checklist**

### ✅ **Preparação:**
- [ ] AWS CLI instalado
- [ ] Credenciais configuradas
- [ ] Conta AWS ativa

### ✅ **Deploy Lambda:**
- [ ] IAM Role criada
- [ ] validate-cnpj-api deployada
- [ ] import-csv-processor deployada  
- [ ] generate-reports deployada

### ✅ **Configuração FastAPI:**
- [ ] lambda_service.py atualizado
- [ ] .env configurado
- [ ] Aplicação reiniciada

### ✅ **Testes:**
- [ ] Funções listadas no AWS
- [ ] API respondendo com Lambda real
- [ ] Logs aparecendo no CloudWatch

---

## 🚀 **Scripts Prontos**

### **deploy_complete.ps1**
```powershell
# Deploy completo automatizado
Write-Host "🚀 Iniciando deploy AWS completo..." -ForegroundColor Green

# 1. Verificar AWS CLI
if (!(Get-Command aws -ErrorAction SilentlyContinue)) {
    Write-Host "❌ AWS CLI não encontrado. Instalando..." -ForegroundColor Red
    winget install Amazon.AWSCLI
    Write-Host "✅ Reinicie o terminal e execute novamente" -ForegroundColor Yellow
    exit
}

# 2. Verificar credenciais
try {
    $identity = aws sts get-caller-identity --output json | ConvertFrom-Json
    Write-Host "✅ AWS configurado: $($identity.UserId)" -ForegroundColor Green
} catch {
    Write-Host "❌ Execute: aws configure" -ForegroundColor Red
    exit
}

# 3. Deploy funções
cd lambda_functions
.\deploy.ps1

# 4. Configurar FastAPI
Write-Host "🔧 Configurando FastAPI para produção..." -ForegroundColor Cyan
# (atualizar lambda_service.py automaticamente)

Write-Host "🎉 Deploy AWS concluído!" -ForegroundColor Green
```

---

## 📞 **Suporte ao Deploy**

### **Problemas comuns:**

#### **"AccessDenied" ao criar função**
```powershell
# Verificar permissões IAM
aws iam list-attached-role-policies --role-name lambda-execution-role
```

#### **"InvalidParameterValueException"**
```powershell
# Verificar região
aws configure get region
# Deve ser: us-east-1
```

#### **Timeout na execução**
```powershell
# Aumentar timeout
aws lambda update-function-configuration \
  --function-name validate-cnpj-api \
  --timeout 60
```

---

**🎯 Pronto para começar o deploy AWS em produção!**

**Próximo passo**: Executar `winget install Amazon.AWSCLI` e seguir o guia passo a passo.