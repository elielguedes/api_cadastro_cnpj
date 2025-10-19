# 🚀 Deploy FastAPI + Lambda na AWS
**Instância EC2**: i-063d58d8309714c44  
**IP Público**: 18.118.167.28  
**Região**: us-east-2

## ✅ **Status AWS**
- **EC2**: ✅ Executando (t3.micro)
- **IP Público**: ✅ 18.118.167.28
- **DNS**: ✅ ec2-18-118-167-28.us-east-2.compute.amazonaws.com
- **Region**: ✅ us-east-2

---

## 🎯 **DEPLOY OPTION 1: Lambda Functions (Recomendado)**

Vamos criar as funções Lambda na mesma região da sua EC2:

### **1. Configure credenciais AWS**
```powershell
# Você precisa das credenciais de acesso
aws configure

# Inserir:
AWS Access Key ID: [sua access key]
AWS Secret Access Key: [sua secret key]
Default region name: us-east-2  # Mesma região da EC2
Default output format: json
```

### **2. Deploy Lambda Functions**
```powershell
cd C:\Users\eliel\.vscode\framework_udf\lambda_functions

# Executar script de deploy
.\deploy.ps1
```

---

## 🎯 **DEPLOY OPTION 2: FastAPI na EC2**

Se quiser usar a EC2 que já está rodando:

### **1. Conectar à EC2**
```powershell
# Via SSH (precisa da chave .pem)
ssh -i "sua-chave.pem" ec2-user@18.118.167.28

# OU via Session Manager (mais fácil)
aws ssm start-session --target i-063d58d8309714c44
```

### **2. Instalar aplicação na EC2**
```bash
# Na EC2:
sudo yum update -y
sudo yum install python3 python3-pip git -y

# Clone projeto
git clone https://github.com/elielguedes/Relatorio_Eliel_Guedes.git
cd Relatorio_Eliel_Guedes/framework_udf

# Instalar dependências
pip3 install -r requirements.txt

# Executar aplicação
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### **3. Configurar Security Group**
```powershell
# Permitir acesso na porta 8000
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxx \
  --protocol tcp \
  --port 8000 \
  --cidr 0.0.0.0/0
```

---

## 🎯 **DEPLOY OPTION 3: Híbrido (Melhor)**

FastAPI local + Lambda na AWS:

### **1. Deploy apenas Lambda**
```powershell
# Manter FastAPI local rodando
cd C:\Users\eliel\.vscode\framework_udf
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Deploy Lambda na AWS (us-east-2)
cd lambda_functions
.\deploy.ps1
```

### **2. Configurar FastAPI para usar Lambda real**
```python
# Editar app/services/lambda_service.py
lambda_service = LambdaService(simulate=False)  # AWS real
```

---

## 🧪 **TESTE RÁPIDO - SEM CONFIGURAÇÃO**

Para testar imediatamente sem configurar AWS:

### **Verificar se EC2 está acessível**
```powershell
# Testar conexão
curl http://18.118.167.28:8000

# Se retornar erro, precisa configurar Security Group
```

### **Usar simulação Lambda local**
```powershell
# Aplicação já funciona 100% com Lambda simulado
http://localhost:8000/docs
http://localhost:8000/lambda/functions/status
```

---

## 🔧 **CONFIGURAÇÃO AWS CREDENTIALS**

Como você tem EC2 rodando, provavelmente tem conta AWS configurada.

### **Método 1: AWS Academy/Educate**
Se usando AWS Academy:
1. AWS Academy → AWS Details → AWS CLI
2. Copiar credenciais temporárias
3. Executar no terminal

### **Método 2: Credenciais permanentes**
```powershell
aws configure
# Usar Access Key do IAM User
```

### **Método 3: EC2 Instance Role**
Se a EC2 tem role configurada, pode executar deploy direto na EC2.

---

## 🚀 **PRÓXIMOS PASSOS**

### **Para Deploy Lambda (Recomendado):**
1. `aws configure` (inserir credenciais)
2. `cd lambda_functions`
3. `.\deploy.ps1`
4. Atualizar `lambda_service.py` para `simulate=False`

### **Para EC2 Deploy:**
1. SSH na EC2: `ssh ec2-user@18.118.167.28`
2. Instalar aplicação
3. Configurar Security Group

### **Para Teste Imediato:**
1. Manter aplicação local rodando
2. Usar ngrok para link público
3. Lambda simulado funciona perfeitamente

---

## 📱 **LINKS FINAIS**

Depois do deploy você terá:

### **Local + Lambda AWS:**
```
✅ Local: http://localhost:8000/docs
✅ Público: https://seu-ngrok.io/docs  
✅ Lambda: AWS us-east-2 (real)
```

### **EC2 + Lambda AWS:**
```
✅ EC2: http://18.118.167.28:8000/docs
✅ Lambda: AWS us-east-2 (real)
```

---

**🎯 Qual opção você prefere? Deploy Lambda apenas ou usar a EC2 também?**