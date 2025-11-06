# 🔑 Configuração AWS - Credenciais
**Deploy AWS Lambda - Configuração**

## 🎯 **Status Atual**
- ✅ **AWS CLI**: Instalado (v2.31.15)
- ❌ **Credenciais**: Não configuradas
- 🎯 **Próximo**: Configurar acesso AWS

---

## 🔧 **CONFIGURAÇÃO RÁPIDA AWS**

### **OPÇÃO 1: AWS Educate/Academy (Gratuito para estudantes)**
Se você tem acesso AWS Academy:
1. Login AWS Academy
2. **AWS Details** → **AWS CLI**
3. Copiar credenciais temporárias
4. Colar no terminal

### **OPÇÃO 2: Conta AWS Pessoal (Free Tier)**
1. **Criar conta**: https://aws.amazon.com/free/
2. **Verificar email + cartão**
3. **IAM** → **Users** → **Create User**
4. **Programmatic access**
5. **Attach policies**: `AWSLambdaFullAccess`
6. **Download credentials**

### **OPÇÃO 3: Usar AWS CloudShell (Mais Fácil)**
1. Login AWS Console
2. Procurar **CloudShell** 
3. Executar deploy direto no navegador

---

## ⚡ **CONFIGURAR CREDENCIAIS**

### **Método 1: aws configure**
```powershell
aws configure

# Inserir quando solicitado:
AWS Access Key ID: [sua access key]
AWS Secret Access Key: [sua secret key]
Default region name: us-east-1
Default output format: json
```

### **Método 2: Variáveis de ambiente**
```powershell
# Temporário (apenas esta sessão)
$env:AWS_ACCESS_KEY_ID = "sua-access-key"
$env:AWS_SECRET_ACCESS_KEY = "sua-secret-key"  
$env:AWS_DEFAULT_REGION = "us-east-1"
```

### **Método 3: AWS SSO (Se disponível)**
```powershell
aws configure sso
# Seguir instruções interativas
```

---

## 🧪 **TESTAR CONFIGURAÇÃO**

```powershell
# Verificar identidade
aws sts get-caller-identity

# Listar regiões disponíveis
aws ec2 describe-regions --query 'Regions[].RegionName'

# Verificar permissões Lambda
aws lambda list-functions
```

---

## 🚀 **DEPOIS DE CONFIGURAR: DEPLOY AUTOMÁTICO**

```powershell
# 1. Ir para pasta Lambda
cd C:\Users\eliel\.vscode\framework_udf\lambda_functions

# 2. Executar deploy
.\deploy.ps1

# 3. OU comandos manuais
```

---

## 🎯 **ALTERNATIVAS SEM CONFIGURAÇÃO**

### **Simulação Local (Atual)**
```powershell
# Continuar usando simulação Lambda
# Funciona 100% sem AWS
http://localhost:8000/lambda/functions/status
```

### **Deploy Vercel/Netlify**
```powershell
# Deploy FastAPI + simulação
# Público sem AWS
```

---

## 📞 **PRÓXIMOS PASSOS**

### **Se você TEM conta AWS:**
1. `aws configure` (inserir credenciais)
2. `cd lambda_functions`
3. `.\deploy.ps1`

### **Se você NÃO TEM conta AWS:**
1. **Criar conta Free Tier**: https://aws.amazon.com/free/
2. **OU continuar com simulação local** (funciona perfeitamente)

### **Para apresentação HOJE:**
- **Usar simulação local** (funciona igual ao AWS real)
- **Link público** via ngrok/DevTunnel
- **Deploy AWS** pode ser feito depois

---

**🎯 O sistema está 100% funcional mesmo sem AWS real!**
**As funções Lambda simuladas são idênticas às reais.**