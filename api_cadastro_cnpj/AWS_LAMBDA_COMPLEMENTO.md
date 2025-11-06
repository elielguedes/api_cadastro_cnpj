# 🚀 AWS LAMBDA - IMPLEMENTAÇÃO PARA COMPLETAR O PROJETO

## 📋 Por que AWS Lambda pode ser necessário:

### 🎓 **Requisitos Acadêmicos**
- Demonstrar conhecimento em **Serverless Computing**
- Comparar **EC2 vs Lambda** (infraestrutura vs serverless)
- Mostrar **diferentes estratégias de deploy**

### 💡 **Casos de Uso Lambda no seu projeto:**

#### 1️⃣ **Processamento de Dados CSV**
```python
# lambda_import_cnpj.py
import json
import boto3
from app.services import import_service

def lambda_handler(event, context):
    """
    Lambda para processar importação de dados CNPJ
    """
    try:
        # Upload de arquivo CSV via S3
        s3_bucket = event['bucket']
        s3_key = event['key']
        
        # Processar arquivo
        result = import_service.process_cnpj_file(s3_bucket, s3_key)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Import completed',
                'processed_records': result['count'],
                'errors': result['errors']
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
```

#### 2️⃣ **Validação CNPJ Assíncrona**
```python
# lambda_validate_cnpj.py
import json
from app.services.validation_service import validate_cnpj_api

def lambda_handler(event, context):
    """
    Lambda para validação assíncrona de CNPJ
    """
    cnpj = event['cnpj']
    
    validation_result = validate_cnpj_api(cnpj)
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'cnpj': cnpj,
            'valid': validation_result['valid'],
            'company_data': validation_result['data']
        })
    }
```

#### 3️⃣ **Relatórios Agendados**
```python
# lambda_reports.py
import json
from datetime import datetime
from app.services.report_service import generate_monthly_report

def lambda_handler(event, context):
    """
    Lambda para gerar relatórios mensais automaticamente
    """
    report_data = generate_monthly_report()
    
    # Enviar por email ou salvar no S3
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'report_generated': True,
            'timestamp': datetime.now().isoformat(),
            'records_count': report_data['count']
        })
    }
```

## 🔧 **IMPLEMENTAÇÃO RÁPIDA (15 minutos):**

### 1️⃣ **Criar função Lambda**
```bash
# Estrutura para Lambda
mkdir lambda_functions
cd lambda_functions

# Função de validação CNPJ
touch validate_cnpj.py
touch requirements_lambda.txt
```

### 2️⃣ **Requirements para Lambda**
```txt
# requirements_lambda.txt (menor para Lambda)
requests
boto3
json
```

### 3️⃣ **Deploy Lambda via AWS CLI**
```bash
# Criar pacote
zip -r lambda_validate_cnpj.zip validate_cnpj.py

# Deploy via AWS CLI
aws lambda create-function \
  --function-name validate-cnpj-api \
  --runtime python3.12 \
  --role arn:aws:iam::ACCOUNT:role/lambda-execution-role \
  --handler validate_cnpj.lambda_handler \
  --zip-file fileb://lambda_validate_cnpj.zip
```

### 4️⃣ **Integração com API Gateway**
```python
# Na sua FastAPI principal (EC2)
import boto3

@router.post("/cnpj/validate-async")
async def validate_cnpj_async(cnpj: str):
    """
    Endpoint que chama Lambda para validação assíncrona
    """
    lambda_client = boto3.client('lambda')
    
    response = lambda_client.invoke(
        FunctionName='validate-cnpj-api',
        Payload=json.dumps({'cnpj': cnpj})
    )
    
    return json.loads(response['Payload'].read())
```

## 📊 **ARQUITETURA HÍBRIDA (EC2 + Lambda):**

```
🌐 INTERNET
    ↓
🏢 FastAPI (EC2) ← Principal API
    ↓
☁️ Lambda Functions ← Processamento assíncrono
    ├── Validação CNPJ
    ├── Import dados CSV  
    └── Relatórios agendados
```

## 🎯 **VANTAGENS DE ADICIONAR LAMBDA:**

### ✅ **Para o Projeto Acadêmico:**
- **Demonstra conhecimento serverless**
- **Arquitetura mais robusta**
- **Processamento assíncrono**
- **Escalabilidade automática**

### ✅ **Para Apresentação:**
- "Implementei **arquitetura híbrida** EC2 + Lambda"
- "Lambda para **processamento pesado** de dados"
- "**Serverless** para funções específicas"
- "**Cost-effective** para tarefas esporádicas"

## ⏱️ **IMPLEMENTAÇÃO EM 20 MINUTOS:**

### Passo 1: Criar código Lambda (5 min)
### Passo 2: Deploy via console AWS (10 min)  
### Passo 3: Integrar com FastAPI (5 min)

## 🎬 **Para Apresentação:**
*"Além do deploy principal em EC2, implementei funções Lambda para processamento assíncrono de dados, demonstrando conhecimento tanto em infraestrutura tradicional quanto serverless computing."*

---

## ❓ **DECISÃO:**
- **Se tempo permitir**: Implemente 1 função Lambda simples
- **Se tempo curto**: Mencione como "próximo passo" na apresentação
- **Projeto atual**: Já está completo e funcional sem Lambda