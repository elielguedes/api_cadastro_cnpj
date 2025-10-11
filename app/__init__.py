"""
Pacote principal da aplicação FastAPI para gerenciamento de dados de empresas brasileiras.

Este módulo __init__.py marca o diretório 'app' como um pacote Python,
permitindo importações dos módulos internos como:
- main.py: Aplicação FastAPI principal
- models.py: Modelos SQLAlchemy para o banco de dados
- schemas.py: Schemas Pydantic para validação de dados
- database.py: Configuração e conexão com banco de dados
- auth.py: Sistema de autenticação JWT

Estrutura do projeto:
app/
├── __init__.py          # Este arquivo - marca como pacote Python
├── main.py              # Aplicação FastAPI e importação de dados
├── models/              # Modelos do banco de dados
├── routers/             # Endpoints da API organizados por recurso
├── services/            # Lógica de negócio e operações CRUD
└── scripts/             # Scripts auxiliares de importação
"""