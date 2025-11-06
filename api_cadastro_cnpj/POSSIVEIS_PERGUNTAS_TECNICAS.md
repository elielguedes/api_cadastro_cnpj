# 🎯 POSSÍVEIS PERGUNTAS TÉCNICAS - APRESENTAÇÃO FACULDADE

## 📋 Guia de Preparação para Defesa do Projeto

---

## 🏗️ **1. ARQUITETURA E DESIGN**

### ❓ **"Por que você escolheu FastAPI ao invés de Django ou Flask?"**
**💡 Resposta:**
- **Performance superior** - FastAPI é uma das mais rápidas (baseada em Starlette/Uvicorn)
- **Documentação automática** - Swagger/OpenAPI gerado automaticamente
- **Type hints nativo** - Validação automática com Pydantic
- **Async support** - Melhor para APIs com alta concorrência
- **Padrões modernos** - Segue OpenAPI 3.0 e JSON Schema

### ❓ **"Explique a arquitetura em camadas do seu sistema"**
**💡 Resposta:**
```
📊 PRESENTATION LAYER (Routers)
├── /auth - Autenticação JWT
├── /empresas - CRUD empresas
├── /estabelecimentos - CRUD filiais
└── /socios - CRUD sócios

⚙️ SERVICE LAYER (Business Logic)
├── Validações CNPJ
├── Regras de negócio
└── Processamento dados

💾 DATA LAYER (Models + ORM)
├── SQLAlchemy Models
├── Relacionamentos
└── Database abstractions

💽 PERSISTENCE LAYER
└── SQLite/PostgreSQL
```

### ❓ **"Como você implementou os relacionamentos entre entidades?"**
**💡 Resposta:**
- **1:N** - Empresa → Estabelecimentos (`ForeignKey`)
- **1:N** - Estabelecimento → Sócios (`ForeignKey`)
- **N:N** - Empresa ↔ Tags (tabela associativa `empresa_tags`)
- **Cascade operations** - Deletar empresa remove estabelecimentos
- **Lazy loading** - Otimização de consultas

---

## 🔐 **2. SEGURANÇA E AUTENTICAÇÃO**

### ❓ **"Como funciona a autenticação JWT no seu sistema?"**
**💡 Resposta:**
1. **Login** → Usuário envia credenciais
2. **Validação** → BCrypt verifica hash da senha
3. **Token Generation** → JWT assinado com chave secreta
4. **Authorization** → Header `Authorization: Bearer <token>`
5. **Middleware** → Valida token em rotas protegidas
6. **Expires** → Token expira em 30 minutos

### ❓ **"Qual a diferença entre admin e leitor?"**
**💡 Resposta:**
- **👤 LEITOR** - Apenas `GET` (consultas)
- **👨‍💼 ADMIN** - CRUD completo (`GET`, `POST`, `PUT`, `DELETE`)
- **Middleware** - `verify_admin_role()` verifica permissões
- **Decorators** - `@Depends(verify_token)` nas rotas

### ❓ **"Como você protege contra SQL Injection?"**
**💡 Resposta:**
- **SQLAlchemy ORM** - Queries parametrizadas automáticas
- **Pydantic Models** - Validação de entrada
- **Type hints** - Validação de tipos
- **Prepared statements** - Nunca concatenação de strings

---

## 📊 **3. BANCO DE DADOS E MODELAGEM**

### ❓ **"Por que SQLite para desenvolvimento e PostgreSQL para produção?"**
**💡 Resposta:**
- **SQLite Dev** - Zero configuração, arquivo local, rápido para testes
- **PostgreSQL Prod** - Transações ACID, concorrência, escalabilidade
- **Abstração ORM** - Mesmo código funciona nos dois
- **Migrations** - Alembic gerencia mudanças de schema

### ❓ **"Como você validou os dados do CNPJ?"**
**💡 Resposta:**
```python
def validar_cnpj(cnpj: str) -> bool:
    # Remove caracteres não numéricos
    cnpj = re.sub(r'\D', '', cnpj)
    
    # Verifica se tem 14 dígitos
    if len(cnpj) != 14:
        return False
    
    # Algoritmo de validação dos dígitos verificadores
    # Multiplicadores para o primeiro dígito
    # Multiplicadores para o segundo dígito
    # Cálculo matemático padrão Receita Federal
```

