#!/bin/bash

# 🚀 Deploy AWS Lambda - CloudShell
# Execução direta no CloudShell da AWS

echo "🔥 DEPLOY AUTOMÁTICO AWS LAMBDA"
echo "================================"

# Definir variáveis
REGION="us-east-2"
ROLE_NAME="lambda-execution-role"
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

echo "📊 Account ID: $ACCOUNT_ID"
echo "🌍 Region: $REGION"

# 1. Criar role IAM para Lambda
echo "🔧 Criando role IAM..."
aws iam create-role \
    --role-name $ROLE_NAME \
    --assume-role-policy-document '{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"Service": "lambda.amazonaws.com"},
                "Action": "sts:AssumeRole"
            }
        ]
    }' \
    --region $REGION 2>/dev/null || echo "Role já existe"

# 2. Anexar políticas
echo "🔐 Anexando políticas..."
aws iam attach-role-policy \
    --role-name $ROLE_NAME \
    --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

# 3. Aguardar propagação
echo "⏳ Aguardando propagação IAM..."
sleep 10

# 4. Criar diretório e arquivos Lambda
echo "📁 Criando funções Lambda..."
mkdir -p lambda_functions && cd lambda_functions

# Função 1: Validar CNPJ
cat > validate_cnpj.py << 'EOF'
import json
import re

def lambda_handler(event, context):
    """Valida CNPJ"""
    try:
        cnpj = event.get('cnpj', '')
        
        # Remove caracteres especiais
        cnpj = re.sub(r'[^0-9]', '', cnpj)
        
        # Validação básica
        if len(cnpj) != 14:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'valid': False,
                    'error': 'CNPJ deve ter 14 dígitos'
                })
            }
        
        # Simulação de validação
        is_valid = len(set(cnpj)) > 1  # CNPJ não pode ter todos os dígitos iguais
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'cnpj': cnpj,
                'valid': is_valid,
                'message': 'CNPJ válido' if is_valid else 'CNPJ inválido'
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }
EOF

# Função 2: Processar CSV
cat > process_csv.py << 'EOF'
import json
import csv
import io

def lambda_handler(event, context):
    """Processa dados CSV"""
    try:
        csv_data = event.get('csv_data', '')
        
        if not csv_data:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'CSV data is required'
                })
            }
        
        # Processar CSV
        csv_reader = csv.DictReader(io.StringIO(csv_data))
        processed_data = []
        
        for row in csv_reader:
            processed_data.append({
                'cnpj': row.get('cnpj', ''),
                'razao_social': row.get('razao_social', ''),
                'status': 'processed'
            })
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'processed_records': len(processed_data),
                'data': processed_data[:10]  # Primeiros 10 registros
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }
EOF

# Função 3: Gerar Relatório
cat > generate_report.py << 'EOF'
import json
from datetime import datetime

def lambda_handler(event, context):
    """Gera relatório"""
    try:
        report_type = event.get('type', 'summary')
        
        # Simulação de geração de relatório
        report_data = {
            'report_id': f"RPT_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'type': report_type,
            'generated_at': datetime.now().isoformat(),
            'summary': {
                'total_companies': 150,
                'active_companies': 120,
                'inactive_companies': 30,
                'success_rate': '80%'
            }
        }
        
        return {
            'statusCode': 200,
            'body': json.dumps(report_data)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }
EOF

# 5. Fazer deploy das funções
echo "🚀 Fazendo deploy das funções..."

# Deploy função 1
zip validate_cnpj.zip validate_cnpj.py
aws lambda create-function \
    --function-name validate-cnpj-async \
    --runtime python3.9 \
    --role arn:aws:iam::$ACCOUNT_ID:role/$ROLE_NAME \
    --handler validate_cnpj.lambda_handler \
    --zip-file fileb://validate_cnpj.zip \
    --region $REGION

# Deploy função 2
zip process_csv.zip process_csv.py
aws lambda create-function \
    --function-name process-csv \
    --runtime python3.9 \
    --role arn:aws:iam::$ACCOUNT_ID:role/$ROLE_NAME \
    --handler process_csv.lambda_handler \
    --zip-file fileb://process_csv.zip \
    --region $REGION

# Deploy função 3
zip generate_report.zip generate_report.py
aws lambda create-function \
    --function-name generate-report \
    --runtime python3.9 \
    --role arn:aws:iam::$ACCOUNT_ID:role/$ROLE_NAME \
    --handler generate_report.lambda_handler \
    --zip-file fileb://generate_report.zip \
    --region $REGION

echo ""
echo "✅ DEPLOY CONCLUÍDO!"
echo "==================="
echo "🔗 Funções criadas:"
echo "   • validate-cnpj-async"
echo "   • process-csv" 
echo "   • generate-report"
echo ""
echo "🧪 Testar:"
echo "aws lambda invoke --function-name validate-cnpj-async --payload '{\"cnpj\":\"12345678901234\"}' response.json"
echo ""
echo "🌐 Configurar FastAPI:"
echo "Mude simulate=False no arquivo lambda_service.py"