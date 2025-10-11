"""
Pacote de modelos SQLAlchemy para a aplicação de dados de empresas.

Este módulo organiza os modelos de banco de dados usando SQLAlchemy ORM:

- models.py: Contém as classes Empresa, Estabelecimento e Socio
  que definem a estrutura das tabelas no banco de dados SQLite

Os modelos seguem a estrutura dos dados do governo brasileiro (dados.gov.br)
para informações de CNPJ, estabelecimentos e sócios das empresas.

Relacionamentos:
- Uma Empresa pode ter múltiplos Estabelecimentos (1:N)
- Uma Empresa pode ter múltiplos Sócios (1:N)
- Estabelecimentos e Sócios estão vinculados às Empresas via foreign keys
"""