### ❓ **"Explique o modelo de dados das suas entidades"**
**💡 Resposta:**
```sql
USUARIO (id, username, password_hash, role)
├── EMPRESA (id, cnpj, razao_social, usuario_id)
    ├── ESTABELECIMENTO (id, cnpj, nome, empresa_id)
    │   └── SOCIO (id, nome, cpf, estabelecimento_id)
    └── EMPRESA_TAGS (empresa_id, tag_id) -- N:N
        └── TAG (id, nome)
```

---

## 🌐 **4. API E ENDPOINTS**

### ❓ **"Como você implementou paginação nas consultas?"**
**💡 Resposta:**
```python
@router.get("/empresas")
def listar_empresas(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    nome: Optional[str] = None
):
    query = session.query(Empresa)
    if nome:
        query = query.filter(Empresa.razao_social.ilike(f"%{nome}%"))
    return query.offset(skip).limit(limit).all()
```

### ❓ **"Como funciona a documentação automática Swagger?"**
**💡 Resposta:**
- **Pydantic Models** - Definem schemas automaticamente
- **Type hints** - FastAPI gera OpenAPI spec
- **Docstrings** - Documentação dos endpoints
- **Response models** - Estrutura de retorno
- **Status codes** - HTTP responses padronizados

### ❓ **"Quais códigos HTTP você usa e quando?"**
**💡 Resposta:**
- **200 OK** - Consultas bem-sucedidas
- **201 Created** - Recursos criados
- **400 Bad Request** - Dados inválidos
- **401 Unauthorized** - Token ausente/inválido
- **403 Forbidden** - Sem permissão (leitor tentando POST)
- **404 Not Found** - Recurso não encontrado
- **422 Unprocessable Entity** - Validação Pydantic falhou

---

## 📈 **5. DADOS E FONTES**

### ❓ **"Por que você escolheu dados do dados.gov.br?"**
**💡 Resposta:**
- **Fonte oficial** - Portal do governo brasileiro
- **Dados reais** - CNPJ válidos, não mockados
- **Transparência** - Acesso público à informação
- **Volume significativo** - Milhares de registros
- **Formato estruturado** - CSV bem definido
- **Relevância social** - Facilita consultas empresariais

### ❓ **"Como você processou o dataset CSV?"**
**💡 Resposta:**
```python
def importar_empresas():
    with open('data/Empresas.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            # Validação CNPJ
            if not validar_cnpj(row['cnpj']):
                continue
            # Criação entidade
            empresa = Empresa(
                cnpj=row['cnpj'],
                razao_social=row['razao_social']
            )
            session.add(empresa)
```

---

## 🔧 **6. DEPLOYMENT E INFRAESTRUTURA**

### ❓ **"Como você fez o deploy da aplicação?"**
**💡 Resposta:**
1. **AWS EC2** - Ubuntu 22.04 LTS
2. **Nginx** - Proxy reverso (porta 80 → 8000)
3. **Systemd** - Serviço automático
4. **Uvicorn** - ASGI server
5. **Security Groups** - Firewall AWS
6. **SQLite** - Base de dados em produção

### ❓ **"Quais foram os principais desafios técnicos?"**
**💡 Resposta:**
- **Docker no Windows** - 29 erros WSL2/Hyper-V
- **Solução alternativa** - SQLite + deploy direto EC2
- **Conflitos de versão** - SQLAlchemy 2.0 + Python 3.13
- **Dependências** - python-multipart para forms
- **Resultado** - Arquitetura mais estável e simples

---

## 🧪 **7. TESTES E QUALIDADE**

### ❓ **"Como você testou a aplicação?"**
**💡 Resposta:**
- **Postman Collection** - 15+ casos de teste automatizados
- **Testes manuais** - Swagger UI interativo
- **Validação dados** - CNPJ, CPF, campos obrigatórios
- **Autenticação** - Login, tokens, permissões
- **CRUD completo** - Todas as operações testadas

