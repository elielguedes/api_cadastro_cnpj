# 📚 Documentação Técnica Completa - API Cadastro CNPJ

## 📋 Índice
1. [Visão Geral](#visao-geral)
2. [Arquitetura do Sistema](#arquitetura)
3. [Modelagem de Dados](#modelagem)
4. [Endpoints da API](#endpoints)
5. [Autenticação e Segurança](#autenticacao)
6. [Deployment e Infraestrutura](#deployment)
7. [Monitoramento e Logs](#monitoramento)
8. [Desenvolvimento Local](#desenvolvimento)
9. [Testes](#testes)
10. [Troubleshooting](#troubleshooting)

---

## 🎯 Visão Geral {#visao-geral}

### Objetivo do Projeto
Desenvolvimento de uma **API RESTful completa** para gestão de dados empresariais brasileiros, utilizando informações públicas do portal **dados.gov.br**. O projeto demonstra aplicação prática de:

- ✅ **FastAPI** para desenvolvimento de APIs modernas
- ✅ **SQLAlchemy** para ORM e modelagem relacional
- ✅ **JWT** para autenticação e autorização
- ✅ **PostgreSQL/SQLite** para persistência de dados
- ✅ **AWS EC2** para deploy em produção
- ✅ **Docker** para containerização
- ✅ **Nginx** como proxy reverso

### Principais Funcionalidades
- 🏢 **Gestão de Empresas**: CRUD completo com validação de CNPJ
- 🏪 **Estabelecimentos**: Filiais e unidades vinculadas às empresas
- 👥 **Sócios**: Pessoas físicas/jurídicas associadas
- 🏷️ **Sistema de Tags**: Categorização flexível (N:N)
- 🔐 **Controle de Acesso**: Perfis admin e leitor
- 📊 **Filtros e Paginação**: Consultas otimizadas
- 📂 **Import/Export CSV**: Integração com dados.gov.br

---

## 🏗️ Arquitetura do Sistema {#arquitetura}

### Padrões Arquiteturais Utilizados

#### 🔄 **Layered Architecture** (Arquitetura em Camadas)
```
┌─────────────────────────────────────┐
│        🌐 Presentation Layer        │
│     FastAPI Routers & Endpoints     │
│  (/empresas, /auth, /estabeleci...) │
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│         ⚙️ Service Layer           │
│      Business Logic & Rules        │
│   (empresa_service, auth_service)   │
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│         💾 Data Layer              │
│    SQLAlchemy Models & Database     │
│     (Empresa, Usuario, Socio)       │
└─────────────────────────────────────┘
```

#### 📋 **Service Layer Pattern**
- **Separação de responsabilidades**: Routers focam em HTTP, Services em lógica de negócio
- **Reutilização de código**: Services podem ser chamados por múltiplos endpoints
- **Testabilidade**: Lógica de negócio isolada e testável independentemente

#### 🔒 **Dependency Injection**
- **Database Session**: Injetada via `Depends(get_db)`
- **Current User**: Injetada via `Depends(get_current_user)`
- **Admin Authorization**: Via `Depends(require_admin)`

### Stack Tecnológico

#### 🐍 **Backend**
- **FastAPI 0.110.0**: Framework web moderno e performático
- **SQLAlchemy 2.0+**: ORM com suporte a relacionamentos complexos
- **Alembic**: Migrations e versionamento de schema
- **Pydantic**: Validação de dados e serialização
- **Passlib + BCrypt**: Hash seguro de senhas
- **Python-Jose**: JWT tokens para autenticação

#### 💾 **Banco de Dados**
- **PostgreSQL**: Produção (robusto, transacional)
- **SQLite**: Desenvolvimento (rápido, zero-config)
- **Relacionamentos**: 1:N e N:N implementados corretamente

#### 🌐 **Infraestrutura**
- **AWS EC2**: Ubuntu 22.04 LTS
- **Nginx**: Proxy reverso e load balancer
- **Systemd**: Gerenciamento de serviços
- **Docker**: Containerização opcional

---

## 🗄️ Modelagem de Dados {#modelagem}

### Entidades e Relacionamentos

#### 👤 **Usuario** (Tabela: `usuarios`)
```python
class Usuario(Base):
    id: int              # PK - Identificador único
    username: str        # UK - Login único
    hashed_password: str # Senha criptografada (bcrypt)  
    is_admin: bool       # Flag de administrador
```

#### 🏢 **Empresa** (Tabela: `empresas`)
```python
class Empresa(Base):
    id: int              # PK - Identificador único
    nome: str            # Razão social
    cnpj: str            # UK - CNPJ validado (formato: XX.XXX.XXX/XXXX-XX)
    # Relacionamentos
    estabelecimentos: List[Estabelecimento]  # 1:N
    tags: List[Tag]      # N:N via empresa_tags
```

#### 🏪 **Estabelecimento** (Tabela: `estabelecimentos`)
```python
class Estabelecimento(Base):
    id: int              # PK - Identificador único
    nome: str            # Nome do estabelecimento/filial
    empresa_id: int      # FK - Referência à empresa
    # Relacionamentos
    empresa: Empresa     # N:1
    socios: List[Socio]  # 1:N
```

#### 👥 **Socio** (Tabela: `socios`)
```python
class Socio(Base):
    id: int                    # PK - Identificador único
    nome: str                  # Nome do sócio
    estabelecimento_id: int    # FK - Referência ao estabelecimento
    # Relacionamentos  
    estabelecimento: Estabelecimento  # N:1
```

#### 🏷️ **Tag** (Tabela: `tags`)
```python
class Tag(Base):
    id: int              # PK - Identificador único
    name: str            # UK - Nome único da tag
    # Relacionamentos
    empresas: List[Empresa]  # N:N via empresa_tags
```

### Relacionamentos Implementados

#### 🔗 **1:N - Empresa → Estabelecimentos**
```python
# Na classe Empresa
estabelecimentos = relationship("Estabelecimento", back_populates="empresa")

# Na classe Estabelecimento  
empresa_id = Column(Integer, ForeignKey("empresas.id"))
empresa = relationship("Empresa", back_populates="estabelecimentos")
```

#### 🔗 **1:N - Estabelecimento → Sócios**
```python
# Na classe Estabelecimento
socios = relationship("Socio", back_populates="estabelecimento")

# Na classe Socio
estabelecimento_id = Column(Integer, ForeignKey("estabelecimentos.id"))
estabelecimento = relationship("Estabelecimento", back_populates="socios")
```

#### 🔗 **N:N - Empresa ↔ Tags**
```python
# Tabela de associação
empresa_tags = Table(
    'empresa_tags',
    Base.metadata,
    Column('empresa_id', Integer, ForeignKey('empresas.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)

# Relacionamento N:N
tags = relationship("Tag", secondary=empresa_tags, back_populates="empresas")
empresas = relationship("Empresa", secondary=empresa_tags, back_populates="tags")
```

---

## 🛣️ Endpoints da API {#endpoints}

### Base URL
- **Desenvolvimento**: `http://localhost:8000`
- **Produção**: `http://18.118.167.28:8000`
- **Documentação**: `/docs` (Swagger UI interativo)

### 🔐 **Autenticação** (`/auth`)

#### POST `/auth/register`
**Registrar novo usuário**
```json
{
  "username": "usuario",
  "password": "senha123",
  "is_admin": false
}
```

#### POST `/auth/login` 
**Login e obtenção de token**
```json
{
  "username": "admin",
  "password": "admin123"
}
```
**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

### 🏢 **Empresas** (`/empresas`)

#### GET `/empresas/`
**Listar empresas com filtros e paginação**
```
GET /empresas/?skip=0&limit=10&nome=petrobras&order_by=nome&order=asc
```

#### POST `/empresas/` 🔒 **(Admin)**
**Criar nova empresa**
```json
{
  "nome": "PETRÓLEO BRASILEIRO S.A.",
  "cnpj": "33.000.167/0001-01"
}
```

#### GET `/empresas/{id}`
**Consultar empresa específica**

#### PUT `/empresas/{id}` 🔒 **(Admin)**
**Atualizar empresa**

#### DELETE `/empresas/{id}` 🔒 **(Admin)**
**Remover empresa**

### 🏪 **Estabelecimentos** (`/estabelecimentos`)

#### GET `/estabelecimentos/`
**Listar estabelecimentos**

#### POST `/estabelecimentos/` 🔒 **(Admin)**
**Criar estabelecimento**
```json
{
  "nome": "Matriz Rio de Janeiro",
  "empresa_id": 1
}
```

#### GET `/estabelecimentos/{id}`
**Consultar estabelecimento específico**

### 👥 **Sócios** (`/socios`)

#### GET `/socios/`
**Listar sócios**

#### POST `/socios/` 🔒 **(Admin)**
**Criar sócio**
```json
{
  "nome": "João Silva Santos",
  "estabelecimento_id": 1
}
```

### 🏷️ **Tags** (`/tags`)

#### GET `/tags/`
**Listar todas as tags**

#### POST `/tags/` 🔒 **(Admin)**
**Criar nova tag**
```json
{
  "name": "Petróleo e Gás"
}
```

#### POST `/tags/{tag_id}/empresas/{empresa_id}` 🔒 **(Admin)**
**Associar tag à empresa**

---

## 🔐 Autenticação e Segurança {#autenticacao}

### JWT (JSON Web Tokens)

#### Configuração
```python
SECRET_KEY = "sua-chave-secreta-super-segura"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

#### Fluxo de Autenticação
1. **Login**: `POST /auth/login` com username/password
2. **Token**: API retorna JWT token válido por 30min
3. **Headers**: Todas as requisições incluem `Authorization: Bearer {token}`
4. **Validação**: Middleware verifica token em rotas protegidas

#### Níveis de Acesso
- 👤 **Leitor**: Acesso apenas GET (consultas)
- 👨‍💼 **Admin**: Acesso completo (CRUD)

#### Implementação de Segurança
```python
# Hash seguro de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Middleware de autenticação
def get_current_user(token: str = Depends(oauth2_scheme)):
    # Validação JWT + verificação de usuário
    
# Middleware de autorização  
def require_admin(current_user: Usuario = Depends(get_current_user)):
    # Verificação de permissão admin
```

---

## 🚀 Deployment e Infraestrutura {#deployment}

### AWS EC2 - Ambiente de Produção

#### Configuração da Instância
- **Tipo**: t3.micro (1 vCPU, 1GB RAM)
- **OS**: Ubuntu 22.04 LTS
- **Storage**: 8GB SSD GP2
- **IP Público**: 18.118.167.28

#### Security Groups
```
Inbound Rules:
- SSH (22): 0.0.0.0/0
- HTTP (80): 0.0.0.0/0  
- HTTPS (443): 0.0.0.0/0
- Custom TCP (8000): 0.0.0.0/0
```

#### Serviços Configurados

##### 🌐 **Nginx** (Proxy Reverso)
```nginx
server {
    listen 80;
    server_name _;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

##### 🚀 **Systemd Service** (FastAPI)
```ini
[Unit]
Description=FastAPI application
After=network.target

[Service] 
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/api_cadastro_cnpj/api_cadastro_cnpj
Environment=PATH=/home/ubuntu/api_cadastro_cnpj/api_cadastro_cnpj/.venv/bin
ExecStart=/home/ubuntu/api_cadastro_cnpj/api_cadastro_cnpj/.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

### Deploy Automatizado

#### Script de Deploy (`deploy/quick-deploy.sh`)
```bash
#!/bin/bash
# Deploy automatizado completo
# 1. Atualização do sistema
# 2. Instalação de dependências
# 3. Clone do repositório
# 4. Setup do ambiente Python
# 5. Configuração de serviços
# 6. Inicialização
```

---

## 📊 Monitoramento e Logs {#monitoramento}

### Logs do Sistema

#### FastAPI Application
```bash
# Logs da aplicação
sudo journalctl -u fastapi -f

# Logs com timestamp
sudo journalctl -u fastapi --since "1 hour ago"
```

#### Nginx Access/Error
```bash
# Logs de acesso
sudo tail -f /var/log/nginx/access.log

# Logs de erro  
sudo tail -f /var/log/nginx/error.log
```

### Health Checks

#### Endpoint de Saúde
```
GET /health
```
**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-18T19:45:00Z",
  "version": "1.0.0",
  "database": "connected"
}
```

#### Monitoramento de Serviços
```bash
# Status FastAPI
sudo systemctl status fastapi

# Status Nginx
sudo systemctl status nginx

# Uso de recursos
htop
df -h
```

---

## 💻 Desenvolvimento Local {#desenvolvimento}

### Setup Inicial

#### 1. Clone e Ambiente
```bash
git clone https://github.com/elielguedes/api_cadastro_cnpj.git
cd api_cadastro_cnpj
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.\.venv\Scripts\Activate.ps1  # Windows
```

#### 2. Dependências
```bash
pip install -r requirements.txt
```

#### 3. Banco de Dados
```bash
# SQLite (padrão)
alembic upgrade head

# PostgreSQL (opcional)
export DATABASE_URL="postgresql+psycopg2://user:pass@localhost:5432/db"
alembic upgrade head
```

#### 4. Executar Aplicação  
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Desenvolvimento com Docker

#### docker-compose.yml
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/empresas_db
    depends_on:
      - db
      
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=empresas_db
      - POSTGRES_USER=postgres  
      - POSTGRES_PASSWORD=postgres
    ports:
      - "5432:5432"
```

#### Comandos Docker
```bash
# Build e start
docker-compose up --build

# Apenas start
docker-compose up -d

# Logs
docker-compose logs -f app
```

---

## 🧪 Testes {#testes}

### Testes Automatizados

#### Estrutura de Testes
```
tests/
├── test_auth.py          # Autenticação e autorização
├── test_empresas.py      # CRUD de empresas
├── test_estabelecimentos.py  # CRUD de estabelecimentos  
├── test_socios.py        # CRUD de sócios
└── conftest.py           # Configurações e fixtures
```

#### Executar Testes
```bash
# Todos os testes
pytest

# Com cobertura
pytest --cov=app

# Testes específicos
pytest tests/test_auth.py -v
```

### Collection Postman

#### Importar Collection
1. Abrir Postman
2. Importar `postman_collection_complete.json`
3. Configurar variável `base_url`
4. Executar "Login" para obter token

#### Testes Inclusos
- ✅ **Autenticação**: Register, Login, Token validation
- ✅ **Empresas**: CRUD completo com filtros
- ✅ **Estabelecimentos**: CRUD e associações
- ✅ **Sócios**: CRUD e relacionamentos
- ✅ **Tags**: Sistema de categorização N:N
- ✅ **Autorização**: Testes de permissão admin/leitor

---

## 🔧 Troubleshooting {#troubleshooting}

### Problemas Comuns

#### ❌ **Docker não inicia (29 erros)**
```bash
# Limpar cache Docker
Remove-Item -Path "$env:APPDATA\Docker" -Recurse -Force
Remove-Item -Path "$env:LOCALAPPDATA\Docker" -Recurse -Force

# Reinstalar WSL2
Enable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform
```

#### ❌ **Erro de conexão PostgreSQL**
```python
# Verificar DATABASE_URL
DATABASE_URL = "postgresql+psycopg2://user:pass@host:5432/db"

# Fallback para SQLite automático
if not DATABASE_URL:
    engine = create_engine("sqlite:///./app.db")
```

#### ❌ **JWT Token inválido**
```python  
# Verificar SECRET_KEY e expiração
SECRET_KEY = "sua-chave-super-secreta"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

#### ❌ **Permissões EC2**
```bash
# Corrigir permissões SSH key
chmod 400 fastapi_app_key.pem

# Verificar Security Groups
# Porta 8000 deve estar liberada
```

### Logs de Debug

#### Aplicação
```bash
# Modo debug local
export ENVIRONMENT=development
uvicorn app.main:app --reload --log-level debug
```

#### Produção
```bash
# Logs detalhados EC2
sudo journalctl -u fastapi -f --no-pager
```

---

## 📞 Suporte e Contribuições

### Contato
- **Desenvolvedor**: Eliel Guedes
- **GitHub**: [@elielguedes](https://github.com/elielguedes)
- **LinkedIn**: [Eliel Guedes](https://linkedin.com/in/elielguedes)

### Como Contribuir
1. Fork do repositório
2. Branch feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit (`git commit -m 'feat: adicionar nova funcionalidade'`)
4. Push (`git push origin feature/nova-funcionalidade`)
5. Pull Request

### Licença
MIT License - Veja [LICENSE](LICENSE) para detalhes.

---

**Documentação atualizada em:** 18 de Outubro de 2025  
**Versão da API:** 1.0.0  
**Status:** ✅ Produção Estável