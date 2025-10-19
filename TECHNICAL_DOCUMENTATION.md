# 📖 Documentação Técnica - Sistema FastAPI + AWS Lambda

**Projeto**: Sistema Empresarial Híbrido  
**Autor**: Eliel Guedes  
**Data**: Outubro 2025  
**Versão**: 2.0.0

## 📊 Visão Geral Arquitetural

### 🏗️ **Arquitetura Híbrida Implementada**

```
┌─────────────────────────────────────────────────────────┐
│                    FastAPI Application                 │
│                    (127.0.0.1:8000)                   │
├─────────────────────────────────────────────────────────┤
│  Traditional Endpoints     │    Lambda Integration      │
│  • /empresas/*            │    • /lambda/validate-cnpj │
│  • /estabelecimentos/*    │    • /lambda/process-csv   │
│  • /socios/*              │    • /lambda/generate-report│
│  • /auth/*                │    • /lambda/functions/*   │
├─────────────────────────────────────────────────────────┤
│             Database Layer (SQLite/PostgreSQL)         │
├─────────────────────────────────────────────────────────┤
│                    AWS Lambda Functions                │
│  • validate_cnpj.py  • import_csv.py  • generate_reports.py │
├─────────────────────────────────────────────────────────┤
│              AWS Services Integration                   │
│  • S3 Storage  • SNS Notifications  • CloudWatch Logs │
└─────────────────────────────────────────────────────────┘
```

## 🔧 Componentes Técnicos

### 📱 **FastAPI Application**

#### **Estrutura de Arquivos**
```
app/
├── main.py                 # Entry point da aplicação
├── auth.py                 # Sistema JWT + bcrypt
├── database.py             # SQLAlchemy engine + session
├── models.py               # Modelos ORM (SQLAlchemy)
├── schemas.py              # Schemas Pydantic validation
├── deps.py                 # Dependencies injection
├── routers/
│   ├── empresas.py         # CRUD empresas
│   ├── estabelecimentos.py # CRUD estabelecimentos  
│   ├── socios.py           # CRUD sócios
│   └── lambda_routes.py    # ⭐ Lambda integration
└── services/
    └── lambda_service.py   # ⭐ AWS Lambda client
```

#### **Configurações de Ambiente**
```python
# Environment Variables
DATABASE_URL=None                    # Auto-detects SQLite
SECRET_KEY=dev-secret-change-me      # JWT secret
SQL_ECHO=false                       # SQLAlchemy logging
AWS_REGION=us-east-1                # Lambda region
LAMBDA_VALIDATE_CNPJ=validate-cnpj-api
LAMBDA_IMPORT_CSV=import-csv-processor  
LAMBDA_GENERATE_REPORTS=generate-reports
```

### ⚡ **AWS Lambda Functions**

#### **1. Validador CNPJ (`validate_cnpj.py`)**
```python
def lambda_handler(event, context):
    """
    Validação matemática + consulta ReceitaWS
    Input: {"cnpj": "11.222.333/0001-81"}
    Output: {"valid": true, "receita_federal": {...}}
    
    Performance: ~200ms
    Memory: 128MB
    Timeout: 30s
    """
```

#### **2. Processador CSV (`import_csv.py`)**
```python
def lambda_handler(event, context):
    """
    Processamento chunked + S3 storage
    Input: {"csv_data": "...", "chunk_size": 100}
    Output: {"processed": 1500, "s3_key": "..."}
    
    Performance: ~2-5min (dependendo do arquivo)
    Memory: 512MB  
    Timeout: 300s
    """
```

#### **3. Gerador Relatórios (`generate_reports.py`)**
```python
def lambda_handler(event, context):
    """
    Estatísticas + notificação SNS
    Input: {"include_data": true}
    Output: {"statistics": {...}, "notification_sent": true}
    
    Performance: ~500ms
    Memory: 256MB
    Timeout: 120s
    """
```

## 🔐 Sistema de Autenticação

### **JWT Implementation**
```python
# Token structure
{
  "sub": "username",
  "is_admin": true,
  "scopes": ["admin"],
  "exp": 1640995200,
  "iat": 1640991600
}

# Permissões
- Admin: Full CRUD + Lambda access
- Leitor: Read-only access
- Lambda: Special endpoints access
```

### **Endpoints de Autenticação**
```bash
POST /auth/register    # Criar usuário
POST /auth/login       # Login JWT  
GET  /auth/me          # Info do usuário atual
```

## 📊 Database Schema

