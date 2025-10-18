# api_cadastro_cnpj

## Descrição
API RESTful para cadastro, consulta e gestão de empresas brasileiras (CNPJ), utilizando dados públicos do portal dados.gov.br. Desenvolvida com FastAPI, SQLAlchemy e SQLite.

## Funcionalidades
- CRUD completo para empresas, estabelecimentos e sócios
- Filtros, ordenação e paginação
- Autenticação JWT (admin/leitor)
- Documentação automática (Swagger)
- Testes automatizados (Postman)

## Como executar
1. Clone o repositório
2. Crie e ative o ambiente virtual (Python 3.12)
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Inicie o servidor:
   ```bash
   uvicorn app.main:app --reload
   ```
5. Acesse a documentação em [http://localhost:8000/docs](http://localhost:8000/docs)

## Estrutura do Projeto
- `app/models/models.py`: Modelos ORM
- `app/schemas.py`: Schemas Pydantic
- `app/routers/`: Rotas da API
- `app/services/`: Lógica de negócio
- `app/auth.py`: Autenticação JWT
- `data/repasse-s.csv`: Dados públicos

## Diagrama ER

```mermaid
erDiagram
    USUARIO ||--o{ EMPRESA : criou
    EMPRESA ||--o{ ESTABELECIMENTO : possui
    ESTABELECIMENTO ||--o{ SOCIO : possui
    EMPRESA }o--o{ TAG : rotulada_com

    USUARIO {
        int id
        string username
        bool is_admin
    }

    EMPRESA {
        int id
        string nome
        string cnpj
    }

    ESTABELECIMENTO {
        int id
        string nome
        int empresa_id
    }

    SOCIO {
        int id
        string nome
        int estabelecimento_id
    }

    TAG {
        int id
        string name
    }
```

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

Uso (PowerShell, no venv):

```powershell
.
# ativar venv
.\.venv\Scripts\Activate.ps1
# importar (simples)
venv\Scripts\python.exe scripts\import_repasse.py
# importar com relatório (gera data/import_rejeitados.csv)
venv\Scripts\python.exe scripts\import_repasse_with_report.py
# exportar empresas
venv\Scripts\python.exe scripts\export_empresas.py
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

## Próximos passos recomendados
- Validar e normalizar CNPJ antes de inserção
- Criar testes adicionais e coleção Postman
- Adicionar CI (GitHub Actions) para rodar lint e testes
- Preparar Dockerfile e scripts para deploy na AWS (EC2/ECS/Lambda)
- Completar cobertura de testes para as rotas de `tags` (criar, associar/desassociar, garantir que `EmpresaRead` retorna tags)
- Consolidar migrations (autogenerate) e adicionar um script `make migrate` ou task no `Makefile`/scripts para padronizar fluxo de migrations
- Atualizar handlers de startup para usar `lifespan` (resolver warnings depreciação do FastAPI)

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
