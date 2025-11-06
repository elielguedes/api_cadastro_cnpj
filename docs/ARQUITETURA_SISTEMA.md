# 🏗️ Arquitetura do Sistema - API Cadastro CNPJ

## 📊 Visão Geral da Arquitetura

```mermaid
graph TB
    %% === CAMADA DE APRESENTAÇÃO ===
    subgraph "🌐 PRESENTATION LAYER"
        A[👤 Cliente Web/Mobile] 
        B[📱 Postman/Insomnia]
        C[🤖 Sistemas Externos]
    end

    %% === PROXY E LOAD BALANCER ===
    subgraph "🔄 PROXY LAYER"
        D[🌐 Nginx Proxy<br/>Port 80]
    end

    %% === APLICAÇÃO ===
    subgraph "🚀 APPLICATION LAYER"
        E[⚡ FastAPI App<br/>Port 8000<br/>Uvicorn Server]
        
        subgraph "📡 API ENDPOINTS"
            E1[🏢 /empresas]
            E2[🏪 /estabelecimentos] 
            E3[👥 /socios]
            E4[🔐 /auth]
            E5[🏷️ /tags]
            E6[📚 /docs]
        end
    end

    %% === CAMADA DE NEGÓCIO ===
    subgraph "⚙️ SERVICE LAYER"
        F[🏢 EmpresaService]
        G[🏪 EstabelecimentoService]
        H[👥 SocioService]
        I[🔐 AuthService]
        J[🏷️ TagService]
    end

    %% === CAMADA DE DADOS ===
    subgraph "💾 DATA LAYER"
        K[🗄️ SQLAlchemy ORM]
        
        subgraph "📊 MODELS"
            K1[👤 Usuario]
            K2[🏢 Empresa]
            K3[🏪 Estabelecimento]
            K4[👥 Socio]
            K5[🏷️ Tag]
        end
    end

    %% === PERSISTÊNCIA ===
    subgraph "💽 PERSISTENCE LAYER"
        L[💻 SQLite<br/>Development]
        M[🐘 PostgreSQL<br/>Production]
    end

    %% === DADOS EXTERNOS ===
    subgraph "📂 EXTERNAL DATA"
        N[🇧🇷 dados.gov.br<br/>CSV Files]
        O[📄 repasse-s.csv]
    end

    %% === CONECTORES ===
    A --> D
    B --> D  
    C --> D
    D --> E
    E --> E1
    E --> E2
    E --> E3
    E --> E4
    E --> E5
    E --> E6
    
    E1 --> F
    E2 --> G
    E3 --> H
    E4 --> I
    E5 --> J
    
    F --> K
    G --> K
    H --> K
    I --> K
    J --> K
    
    K --> K1
    K --> K2
    K --> K3
    K --> K4
    K --> K5
    
    K --> L
    K --> M
    
    N --> O
    O --> F

    %% === ESTILOS ===
    classDef clientLayer fill:#e1f5fe
    classDef proxyLayer fill:#f3e5f5
    classDef appLayer fill:#e8f5e8
    classDef serviceLayer fill:#fff3e0
    classDef dataLayer fill:#fce4ec
    classDef persistLayer fill:#f1f8e9
    classDef externalLayer fill:#fff9c4

    class A,B,C clientLayer
    class D proxyLayer
    class E,E1,E2,E3,E4,E5,E6 appLayer
    class F,G,H,I,J serviceLayer
    class K,K1,K2,K3,K4,K5 dataLayer
    class L,M persistLayer
    class N,O externalLayer
```

## 🔄 Fluxo de Dados Detalhado

