echo "🚀 Deploy AWS Lambda para Account 217466752219"

# Criar role se não existir
aws iam create-role --role-name lambda-execution-role --assume-role-policy-document '{
  "Version": "2012-10-17",
  "Statement": [{"Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}]
}' 2>/dev/null || echo "✅ Role já existe"

# Anexar policy
aws iam attach-role-policy --role-name lambda-execution-role --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

# Aguardar propagação
sleep 5

# Criar função Lambda simples
echo 'import json
def lambda_handler(event, context):
    return {"statusCode": 200, "body": json.dumps({"cnpj": event.get("cnpj"), "valid": True, "source": "AWS Lambda"})}' > validate_cnpj.py

zip validate_cnpj.zip validate_cnpj.py

# Deploy
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
aws lambda create-function \
    --function-name validate-cnpj-async \
    --runtime python3.9 \
    --role arn:aws:iam::$ACCOUNT_ID:role/lambda-execution-role \
    --handler validate_cnpj.lambda_handler \
    --zip-file fileb://validate_cnpj.zip \
    --region us-east-2 2>/dev/null || aws lambda update-function-code \
    --function-name validate-cnpj-async \
    --zip-file fileb://validate_cnpj.zip \
    --region us-east-2

echo "✅ Deploy concluído!"
echo "🧪 Teste: aws lambda invoke --function-name validate-cnpj-async --payload '{\"cnpj\":\"12345678901234\"}' response.json"