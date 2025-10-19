# 🚀 Guia Completo de Deploy AWS Lambda
**Projeto: Sistema Empresarial FastAPI + Lambda**  
**Autor: Eliel Guedes**  
**Data: Outubro 2025**  
**Status: ✅ 100% Funcional - Deploy Ready**

## 📋 Resumo do Estado Atual

### ✅ **Implementado e Funcionando**:
- **FastAPI local**: http://127.0.0.1:8000/docs ✅
- **Lambda routes simuladas**: `/lambda/*` endpoints 100% funcionais ✅
- **Autenticação JWT**: Sistema completo integrado ✅
- **Validação CNPJ**: Algoritmo oficial Receita Federal ✅
- **Processamento CSV**: Lógica chunking + S3 ready ✅
- **Geração relatórios**: Estatísticas + SNS notifications ✅
- **Scripts deploy**: PowerShell automatizado ✅
- **Documentação**: Guias completos + exemplos ✅

### 🎯 **Objetivo**: Deploy Production AWS

## 🔧 Pré-requisitos para Deploy

### 1. AWS CLI
```powershell
# Instalar AWS CLI
winget install Amazon.AWSCLI

# Verificar instalação
aws --version
```

### 2. Configurar Credenciais AWS
```powershell
# Configurar AWS (você precisa ter uma conta AWS)
aws configure

# Inserir:
# AWS Access Key ID: [sua chave]
# AWS Secret Access Key: [sua chave secreta]
# Default region: us-east-1
# Default output format: json
```

### 3. Permissões necessárias
- `AWSLambdaFullAccess`
- `IAMFullAccess` 
- `AmazonS3FullAccess`
- `AmazonSNSFullAccess`

## 🚀 Deploy Automático

### Opção 1: Script de Deploy
```powershell
cd C:\Users\eliel\.vscode\framework_udf\lambda_functions
.\deploy.sh
```

### Opção 2: Deploy Manual

#### Função 1: Validador CNPJ
```powershell
cd C:\Users\eliel\.vscode\framework_udf\lambda_functions

# Criar pacote
Compress-Archive -Path validate_cnpj.py -DestinationPath validate-cnpj.zip

# Deploy para AWS
aws lambda create-function \
  --function-name validate-cnpj-api \
  --runtime python3.9 \
  --role arn:aws:iam::ACCOUNT:role/lambda-execution-role \
  --handler validate_cnpj.lambda_handler \
  --zip-file fileb://validate-cnpj.zip \
  --timeout 30 \
  --memory-size 128
```

#### Função 2: Processador CSV
```powershell
# Criar requirements.txt para Lambda
echo "boto3==1.26.137" > requirements_lambda.txt
echo "requests==2.31.0" >> requirements_lambda.txt

# Instalar dependências
pip install -r requirements_lambda.txt -t .

# Criar pacote
Compress-Archive -Path import_csv.py,boto3,requests -DestinationPath import-csv.zip

# Deploy
aws lambda create-function \
  --function-name import-csv-processor \
  --runtime python3.9 \
  --role arn:aws:iam::ACCOUNT:role/lambda-execution-role \
  --handler import_csv.lambda_handler \
  --zip-file fileb://import-csv.zip \
  --timeout 300 \
  --memory-size 512
```

#### Função 3: Gerador de Relatórios
```powershell
# Criar pacote
Compress-Archive -Path generate_reports.py,boto3 -DestinationPath generate-reports.zip

# Deploy
aws lambda create-function \
  --function-name generate-reports \
  --runtime python3.9 \
  --role arn:aws:iam::ACCOUNT:role/lambda-execution-role \
  --handler generate_reports.lambda_handler \
  --zip-file fileb://generate-reports.zip \
  --timeout 120 \
  --memory-size 256
```

## 🔗 Conectar FastAPI com Lambda Real

### 1. Instalar boto3 (já feito)
```powershell
pip install boto3
```

### 2. Configurar variáveis de ambiente
```powershell
# No arquivo .env
AWS_REGION=us-east-1
LAMBDA_VALIDATE_CNPJ=validate-cnpj-api
LAMBDA_IMPORT_CSV=import-csv-processor
LAMBDA_GENERATE_REPORTS=generate-reports
```

### 3. Ativar Lambda Service Real
Descomentar no `app/services/lambda_service.py`:
```python
# Trocar simulate=True por simulate=False
lambda_service = LambdaService(simulate=False)
```

## 🧪 Teste Local vs. Lambda Real

### Teste Local (atual):
```http
POST http://127.0.0.1:8000/lambda/validate-cnpj-async
Authorization: Bearer test-token
Content-Type: application/json

{
    "cnpj": "11.222.333/0001-81"
}
```

### Resultado esperado após deploy:
```json
{
  "success": true,
  "user": "lambda_user", 
  "processing_location": "AWS Lambda us-east-1",
  "result": {
    "cnpj": "11.222.333/0001-81",
    "valid": true,
    "receita_federal": {...}
  }
}
```

## 💰 Custos Estimados

### AWS Free Tier (primeiro ano):
- **Lambda**: 1M invocações gratuitas/mês
- **S3**: 5GB armazenamento gratuito
- **SNS**: 1.000 notificações gratuitas

### Estimativa para produção:
- **Lambda**: ~$0.20 por 1M invocações
- **S3**: ~$0.023 per GB/mês
- **SNS**: ~$0.50 per 1M mensagens
- **Total mensal estimado**: < $5.00

## ⚡ Próximos Passos

1. **Configurar AWS CLI**: `aws configure`
2. **Testar credenciais**: `aws sts get-caller-identity`
3. **Executar deploy**: `./deploy.sh`
4. **Testar endpoints**: Via Swagger UI
5. **Monitorar logs**: AWS CloudWatch

## 🎓 Apresentação Acadêmica

### Arquitetura Híbrida Implementada:
- **FastAPI**: API Rest tradicional
- **AWS Lambda**: Processamento serverless
- **SQLite**: Banco de dados local
- **JWT**: Autenticação stateless
- **OpenAPI**: Documentação automática

### Benefícios demonstrados:
- ✅ Escalabilidade serverless
- ✅ Custos otimizados (pay-per-use)
- ✅ Alta disponibilidade
- ✅ Separação de responsabilidades
- ✅ Integração híbrida cloud/on-premise

---

**Status**: 🟢 Pronto para deploy!  
**Próximo**: Configure AWS CLI e execute deploy