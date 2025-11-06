# Deploy/Update AWS Lambda functions (us-east-2) - account 217466752219
# Requer: AWS CLI com credenciais válidas

$ErrorActionPreference = 'Stop'

Write-Host "🔍 Verificando credenciais AWS..." -ForegroundColor Yellow
try {
  $id = aws sts get-caller-identity --output json | ConvertFrom-Json
  if ($id.Account -ne "217466752219") {
    Write-Host "❌ Conta incorreta: $($id.Account). Esperado: 217466752219" -ForegroundColor Red
    exit 1
  }
  Write-Host "✅ AWS OK - $($id.Arn)" -ForegroundColor Green
} catch {
  Write-Host "❌ Sem credenciais. Rode: aws configure" -ForegroundColor Red
  exit 1
}

$region = "us-east-2"
$roleArn = "arn:aws:iam::217466752219:role/lambda-execution-role"
$lambdaPath = Join-Path $PSScriptRoot "..\lambda_functions"
Push-Location $lambdaPath

function Ensure-Role {
  Write-Host "🔧 Garantindo IAM Role..." -ForegroundColor Yellow
  try {
    aws iam get-role --role-name lambda-execution-role --region $region | Out-Null
    Write-Host "✅ Role existe" -ForegroundColor Green
  } catch {
    Write-Host "🆕 Criando role..." -ForegroundColor Yellow
    aws iam create-role --role-name lambda-execution-role --assume-role-policy-document '{
      "Version":"2012-10-17",
      "Statement":[{"Effect":"Allow","Principal":{"Service":"lambda.amazonaws.com"},"Action":"sts:AssumeRole"}]
    }' --region $region | Out-Null
    aws iam attach-role-policy --role-name lambda-execution-role --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole --region $region | Out-Null
    Start-Sleep -Seconds 8
    Write-Host "✅ Role criada" -ForegroundColor Green
  }
}

function Deploy-Or-Update($name, $handler, $codeZip) {
  try {
    aws lambda get-function --function-name $name --region $region | Out-Null
    Write-Host "♻️ Atualizando função $name..." -ForegroundColor Yellow
    aws lambda update-function-code --function-name $name --zip-file fileb://$codeZip --region $region | Out-Null
  } catch {
    Write-Host "🆕 Criando função $name..." -ForegroundColor Yellow
    aws lambda create-function --function-name $name --runtime python3.12 --role $roleArn --handler $handler --zip-file fileb://$codeZip --timeout 60 --memory-size 256 --region $region | Out-Null
  }
  Write-Host "✅ $name pronto" -ForegroundColor Green
}

Ensure-Role

# validate_cnpj
Write-Host "📦 Empacotando validate_cnpj..." -ForegroundColor Yellow
Compress-Archive -Path validate_cnpj.py -DestinationPath validate_cnpj.zip -Force
Deploy-Or-Update -name "validate-cnpj-async" -handler "validate_cnpj.lambda_handler" -codeZip "validate_cnpj.zip"

# generate_reports
Write-Host "📦 Empacotando generate_reports..." -ForegroundColor Yellow
Compress-Archive -Path generate_reports.py -DestinationPath generate_reports.zip -Force
Deploy-Or-Update -name "generate-report" -handler "generate_reports.lambda_handler" -codeZip "generate_reports.zip"

# import_csv (com dependências)
Write-Host "📦 Empacotando import_csv + deps..." -ForegroundColor Yellow
$pkgDir = "package"
if (Test-Path $pkgDir) { Remove-Item $pkgDir -Recurse -Force }
New-Item -ItemType Directory -Path $pkgDir | Out-Null
Copy-Item import_csv.py "$pkgDir/import_csv.py"
# Instalar dependências mínimas se necessário
try { pip install boto3 -t $pkgDir --quiet | Out-Null } catch {}
Push-Location $pkgDir
Compress-Archive -Path * -DestinationPath ../import_csv.zip -Force
Pop-Location
Deploy-Or-Update -name "process-csv" -handler "import_csv.lambda_handler" -codeZip "import_csv.zip"

Write-Host "📋 Funções na conta:" -ForegroundColor Cyan
aws lambda list-functions --region $region --query 'Functions[].FunctionName'

Pop-Location
