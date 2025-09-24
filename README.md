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
