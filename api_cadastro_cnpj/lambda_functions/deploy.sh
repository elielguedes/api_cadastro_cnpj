#!/bin/bash

# Deploy automático das funções Lambda
# Autor: Eliel Guedes

set -e

echo "🚀 Deploy AWS Lambda Functions - API Cadastro CNPJ"
echo "=================================================="

# Configurações
REGION="us-east-1"
ROLE_NAME="lambda-execution-role-cnpj"
POLICY_ARN="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"

echo "📋 Verificando AWS CLI..."
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI não encontrado. Instale: https://aws.amazon.com/cli/"
    exit 1
fi

echo "🔑 Verificando credenciais AWS..."
aws sts get-caller-identity > /dev/null || {
    echo "❌ Credenciais AWS não configuradas. Execute: aws configure"
    exit 1
}

# Função para criar role IAM se não existir
create_lambda_role() {
    echo "🔐 Verificando IAM Role: $ROLE_NAME"
    
    if aws iam get-role --role-name "$ROLE_NAME" &>/dev/null; then
        echo "✅ Role já existe: $ROLE_NAME"
    else
        echo "📝 Criando IAM Role: $ROLE_NAME"
        
        # Criar trust policy
        cat > trust-policy.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
        
        # Criar role
        aws iam create-role \
            --role-name "$ROLE_NAME" \
            --assume-role-policy-document file://trust-policy.json
        
        # Anexar policy básica
        aws iam attach-role-policy \
            --role-name "$ROLE_NAME" \
            --policy-arn "$POLICY_ARN"
        
        # Anexar políticas adicionais para S3 e SNS
        aws iam attach-role-policy \
            --role-name "$ROLE_NAME" \
            --policy-arn "arn:aws:iam::aws:policy/AmazonS3FullAccess"
        
        aws iam attach-role-policy \
            --role-name "$ROLE_NAME" \
            --policy-arn "arn:aws:iam::aws:policy/AmazonSNSFullAccess"
        
        # Aguardar propagação
        echo "⏳ Aguardando propagação da role (30s)..."
        sleep 30
        
        rm trust-policy.json
        echo "✅ Role criada: $ROLE_NAME"
    fi
}

# Função para fazer deploy de uma Lambda
deploy_lambda() {
    local function_name=$1
    local file_name=$2
    local handler=$3
    local description=$4
    
    echo "📦 Fazendo deploy: $function_name"
    
    # Criar pacote ZIP
    zip -j "${function_name}.zip" "lambda_functions/${file_name}"
    
    # Obter ARN da role
    ROLE_ARN=$(aws iam get-role --role-name "$ROLE_NAME" --query 'Role.Arn' --output text)
    
    # Verificar se função já existe
    if aws lambda get-function --function-name "$function_name" &>/dev/null; then
        echo "🔄 Atualizando função existente: $function_name"
        
        aws lambda update-function-code \
            --function-name "$function_name" \
            --zip-file "fileb://${function_name}.zip"
        
        aws lambda update-function-configuration \
            --function-name "$function_name" \
            --description "$description" \
            --timeout 30 \
            --memory-size 256
    else
        echo "🆕 Criando nova função: $function_name"
        
        aws lambda create-function \
            --function-name "$function_name" \
            --runtime python3.12 \
            --role "$ROLE_ARN" \
            --handler "$handler" \
            --zip-file "fileb://${function_name}.zip" \
            --description "$description" \
            --timeout 30 \
            --memory-size 256 \
            --environment Variables='{
                "REGION":"'$REGION'",
                "ENVIRONMENT":"production"
            }'
    fi
    
    # Limpar arquivo ZIP
    rm "${function_name}.zip"
    
    # Obter URL de invocação
    FUNCTION_ARN=$(aws lambda get-function --function-name "$function_name" --query 'Configuration.FunctionArn' --output text)
    echo "✅ Deploy concluído: $function_name"
    echo "   ARN: $FUNCTION_ARN"
    
    # Criar URL de função (opcional)
    if aws lambda get-function-url-config --function-name "$function_name" &>/dev/null; then
        echo "   URL já existe para: $function_name"
    else
        echo "🌐 Criando Function URL para: $function_name"
        aws lambda create-function-url-config \
            --function-name "$function_name" \
            --auth-type NONE \
            --cors 'AllowCredentials=false,AllowMethods=["GET","POST"],AllowOrigins=["*"]' \
            --qualifier '$LATEST' 2>/dev/null || echo "   Aviso: Function URL não criada (opcional)"
    fi
    
    echo ""
}

# Executar deploy
echo "🏁 Iniciando deploy das funções Lambda..."
echo ""

create_lambda_role

# Deploy das 3 funções
deploy_lambda "validate-cnpj-api" "validate_cnpj.py" "validate_cnpj.lambda_handler" "Validação assíncrona de CNPJ com consulta Receita Federal"

deploy_lambda "import-csv-processor" "import_csv.py" "import_csv.lambda_handler" "Processador de arquivos CSV de empresas"

deploy_lambda "generate-reports" "generate_reports.py" "generate_reports.lambda_handler" "Gerador de relatórios estatísticos automatizados"

echo "🎉 Deploy completo das funções Lambda!"
echo ""
echo "📋 Funções deployadas:"
echo "   1. validate-cnpj-api - Validação de CNPJ"
echo "   2. import-csv-processor - Processamento CSV"
echo "   3. generate-reports - Relatórios automatizados"
echo ""
echo "🔧 Para testar as funções:"
echo "   aws lambda invoke --function-name validate-cnpj-api --payload '{\"cnpj\":\"11.222.333/0001-81\"}' response.json"
echo ""
echo "📚 Documentação das funções disponível em: lambda_functions/README.md"