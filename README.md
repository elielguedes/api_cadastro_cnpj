# 🏢 API Cadastro CNPJ - FastAPI

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-green.svg)](https://fastapi.tiangolo.com)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-orange.svg)](https://sqlalchemy.org)
[![Deploy](https://img.shields.io/badge/Deploy-AWS_EC2-yellow.svg)](http://18.118.167.28:8000/docs)
[![Status](https://img.shields.io/badge/Status-Produção-brightgreen.svg)](http://18.118.167.28:8000)

## 📋 Descrição
**API RESTful completa** para cadastro, consulta e gestão de empresas brasileiras (CNPJ), utilizando **dados públicos do portal dados.gov.br**. Desenvolvida com **FastAPI**, **SQLAlchemy** e arquitetura robusta com suporte a **PostgreSQL** (produção) e **SQLite** (desenvolvimento).

> 🎯 **Projeto acadêmico** para disciplina de **Técnicas de Desenvolvimento de Algoritmos**  
> 📊 **Dados reais** do governo brasileiro via dados.gov.br  
> 🚀 **Deploy funcional** em produção na AWS EC2

## ✨ Funcionalidades Principais
- 🔐 **Autenticação JWT** com controle de permissões (admin/leitor)
- 📊 **CRUD completo** para empresas, estabelecimentos e sócios
- 🏷️ **Sistema de Tags** com relacionamento N:N
- 🔍 **Filtros avançados**, ordenação e paginação
- 📖 **Documentação automática** interativa (Swagger/OpenAPI)
- ✅ **Validação de CNPJ** integrada com dígitos verificadores
- 📂 **Import/Export** de dados CSV do dados.gov.br
- 🔄 **Migrations Alembic** para versionamento de banco
- 🧪 **Testes automatizados** com Postman e pytest
- 🐳 **Dockerizado** com PostgreSQL
- ☁️ **Deploy AWS EC2** em produção funcionando

## 🏃‍♂️ Início Rápido

### 💻 **Desenvolvimento Local (Recomendado)**
```bash
# 1. Clone o repositório
git clone https://github.com/elielguedes/Relatorio_Eliel_Guedes.git
cd Relatorio_Eliel_Guedes/framework_udf

# 2. Crie e ative ambiente virtual (Python 3.10+)
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# Linux/Mac
source .venv/bin/activate

# 3. Instale dependências
pip install -r requirements.txt

# 4. Inicie aplicação (SQLite automático)
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# 5. OU use script otimizado
.\.venv\Scripts\python.exe start_sqlite.py
```

### 🚀 **Acessar Aplicação**

#### 💻 **Local (Desenvolvimento)**
- 🌐 **API**: http://127.0.0.1:8000
- 📚 **Docs**: http://127.0.0.1:8000/docs  
- ❤️ **Health**: http://127.0.0.1:8000/health

#### ☁️ **Produção (AWS EC2)**  
- 🌍 **API**: [http://18.118.167.28:8000](http://18.118.167.28:8000)
- 📖 **Docs**: [http://18.118.167.28:8000/docs](http://18.118.167.28:8000/docs)

#### 🔐 **Credenciais Padrão**
- 👨‍💼 **Admin**: `admin` / `admin123`
- 👤 **Leitor**: `leitor` / `leitor123`

### Com Docker

**Desenvolvimento:**
```bash
# Desenvolvimento com hot-reload
docker-compose -f docker-compose.dev.yml up --build

# Acesse: http://localhost:8001/docs
```

**Produção:**
```bash
# Produção com PostgreSQL
docker-compose up --build

# Com Nginx (SSL/proxy)
docker-compose --profile production up --build

# Acesse: http://localhost:8000/docs
```

## 📁 Estrutura Organizada do Projeto

```
📦 framework_udf/
├── 🚀 app/                          # Código principal da aplicação
│   ├── 🏗️  models/
│   │   ├── __init__.py              # Documentação dos modelos
│   │   └── models.py                # Modelos ORM SQLAlchemy
│   ├── 🛣️  routers/                 # Endpoints da API organizados
│   │   ├── empresas.py              # CRUD de empresas
│   │   ├── estabelecimentos.py      # CRUD de estabelecimentos
│   │   └── socios.py                # CRUD de sócios
│   ├── ⚙️  services/                # Lógica de negócio (Service Layer)
│   │   ├── __init__.py              # Documentação dos serviços
│   │   ├── empresa_service.py       # Regras de negócio empresas
│   │   ├── estabelecimento_service.py # Regras estabelecimentos
│   │   └── socio_service.py         # Regras de negócio sócios
│   ├── 🔧 utils/                    # Utilitários e helpers
│   │   ├── __init__.py
│   │   └── cnpj_validator.py        # Validação de CNPJ
│   ├── 📊 schemas.py                # Schemas Pydantic (validação)
│   ├── 🔐 auth.py                   # Autenticação JWT completa
│   ├── 💾 database.py               # Configuração SQLAlchemy
│   └── 🚀 main.py                   # App FastAPI principal
├── 📂 data/                         # Dados públicos do dados.gov.br
│   ├── repasse-s.csv                # Dataset principal (empresas)
│   ├── Empresas.csv                 # Dados complementares
│   └── import_rejeitados.csv        # Log de importações rejeitadas
├── 📜 scripts/                      # Scripts utilitários
│   ├── import_repasse.py            # Importador CSV principal
│   ├── import_repasse_with_report.py # Import com relatório
│   ├── export_empresas.py           # Exportador de dados
│   └── seed_postgres.py             # Seed para PostgreSQL
├── 🧪 tests/                        # Testes automatizados
│   ├── test_empresas.py             # Testes CRUD empresas
│   ├── test_estabelecimentos.py     # Testes estabelecimentos
│   ├── test_socios.py               # Testes sócios
│   └── test_auth.py                 # Testes autenticação
├── 🔄 alembic/                      # Migrations de banco
│   ├── env.py                       # Configuração Alembic
│   └── versions/                    # Histórico de migrations
├── 🐳 docker/                       # Containerização
│   ├── docker-compose.yml          # Orquestração Docker
│   ├── Dockerfile                   # Imagem da aplicação
│   └── nginx.conf                   # Configuração proxy
├── 📋 docs/                         # Documentação adicional
│   ├── RELATORIO.md                 # Relatório técnico completo
│   ├── SOLUCAO_29_ERROS_DOCKER.md   # Troubleshooting Docker
│   ├── STATUS_FINAL_FUNCIONANDO.md  # Status do projeto
│   └── DEPLOY_EC2_AGORA.md          # Guia de deploy AWS
├── 🌐 deploy/                       # Scripts de deploy
│   ├── quick-deploy.sh              # Deploy automatizado EC2
│   ├── nginx_config                 # Config Nginx produção
│   └── systemd_service              # Service Linux
├── 📮 postman_collection_complete.json # Testes Postman
├── 📦 requirements.txt              # Dependências Python
├── ⚙️  alembic.ini                 # Config migrations
├── 📖 README.md                     # Documentação principal
└── 🔒 .env                         # Variáveis de ambiente
```

### 🏗️ **Arquitetura em Camadas:**
- **🚀 Presentation Layer**: FastAPI routers (`routers/`)
- **⚙️ Service Layer**: Lógica de negócio (`services/`)  
- **🏗️ Data Layer**: Models SQLAlchemy (`models/`)
- **🔐 Security Layer**: Autenticação JWT (`auth.py`)
- **📊 Validation Layer**: Schemas Pydantic (`schemas.py`)

## 📊 Diagrama ER - Modelagem de Dados

```mermaid
erDiagram
    %% === ENTIDADES PRINCIPAIS ===
    
    USUARIO ||--o{ EMPRESA : "cria/gerencia"
    EMPRESA ||--o{ ESTABELECIMENTO : "possui (1:N)"
    ESTABELECIMENTO ||--o{ SOCIO : "possui (1:N)"  
    EMPRESA }o--o{ TAG : "rotulada_com (N:N)"

    %% === DEFINIÇÃO DAS TABELAS ===
    
    USUARIO {
        int id PK "Chave primária"
        string username UK "Login único do usuário"
        string hashed_password "Senha criptografada (bcrypt)"
        bool is_admin "Permissão de administrador"
        datetime created_at "Data de criação"
    }

    EMPRESA {
        int id PK "Chave primária"
        string nome "Razão social da empresa"
        string cnpj UK "CNPJ único validado"
        datetime created_at "Data de cadastro"
        datetime updated_at "Última atualização"
    }

    ESTABELECIMENTO {
        int id PK "Chave primária"
        string nome "Nome do estabelecimento/filial"
        int empresa_id FK "Referência à empresa"
        string endereco "Endereço completo"
        datetime created_at "Data de criação"
    }

    SOCIO {
        int id PK "Chave primária"
        string nome "Nome do sócio"
        string cpf_cnpj "CPF ou CNPJ do sócio"
        string tipo "Pessoa física ou jurídica"
        int estabelecimento_id FK "Referência ao estabelecimento"
        datetime created_at "Data de cadastro"
    }

    TAG {
        int id PK "Chave primária"
        string name UK "Nome único da tag"
        string description "Descrição da categoria"
        datetime created_at "Data de criação"
    }
    
    %% === TABELA DE ASSOCIAÇÃO N:N ===
    EMPRESA_TAGS {
        int empresa_id FK "ID da empresa"
        int tag_id FK "ID da tag"
    }
```

### 🔗 **Relacionamentos Detalhados:**
- **1:N** - Uma **Empresa** pode ter múltiplos **Estabelecimentos**
- **1:N** - Um **Estabelecimento** pode ter múltiplos **Sócios**
- **N:N** - Uma **Empresa** pode ter múltiplas **Tags** e vice-versa
- **1:N** - Um **Usuário** pode gerenciar múltiplas **Empresas**

## Origem dos Dados
- Fonte: [dados.gov.br](https://dados.gov.br)
- Formato: CSV
- Periodicidade: conforme atualização oficial

## Relatório rápido / EDA

- Arquivo principal: `data/repasse-s.csv` (CSV delimitado por `;`).
- Colunas mapeadas para entidades: `Entidade` -> `Empresa.nome`, `UC/CNPJ` -> `Empresa.cnpj`.
- A carga inicial evita duplicatas por `nome`.
- Recomenda-se validar e normalizar CNPJ (remoção de máscara) antes de inserir em produção.

## Scripts de importação / exportação

Há scripts práticos no diretório `scripts/` para trabalhar com o CSV local:

- `scripts/import_repasse.py` — importa `data/repasse-s.csv` para o DB validando CNPJ.
- `scripts/import_repasse_with_report.py` — import com relatório de rejeitados em `data/import_rejeitados.csv`.
- `scripts/export_empresas.py` — exporta as empresas atuais do DB para `data/empresas_importadas.csv`.

Uso (PowerShell/Bash, no venv):

```bash
# ativar venv
# Windows
.\.venv\Scripts\Activate.ps1
# Linux/Mac  
source .venv/bin/activate

# importar (simples)
python scripts/import_repasse.py

# importar com relatório (gera data/import_rejeitados.csv)
python scripts/import_repasse_with_report.py

# exportar empresas
python scripts/export_empresas.py
```

Opções do `import_repasse_with_report.py`:

- `--dry-run` : processa o CSV e gera o relatório de rejeitados sem inserir nada no banco.
- `--limit N` : limita o número de linhas processadas (útil para testes).
- `--out <path>` : caminho do arquivo de relatório de rejeitados (padrão: `data/import_rejeitados.csv`).

Exemplo (dry-run, 100 linhas):

```powershell
venv\Scripts\python.exe scripts\import_repasse_with_report.py --dry-run --limit 100
```

## Migrations (Alembic)

1. Instale alembic no venv:

```powershell
pip install alembic
```

2. Crie a primeira migration (autogenerate usa `app.database.Base`):

```powershell
alembic revision --autogenerate -m "initial"
alembic upgrade head
```

Observação: já existe um esqueleto `alembic/env.py` apontando para `app.database.Base`.

Nota importante sobre estados locais de banco:
- Se você já executou a aplicação antes e as tabelas já existem (SQLite ou outro), o `alembic upgrade head` pode falhar porque as tabelas já existem. Nesse caso você pode:
    - Usar `alembic stamp head` para marcar a migration atual como aplicada sem tentar recriar tabelas (útil em dev local quando já existem dados).
    - Ou dropar o banco local (apenas em dev) e rodar `alembic upgrade head` novamente.

## Testes

1. Instale pytest e httpx:

```powershell
pip install pytest httpx
```

2. Execute os testes:

```powershell
pytest -q
```

Um teste básico (autenticação + CRUD de empresas) foi adicionado em `tests/test_auth_empresa.py`.

## 🌐 Deploy AWS EC2 - Ambiente de Produção

### 🚀 URLs Funcionais em Produção
- 🌍 **API Principal**: [http://18.118.167.28:8000](http://18.118.167.28:8000)
- 📚 **Documentação**: [http://18.118.167.28:8000/docs](http://18.118.167.28:8000/docs)
- ❤️ **Health Check**: [http://18.118.167.28:8000/health](http://18.118.167.28:8000/health)
- 🔧 **OpenAPI Schema**: [http://18.118.167.28:8000/openapi.json](http://18.118.167.28:8000/openapi.json)

### 🏗️ **Infraestrutura de Produção**
```
┌─────────────────────────────────────────┐
│          🌐 Internet                    │
│                 │                       │
│    ┌─────────────▼──────────────┐       │
│    │     AWS Security Group     │       │
│    │   Ports: 22, 80, 8000     │       │
│    └─────────────┬──────────────┘       │
│                  │                      │
│    ┌─────────────▼──────────────┐       │
│    │      🖥️ EC2 Instance       │       │
│    │    Ubuntu 22.04 LTS       │       │
│    │   IP: 18.118.167.28       │       │
│    │                           │       │
│    │  ┌─────────────────────┐  │       │
│    │  │   🌐 Nginx Proxy    │  │       │
│    │  │     Port: 80       │  │       │
│    │  └──────────┬──────────┘  │       │
│    │             │             │       │
│    │  ┌─────────────────────┐  │       │
│    │  │  🚀 FastAPI App    │  │       │
│    │  │    Port: 8000     │  │       │
│    │  │   Uvicorn Server  │  │       │
│    │  └──────────┬──────────┘  │       │
│    │             │             │       │
│    │  ┌─────────────────────┐  │       │
│    │  │  💾 SQLite DB      │  │       │
│    │  │   app.db           │  │       │
│    │  └─────────────────────┘  │       │
│    └─────────────────────────────┘       │
└─────────────────────────────────────────┘
```

### 📊 **Status dos Serviços**
- ✅ **FastAPI**: Rodando como systemd service
- ✅ **Nginx**: Proxy reverso configurado
- ✅ **SQLite**: Banco funcionando com dados carregados
- ✅ **Firewall**: Portas 80 e 8000 liberadas
- ✅ **SSL**: Pronto para configuração HTTPS
- ✅ **Logs**: Monitoramento via journalctl

---

## 📚 Documentação Completa

### 📋 **Documentos Principais**
- 📖 **[README.md](./README.md)** - Este arquivo (visão geral)
- 📊 **[RELATORIO.md](./RELATORIO.md)** - Relatório técnico acadêmico  
- 🏗️ **[ARQUITETURA_SISTEMA.md](./ARQUITETURA_SISTEMA.md)** - Diagramas e design
- 📚 **[DOCUMENTACAO_TECNICA_COMPLETA.md](./DOCUMENTACAO_TECNICA_COMPLETA.md)** - Referência técnica
- 📋 **[INDICE_DOCUMENTACAO.md](./INDICE_DOCUMENTACAO.md)** - 🗂️ **NAVEGUE AQUI!**

### 🚀 **Deploy e Status**  
- ✅ **[STATUS_FINAL_FUNCIONANDO.md](./STATUS_FINAL_FUNCIONANDO.md)** - Status atual
- 🌐 **[DEPLOY_EC2_AGORA.md](./DEPLOY_EC2_AGORA.md)** - Guia deploy AWS
- 🔍 **[ENCONTRAR_EC2_INFO.md](./ENCONTRAR_EC2_INFO.md)** - Informações EC2

### 🔧 **Troubleshooting**
- 🐳 **[SOLUCAO_29_ERROS_DOCKER.md](./SOLUCAO_29_ERROS_DOCKER.md)** - Problemas Docker

### 🧪 **Testes**
- 📮 **[postman_collection_complete.json](./postman_collection_complete.json)** - Collection Postman

### Pré-requisitos EC2
- Instância EC2 (t3.micro ou superior)
- Security Groups: SSH(22), HTTP(80), HTTPS(443), Custom TCP(8000)  
- Ubuntu 22.04 LTS (Python 3.10+ nativo)

### Deploy Automático
```bash
# 1. Conectar ao EC2
ssh -i fastapi_app_key.pem ubuntu@18.118.167.28

# 2. Clonar repositório
git clone https://github.com/elielguedes/Relatorio_Eliel_Guedes.git
cd Relatorio_Eliel_Guedes/framework_udf

# 3. Executar script de deploy
chmod +x deploy/quick-deploy.sh
./deploy/quick-deploy.sh

# 4. Configurar produção (opcional)
sudo cp deploy/nginx.conf /etc/nginx/conf.d/fastapi.conf
sudo cp deploy/fastapi-app.service /etc/systemd/system/
sudo systemctl enable fastapi-app
sudo systemctl start fastapi-app
```

### Compatibilidade
✅ **Python 3.9+** (compatível com Amazon Linux 2023)  
✅ **SQLAlchemy 2.0** com fallback automático SQLite → PostgreSQL  
✅ **Pydantic v2** com configuração otimizada  
✅ **FastAPI 0.119+** com todas as features modernas  

## 🧪 Testes

### Testes Automatizados
```bash
# Instalar dependências de teste
pip install pytest httpx

# Executar todos os testes
pytest -v

# Testes com cobertura
pytest --cov=app tests/
```

### Coleção Postman
📋 **Coleção completa disponível**: `postman_collection_complete.json`

**Inclui:**
- ✅ Autenticação JWT (admin/leitor)
- ✅ CRUD Empresas com filtros
- ✅ CRUD Estabelecimentos  
- ✅ CRUD Sócios
- ✅ Sistema de Tags com associações
- ✅ Variáveis de ambiente configuradas
- ✅ Testes automatizados com scripts
- ✅ Token management automático

**Como usar:**
1. Importe `postman_collection_complete.json` no Postman
2. Configure variável `base_url` (padrão: `http://localhost:8000`)
3. Execute "Login" para obter token automaticamente
4. Todos os endpoints estarão prontos para uso

## 📋 Próximos passos recomendados
- ✅ Validação e normalização de CNPJ implementada
- ✅ Coleção Postman atualizada
- ✅ Deploy EC2 configurado
- ⏳ CI/CD GitHub Actions
- ⏳ Monitoramento e logs centralizados
- ⏳ Cache Redis para performance
- ⏳ Rate limiting e segurança avançada

## Autores
- Eliel Guedes

## Licença
MIT

## Executando localmente (venv)

Este projeto pode ser executado localmente com um ambiente virtual Python.

1. Crie e ative o venv:

```powershell
python -m venv .\.venv
.\.venv\Scripts\Activate.ps1
```

2. Instale dependências:

```powershell
pip install -r requirements.txt
```

3. Inicie a aplicação:

```powershell
venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Ou use o helper `start.ps1` que já configura o venv e roda o servidor:

```powershell
.\start.ps1
# ou para habilitar o carregamento automático do CSV
.\start.ps1 -AutoLoad
```

Se quiser rodar a aplicação apontando para um PostgreSQL externo, exporte a variável de ambiente `DATABASE_URL`:

```powershell
$env:DATABASE_URL = "postgresql+psycopg2://user:pass@host:5432/dbname"
uvicorn app.main:app --reload

## Endpoints importantes (rápido resumo)

- Auth:
    - POST /auth/register — registrar usuário (retorna token)
    - POST /auth/login — login (retorna access_token)

- Empresas:
    - GET /empresas/ — lista (aceita skip/limit/nome/cnpj/order_by)
    - POST /empresas/ — criar (admin)
    - GET /empresas/{id} — detalhe (inclui `tags` via `EmpresaRead`)
    - PUT /empresas/{id} — atualizar (admin)
    - DELETE /empresas/{id} — remover (admin)

- Tags:
    - GET /tags/ — lista tags
    - POST /tags/ — criar tag (admin)
    - POST /tags/{tag_id}/empresas/{empresa_id} — associar tag a empresa (admin)
    - DELETE /tags/{tag_id}/empresas/{empresa_id} — remover associação (admin)

## Estado atual / O que foi feito

- Integração com SQLAlchemy e suporte a `DATABASE_URL` (Postgres) + fallback SQLite.
- Dependências de autorização centralizadas (`get_current_user`, `require_admin`).
- Implementação de `Tag` com relação N:N (`empresa_tags`) e endpoints correspondentes.
- Alembic: `env.py` configurado; se necessário foi usada a estratégia `alembic stamp head` em dev local para evitar conflitos quando as tabelas já existiam.
- Testes básicos (autenticação + CRUD de empresas) adicionados e passando.

```