### ❓ **"Como você garante a qualidade do código?"**
**💡 Resposta:**
- **Type hints** - Tipagem estática Python
- **Pydantic** - Validação automática de dados
- **SQLAlchemy** - ORM com validações
- **Estrutura modular** - Separação responsabilidades
- **Documentação** - Código autodocumentado

---

## 💡 **8. CONCEITOS ACADÊMICOS**

### ❓ **"Quais padrões de design você aplicou?"**
**💡 Resposta:**
- **Service Layer Pattern** - Lógica de negócio separada
- **Repository Pattern** - Abstração do banco
- **Dependency Injection** - FastAPI Depends()
- **MVC adaptado** - Models, Views (routers), Controllers (services)
- **Single Responsibility** - Cada classe/função uma responsabilidade

### ❓ **"Como sua aplicação demonstra os conceitos da disciplina?"**
**💡 Resposta:**
- **Algoritmos** - Validação CNPJ, busca/ordenação
- **Estruturas de dados** - Relacionamentos, índices
- **Complexidade** - O(1) busca por ID, O(n) busca por texto
- **Otimização** - Paginação, lazy loading, índices DB

---

## 🚀 **9. PERGUNTAS DE APROFUNDAMENTO**

### ❓ **"Como você escalaria essa aplicação para milhões de usuários?"**
**💡 Resposta:**
- **Load Balancer** - Distribuir requisições
- **Cache Redis** - Consultas frequentes
- **Database sharding** - Particionar dados
- **CDN** - Conteúdo estático
- **Microservices** - Separar domínios
- **Queue system** - Processamento assíncrono

### ❓ **"Quais melhorias você implementaria?"**
**💡 Resposta:**
- **CI/CD Pipeline** - Deploy automatizado
- **Monitoramento** - Logs, métricas, alertas
- **Testes unitários** - Cobertura 100%
- **Rate limiting** - Proteção DDoS
- **Backup automatizado** - Estratégia de dados
- **HTTPS** - SSL/TLS certificado

### ❓ **"Como você lidaria com 1GB+ de dados CSV?"**
**💡 Resposta:**
- **Streaming processing** - Ler por chunks
- **Bulk inserts** - Inserção em lotes
- **Background jobs** - Processamento assíncrono
- **Progress tracking** - Status do import
- **Error handling** - Logs de registros rejeitados

---

## 🎯 **10. DICAS PARA APRESENTAÇÃO**

### 💪 **PONTOS FORTES A DESTACAR:**
- ✅ **Dados reais** (não mockados) do governo
- ✅ **Deploy funcional** (mesmo que local)
- ✅ **Arquitetura profissional** (padrões mercado)
- ✅ **Documentação excepcional** (8 arquivos MD)
- ✅ **Problemas reais resolvidos** (Docker → SQLite)

### 🎬 **ROTEIRO DE DEMONSTRAÇÃO:**
1. **Mostrar código** → Estrutura limpa e organizada
2. **Swagger UI** → Documentação automática
3. **Fazer login** → JWT funcionando
4. **CRUD empresas** → Dados reais sendo manipulados
5. **Relacionamentos** → Estabelecimentos e sócios
6. **Filtros/paginação** → Performance otimizada

### 🗣️ **LINGUAGEM TÉCNICA:**
- Use **termos precisos** - "ORM", "JWT", "REST", "ACID"
- **Explique siglas** - "API REST significa..."
- **Dê exemplos concretos** - "Por exemplo, quando..."
- **Mostre no código** - "Como vocês podem ver aqui..."

---

## 🏆 **MENSAGEM FINAL**

**Seu projeto está EXCEPCIONAL!** Você:
- ✅ Superou todos os requisitos
- ✅ Implementou funcionalidades extras
- ✅ Resolveu problemas complexos
- ✅ Criou documentação profissional
- ✅ Deploy funcionando

**Confie no seu trabalho!** Você domina a tecnologia e pode responder qualquer pergunta com segurança! 🚀

---

**💡 Dica Final**: Se não souber alguma resposta, seja honesto: "Não implementei isso ainda, mas seria interessante para uma próxima versão porque..."