```mermaid
sequenceDiagram
    participant C as 👤 Cliente
    participant N as 🌐 Nginx
    participant F as 🚀 FastAPI
    participant S as ⚙️ Service
    participant O as 🗄️ ORM
    participant D as 💾 Database
    
    Note over C,D: 🔐 Fluxo de Autenticação
    C->>+N: POST /auth/login
    N->>+F: Encaminha requisição
    F->>+S: AuthService.login()
    S->>+O: query Usuario
    O->>+D: SELECT * FROM usuarios
    D-->>-O: user data
    O-->>-S: Usuario model
    S-->>S: Validate password
    S-->>S: Generate JWT
    S-->>-F: {access_token}
    F-->>-N: HTTP 200 + token
    N-->>-C: Bearer token
    
    Note over C,D: 📊 Fluxo de Consulta de Empresas
    C->>+N: GET /empresas?nome=petro&limit=10
    N->>+F: Encaminha + Bearer token
    F-->>F: Validate JWT
    F->>+S: EmpresaService.get_empresas()
    S->>+O: query Empresa with filters
    O->>+D: SELECT * FROM empresas WHERE nome LIKE '%petro%' LIMIT 10
    D-->>-O: empresa records
    O-->>-S: List[Empresa]
    S-->>-F: EmpresaRead models
    F-->>-N: HTTP 200 + JSON
    N-->>-C: Lista de empresas

    Note over C,D: ✏️ Fluxo de Criação (Admin)
    C->>+N: POST /empresas + Bearer token
    N->>+F: Encaminha requisição
    F-->>F: Validate JWT + Admin role
    F->>+S: EmpresaService.create()
    S-->>S: Validate CNPJ
    S->>+O: create Empresa
    O->>+D: INSERT INTO empresas
    D-->>-O: empresa_id
    O-->>-S: Empresa created
    S-->>-F: EmpresaRead
    F-->>-N: HTTP 201 + empresa
    N-->>-C: Empresa criada
```

## 🏗️ Padrões Arquiteturais Implementados

### 🔄 **Layered Architecture**
```
┌─────────────────────────────────┐
│    🌐 PRESENTATION LAYER        │  ← FastAPI Routers
│    (HTTP Endpoints)             │    REST API, Swagger UI
├─────────────────────────────────┤
│    ⚙️ SERVICE LAYER             │  ← Business Logic  
│    (Business Rules)             │    Validation, Processing
├─────────────────────────────────┤
│    💾 DATA LAYER                │  ← SQLAlchemy Models
│    (Domain Models)              │    ORM, Relationships
├─────────────────────────────────┤
│    💽 PERSISTENCE LAYER         │  ← Database Access
│    (Data Storage)               │    SQLite, PostgreSQL
└─────────────────────────────────┘
```

### 🎯 **Dependency Injection Pattern**
```python
# Injeção de Dependências
@router.get("/")
def get_empresas(
    db: Session = Depends(get_db),           # Database session
    current_user: User = Depends(get_current_user),  # Authentication
    skip: int = 0,
    limit: int = 10
):
    return EmpresaService.get_empresas(db, skip, limit)
```

### 🔒 **Middleware Pattern**
```python
# Chain of Responsibility para autenticação
Request → CORS → JWT Validation → Role Authorization → Endpoint
```

## 🗄️ Modelo de Dados Relacional

```mermaid
erDiagram
    %% === RELACIONAMENTOS ===
    USUARIO ||--o{ EMPRESA : "gerencia"
    EMPRESA ||--o{ ESTABELECIMENTO : "possui"
    ESTABELECIMENTO ||--o{ SOCIO : "possui"
    EMPRESA }o--o{ TAG : "categorizada_por"

    %% === TABELAS ===
    USUARIO {
        int id PK
        string username UK
        string hashed_password
        boolean is_admin
        datetime created_at
        datetime updated_at
    }

    EMPRESA {
        int id PK
        string nome
        string cnpj UK
        datetime created_at
        datetime updated_at
    }

    ESTABELECIMENTO {
        int id PK
        string nome
        int empresa_id FK
        string endereco
        datetime created_at
        datetime updated_at
    }

    SOCIO {
        int id PK
        string nome
        string cpf_cnpj
        string tipo
        int estabelecimento_id FK
        datetime created_at
        datetime updated_at
    }

    TAG {
        int id PK
        string name UK
        string description
        datetime created_at
    }

    EMPRESA_TAGS {
        int empresa_id FK
        int tag_id FK
    }
```

