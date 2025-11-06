# 🚀 AWS Lambda Functions - API Cadastro CNPJ

## � Funções Serverless Implementadas

### 🎯 **Arquitetura Híbrida EC2 + Lambda**
```
🌐 Internet
    ↓
🏢 FastAPI (EC2) ← API Principal
    ↓ (integração)
☁️ AWS Lambda ← Processamento Assíncrono
    ├── 🔍 validate-cnpj-api
    ├── 📊 import-csv-processor  
    └── � generate-reports
```

## 📁 **Estrutura de Arquivos:**

### **1️⃣ validate_cnpj.py** - Validação Assíncrona
- ✅ Algoritmo matemático CNPJ (Receita Federal)
- 🌐 Consulta API pública ReceitaWS
- ⚡ Processamento mais rápido que síncronos
- 🔄 Integrado com FastAPI via `/lambda/validate-cnpj-async`

### **2️⃣ import_csv.py** - Processamento CSV
- 📂 Processa arquivos CSV grandes em chunks
- 💾 Salva resultados no S3
- 🔍 Validação automática dos dados
- 📊 Relatório de erros e sucessos

### **3️⃣ generate_reports.py** - Relatórios
- 📈 Estatísticas automáticas (UF, situação, porte)
- 📧 Notificações via SNS (opcional)
- 💾 Backup automático S3
- ⏰ Pode ser agendado via EventBridge

## 🔧 **Deploy Automático**

### **Pré-requisitos:**
```bash
# 1. AWS CLI configurado
aws configure

# 2. Permissões necessárias:
#    - Lambda Full Access
#    - IAM Role Creation
#    - S3 Access (opcional)
#    - SNS Access (opcional)
```

### **Deploy em 1 Comando:**
```bash
chmod +x deploy.sh
./deploy.sh
```

### **Deploy Manual:**
```bash
# Função 1: Validação CNPJ
zip -j validate-cnpj.zip validate_cnpj.py
aws lambda create-function \
  --function-name validate-cnpj-api \
  --runtime python3.12 \
  --role arn:aws:iam::ACCOUNT:role/lambda-execution-role \
  --handler validate_cnpj.lambda_handler \
  --zip-file fileb://validate-cnpj.zip

# Função 2: CSV Processor  
zip -j import-csv.zip import_csv.py
aws lambda create-function \
  --function-name import-csv-processor \
  --runtime python3.12 \
  --role arn:aws:iam::ACCOUNT:role/lambda-execution-role \
  --handler import_csv.lambda_handler \
  --zip-file fileb://import-csv.zip

# Função 3: Reports Generator
zip -j generate-reports.zip generate_reports.py  
aws lambda create-function \
  --function-name generate-reports \
  --runtime python3.12 \
  --role arn:aws:iam::ACCOUNT:role/lambda-execution-role \
  --handler generate_reports.lambda_handler \
  --zip-file fileb://generate-reports.zip
```

## 🔌 **Integração com FastAPI**

### **Novos Endpoints:**
```
POST /lambda/validate-cnpj-async
POST /lambda/process-csv  
POST /lambda/generate-report
GET  /lambda/functions/status
POST /lambda/test-integration
```

### **Exemplo de Uso:**
```python
# Via FastAPI
response = requests.post(
    "http://sua-api.com/lambda/validate-cnpj-async",
    json={"cnpj": "11.222.333/0001-81"},
    headers={"Authorization": "Bearer seu-jwt-token"}
)
```

## 🧪 **Testes das Funções**

### **Teste Local:**
```python
# Testar validate_cnpj.py
python validate_cnpj.py

# Testar import_csv.py  
python import_csv.py

# Testar generate_reports.py
python generate_reports.py
```

### **Teste AWS Lambda:**
```bash
# Teste via AWS CLI
aws lambda invoke \
  --function-name validate-cnpj-api \
  --payload '{"cnpj":"11.222.333/0001-81"}' \
  response.json && cat response.json

aws lambda invoke \
  --function-name generate-reports \
  --payload '{}' \
  report_response.json && cat report_response.json
```

## 📊 **Monitoramento e Logs**

### **CloudWatch Logs:**
```bash
# Ver logs em tempo real
aws logs tail /aws/lambda/validate-cnpj-api --follow
aws logs tail /aws/lambda/import-csv-processor --follow  
aws logs tail /aws/lambda/generate-reports --follow
```

### **Métricas disponíveis:**
- ⏱️ **Duration** - Tempo de execução
- 💰 **Cost** - Custo por invocação
- 🔄 **Invocations** - Número de chamadas
- ❌ **Errors** - Taxa de erro

## 🎯 **Vantagens da Implementação**

### **✅ Para o Projeto:**
- **Arquitetura moderna** - EC2 + Serverless
- **Escalabilidade** - Lambda escala automaticamente
- **Performance** - Processamento paralelo
- **Custo-efetivo** - Paga apenas pelo uso
- **Demonstra conhecimento** - AWS completo

### **✅ Para Apresentação:**
- *"Implementei arquitetura híbrida"*
- *"Serverless para processamento pesado"*  
- *"Demonstra conhecimento AWS completo"*
- *"Escalável para milhões de requisições"*

## 📈 **Casos de Uso:**

1. **Validação CNPJ** → Para múltiplas validações simultâneas
2. **Import CSV** → Arquivos grandes (>100MB)  
3. **Relatórios** → Processamento noturno automatizado

## 🔧 **Configurações Opcionais**

### **S3 Buckets (criar se necessário):**
```bash
aws s3 mb s3://cnpj-processed-data
aws s3 mb s3://cnpj-reports
```

### **SNS Topic (notificações):**
```bash
aws sns create-topic --name cnpj-reports-notification
```

## 🎉 **Resultado Final:**
- ✅ **3 funções Lambda** deployadas
- ✅ **Integração com FastAPI** funcionando
- ✅ **Endpoints novos** disponíveis
- ✅ **Arquitetura híbrida** completa
- ✅ **Demonstração serverless** impressionante

**🚀 Projeto agora tem EC2 + Lambda = Arquitetura Profissional Completa!**