### **Modelo de Dados**
```sql
-- Empresas (tabela principal)
CREATE TABLE empresas (
    id SERIAL PRIMARY KEY,
    cnpj VARCHAR(18) UNIQUE NOT NULL,
    razao_social VARCHAR(255) NOT NULL,
    nome_fantasia VARCHAR(255),
    situacao_cadastral VARCHAR(50),
    data_situacao_cadastral DATE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Estabelecimentos  
CREATE TABLE estabelecimentos (
    id SERIAL PRIMARY KEY,
    empresa_id INTEGER REFERENCES empresas(id),
    cnpj VARCHAR(18) NOT NULL,
    matriz_filial VARCHAR(10),
    nome_fantasia VARCHAR(255),
    situacao_cadastral VARCHAR(50)
);

-- Sócios
CREATE TABLE socios (
    id SERIAL PRIMARY KEY,
    empresa_id INTEGER REFERENCES empresas(id),
    nome VARCHAR(255) NOT NULL,
    cpf_cnpj VARCHAR(18),
    qualificacao VARCHAR(100),
    data_entrada DATE
);
```

## 🛠️ APIs e Endpoints

### **📋 Endpoints FastAPI Tradicionais**

#### **Empresas**
```bash
GET    /empresas/              # Listar (paginado)
POST   /empresas/              # Criar nova
GET    /empresas/{id}          # Buscar por ID
PUT    /empresas/{id}          # Atualizar completa
PATCH  /empresas/{id}          # Atualizar parcial
DELETE /empresas/{id}          # Deletar
GET    /empresas/search        # Busca avançada
```

#### **Estabelecimentos**
```bash
GET    /estabelecimentos/                    # Listar todos
POST   /estabelecimentos/                    # Criar novo
GET    /estabelecimentos/{id}                # Buscar por ID
PUT    /estabelecimentos/{id}                # Atualizar
DELETE /estabelecimentos/{id}                # Deletar
GET    /estabelecimentos/empresa/{empresa_id} # Por empresa
```

#### **Sócios**
```bash
GET    /socios/                 # Listar todos  
POST   /socios/                 # Criar novo
GET    /socios/{id}             # Buscar por ID
PUT    /socios/{id}             # Atualizar
DELETE /socios/{id}             # Deletar
GET    /socios/empresa/{empresa_id} # Por empresa
```

### **⚡ Endpoints Lambda Integration**

#### **Validação CNPJ**
```bash
POST /lambda/validate-cnpj-async
Content-Type: application/json
Authorization: Bearer {token}

{
  "cnpj": "11.222.333/0001-81"
}

# Response
{
  "success": true,
  "user": "lambda_user",
  "processing_location": "AWS Lambda us-east-1",
  "result": {
    "cnpj": "11.222.333/0001-81", 
    "valid": true,
    "validation_method": "ReceitaWS + Mathematical",
    "receita_federal": {
      "razao_social": "Empresa Exemplo LTDA",
      "situacao": "ATIVA",
      "cnae_principal": "6201-5/00"
    }
  }
}
```

#### **Processamento CSV**
```bash
POST /lambda/process-csv
Content-Type: multipart/form-data
Authorization: Bearer {token}

file: empresas.csv
chunk_size: 100

# Response  
{
  "success": true,
  "result": {
    "filename": "empresas.csv",
    "total_lines": 15000,
    "valid_lines": 14850,
    "chunk_size": 100,
    "estimated_chunks": 149,
    "s3_bucket": "lambda-csv-storage",
    "s3_key": "processed/empresas_20251018_143022.csv"
  }
}
```

#### **Geração Relatórios**
```bash
POST /lambda/generate-report
Content-Type: application/json
Authorization: Bearer {token}

{
  "include_data": true
}

# Response
{
  "success": true,
  "result": {
    "resumo_executivo": {
      "total_empresas": 15000,
      "data_geracao": "2025-10-18T14:30:22",
      "periodo_analise": "2025-01 a 2025-10"
    },
    "distribuicao_situacao": {
      "ATIVA": 12000,
      "BAIXADA": 2000,
      "SUSPENSA": 800,
      "INAPTA": 200
    },
    "distribuicao_uf": {
      "SP": 6000,
      "RJ": 3000,
      "MG": 2000,
      "RS": 1500,
      "PR": 1200,
      "outros": 1300
    },
    "notification": {
      "sns_message_id": "12345678-1234-1234-1234-123456789012",
      "status": "sent"
    }
  }
}
```

## 🔧 Configuração de Desenvolvimento

### **Instalação Local**
```powershell
# 1. Clone do repositório
git clone https://github.com/elielguedes/Relatorio_Eliel_Guedes.git
cd Relatorio_Eliel_Guedes/framework_udf

# 2. Ambiente virtual
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. Dependências
pip install -r requirements.txt
pip install boto3  # Para AWS integration

# 4. Executar aplicação
python -m uvicorn app.main:app --reload --port 8000
```

### **Estrutura de Dados de Teste**
```python
# Dados exemplo para teste
test_empresa = {
    "cnpj": "11.222.333/0001-81",
    "razao_social": "Empresa Teste LTDA",
    "nome_fantasia": "Teste Corp", 
    "situacao_cadastral": "ATIVA"
}

test_user = {
    "username": "admin",
    "password": "admin123",
    "is_admin": true
}
```

## 🚀 Deploy e Produção

### **Deploy AWS Lambda**
```powershell
# 1. Configurar AWS CLI
aws configure

# 2. Executar deploy automático
cd lambda_functions
.\deploy.ps1

# 3. Verificar funções
aws lambda list-functions --query 'Functions[].FunctionName'
```