## 🌐 Deployment Architecture (AWS EC2)

```mermaid
graph TB
    %% === INTERNET ===
    subgraph "🌍 INTERNET"
        I[👥 Users Worldwide]
    end

    %% === AWS CLOUD ===
    subgraph "☁️ AWS CLOUD"
        subgraph "🔐 VPC & Security"
            SG[🛡️ Security Groups<br/>SSH: 22<br/>HTTP: 80<br/>HTTPS: 443<br/>Custom: 8000]
        end
        
        subgraph "🖥️ EC2 Instance (t3.micro)"
            subgraph "🐧 Ubuntu 22.04 LTS"
                subgraph "🌐 Nginx (Port 80)"
                    N[Reverse Proxy<br/>Load Balancer<br/>SSL Termination]
                end
                
                subgraph "🚀 FastAPI App (Port 8000)"
                    APP[Uvicorn Server<br/>Systemd Service<br/>Auto-restart]
                end
                
                subgraph "💾 Data Storage"
                    SQLITE[SQLite Database<br/>app.db<br/>Local Storage]
                end
                
                subgraph "📊 Monitoring"
                    LOGS[Journald Logs<br/>Nginx Logs<br/>Application Logs]
                end
            end
        end
    end

    %% === EXTERNAL DATA ===
    subgraph "📂 DATA SOURCES"
        GOV[🇧🇷 dados.gov.br<br/>CSV Files<br/>CNPJ Data]
    end

    %% === DESENVOLVIMENTO ===
    subgraph "💻 DEVELOPMENT"
        DEV[🖥️ Local Machine<br/>SQLite<br/>Port 8000]
    end

    %% === CONECTORES ===
    I --> SG
    SG --> N
    N --> APP
    APP --> SQLITE
    APP --> LOGS
    GOV --> APP
    DEV -.-> APP

    %% === ESTILOS ===
    classDef internet fill:#e3f2fd
    classDef aws fill:#fff3e0
    classDef security fill:#fce4ec
    classDef compute fill:#e8f5e8
    classDef data fill:#f3e5f5
    classDef external fill:#fff9c4
    classDef dev fill:#f1f8e9

    class I internet
    class SG security
    class N,APP,SQLITE,LOGS compute
    class GOV external
    class DEV dev
```

## 📈 Escalabilidade e Performance

### 🔄 **Horizontal Scaling Strategy**
```mermaid
graph LR
    subgraph "🌐 Load Balancer"
        LB[Nginx/ALB]
    end
    
    subgraph "🚀 Application Tier"
        APP1[FastAPI Instance 1]
        APP2[FastAPI Instance 2]
        APP3[FastAPI Instance N...]
    end
    
    subgraph "💾 Database Tier"
        DB1[PostgreSQL Primary]
        DB2[PostgreSQL Replica]
        CACHE[Redis Cache]
    end
    
    LB --> APP1
    LB --> APP2  
    LB --> APP3
    
    APP1 --> DB1
    APP2 --> DB1
    APP3 --> DB1
    
    DB1 --> DB2
    
    APP1 --> CACHE
    APP2 --> CACHE
    APP3 --> CACHE
```

### ⚡ **Performance Optimizations**
- **Connection Pooling**: SQLAlchemy pool configurado
- **Query Optimization**: Índices em campos frequentes
- **Pagination**: Limit/Offset para grandes datasets  
- **Lazy Loading**: Relacionamentos carregados sob demanda
- **Response Compression**: Gzip automático no Nginx
- **Static Asset Caching**: Headers de cache configurados

---

**Arquitetura projetada por:** Eliel Guedes  
**Data:** 18 de Outubro de 2025  
**Versão:** 1.0.0  
**Status:** ✅ Produção Ativa