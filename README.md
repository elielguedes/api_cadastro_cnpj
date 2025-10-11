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
    EMPRESA ||--o{ ESTABELECIMENTO : possui
    ESTABELECIMENTO ||--o{ SOCIO : possui
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
```

## Origem dos Dados
- Fonte: [dados.gov.br](https://dados.gov.br)
- Formato: CSV
- Periodicidade: conforme atualização oficial

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
uvicorn app.main:app --reload
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
```