### **Monitoramento**
```bash
# Logs CloudWatch
aws logs describe-log-groups --log-group-name-prefix "/aws/lambda/"

# Métricas
aws cloudwatch get-metric-statistics \
  --namespace "AWS/Lambda" \
  --metric-name "Invocations" \
  --start-time 2025-10-18T00:00:00Z \
  --end-time 2025-10-18T23:59:59Z \
  --period 3600 \
  --statistics Sum
```

## 🧪 Testes e Validação

### **Testes de Unidade**
```python
# Executar testes
python -m pytest tests/ -v

# Coverage
python -m pytest --cov=app tests/
```

### **Testes de Integração**
```bash
# Teste endpoints Lambda
curl -X POST "http://127.0.0.1:8000/lambda/test-integration" \
  -H "Authorization: Bearer test-token"

# Teste CNPJ validation
curl -X POST "http://127.0.0.1:8000/lambda/validate-cnpj-async" \
  -H "Authorization: Bearer test-token" \
  -H "Content-Type: application/json" \
  -d '{"cnpj": "11.222.333/0001-81"}'
```

## 📈 Performance e Otimização

### **Métricas de Performance**
- **FastAPI Response Time**: ~50-200ms
- **Lambda Cold Start**: ~1-2s
- **Lambda Warm**: ~100-500ms
- **Database Queries**: ~10-50ms (SQLite)
- **JWT Validation**: ~5-10ms

### **Otimizações Implementadas**
- ✅ **Connection Pooling** (SQLAlchemy)
- ✅ **JWT Token Caching**
- ✅ **Lambda Warm-up** (keep-alive)
- ✅ **Async/await** patterns
- ✅ **Pydantic validation** caching
- ✅ **Database indexing** otimizado

## 🛡️ Segurança

### **Implementações de Segurança**
```python
# 1. Password hashing (bcrypt + SHA256)
password_hash = bcrypt_sha256.hash(password)

# 2. JWT com expiração
token = jwt.encode({
    "sub": username,
    "exp": datetime.utcnow() + timedelta(minutes=30)
}, SECRET_KEY)

# 3. CORS configurado
app.add_middleware(CORSMiddleware, 
    allow_origins=["http://localhost:3000"],
    allow_credentials=True)

# 4. Rate limiting (production)
@limiter.limit("5/minute")
async def login_endpoint():
    pass
```

### **Boas Práticas Aplicadas**
- ✅ **Environment variables** para secrets
- ✅ **Input validation** (Pydantic)
- ✅ **SQL injection protection** (SQLAlchemy ORM)
- ✅ **HTTPS ready** (TLS configuration)
- ✅ **Access control** (JWT scopes)

## 📋 Troubleshooting

### **Problemas Comuns**

#### **1. Erro de Import**
```bash
ModuleNotFoundError: No module named 'app'
# Solução: Execute do diretório correto
cd framework_udf && python -m uvicorn app.main:app
```

#### **2. Database Connection**
```bash
sqlalchemy.exc.OperationalError: database is locked
# Solução: Verificar se SQLite não está aberto em outro processo
```

#### **3. AWS Credentials**
```bash
boto3.exceptions.NoCredentialsError
# Solução: aws configure ou variáveis de ambiente
```

#### **4. Lambda Timeout**
```bash
Task timed out after 30.00 seconds
# Solução: Aumentar timeout na configuração Lambda
```

## 🔗 Recursos Adicionais

### **Links Úteis**
- 📖 **FastAPI Docs**: https://fastapi.tiangolo.com/
- ⚡ **AWS Lambda**: https://docs.aws.amazon.com/lambda/
- 🗄️ **SQLAlchemy**: https://docs.sqlalchemy.org/
- 🔐 **JWT**: https://jwt.io/
- 📊 **Pydantic**: https://pydantic-docs.helpmanual.io/

### **Ferramentas de Desenvolvimento**
- **VS Code Extensions**: Python, FastAPI, AWS Toolkit
- **Postman Collection**: Para testes de API
- **AWS Console**: Monitoramento Lambda
- **DBeaver**: Visualização do banco SQLite

---

## 📄 Changelog

### **v2.0.0** (Outubro 2025)
- ✅ **Adicionado**: Integração completa AWS Lambda
- ✅ **Adicionado**: Simulação local das funções Lambda  
- ✅ **Adicionado**: Scripts de deploy automatizado
- ✅ **Melhorado**: Sistema de autenticação
- ✅ **Melhorado**: Documentação técnica completa

### **v1.0.0** (Setembro 2025)  
- ✅ **Inicial**: FastAPI + SQLAlchemy
- ✅ **Inicial**: CRUD completo
- ✅ **Inicial**: Autenticação JWT
- ✅ **Inicial**: Documentação Swagger

---

**📞 Suporte**: eliel@universidade.edu.br  
**🐙 Repositório**: https://github.com/elielguedes/Relatorio_Eliel_Guedes