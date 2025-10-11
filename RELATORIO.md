# Relatório Técnico do Projeto: API Cadastro CNPJ

## 1. Justificativa da Escolha do Dataset
O conjunto de dados escolhido foi extraído do portal dados.gov.br, focando em informações públicas de empresas brasileiras (CNPJ). A escolha se deu pela relevância do tema para aplicações reais de gestão, transparência e análise econômica, além da ampla disponibilidade e atualização periódica dos dados.

## 2. Análise e Modelagem de Dados
Foi realizada uma análise exploratória dos dados originais em CSV, identificando as principais entidades: Empresa, Estabelecimento e Sócio. A modelagem seguiu boas práticas de normalização, garantindo integridade referencial e flexibilidade para consultas e expansões futuras.

- **Empresa**: representa o cadastro básico da pessoa jurídica, com campos como id, nome e cnpj.
- **Estabelecimento**: vinculado à empresa, representa filiais ou unidades operacionais.
- **Sócio**: vinculado ao estabelecimento, representa pessoas físicas ou jurídicas associadas.

O diagrama ER foi elaborado em português, com setas e nomes claros, facilitando o entendimento por qualquer público.

## 3. Estrutura e Organização da API
A API foi construída com FastAPI, SQLAlchemy e SQLite, separando o código em camadas:
- **Modelos (models.py)**: definição das entidades e relacionamentos ORM.
- **Schemas (schemas.py)**: validação e serialização dos dados via Pydantic.
- **Rotas (routers/)**: endpoints RESTful organizados por entidade.
- **Serviços (services/)**: lógica de negócio e integração com o banco.
- **Autenticação (auth.py)**: implementação de JWT, perfis de usuário e proteção de rotas.

A documentação automática foi gerada via Swagger/OpenAPI, permitindo fácil exploração e testes dos endpoints.

## 4. Autenticação e Segurança
A autenticação JWT foi implementada seguindo padrões do mercado, com rotas protegidas e perfis diferenciados (admin/leitor). As senhas são armazenadas com hash seguro (passlib), e o fluxo de login, cadastro e autorização foi testado manualmente e via Postman.

## 5. Testes e Validação
- **Coleção Postman**: criada para testar todos os endpoints, incluindo autenticação, CRUD e filtros.
- **Testes manuais**: realizados com evidências (prints e logs) para garantir o funcionamento da API.
- **Validação de dados**: garantida via schemas Pydantic e constraints do banco.

## 6. Versionamento e Deploy
O projeto foi versionado no GitHub, seguindo o padrão Git Flow (main, develop, feature/*). O arquivo `.gitignore` foi configurado para evitar o envio de arquivos do ambiente virtual e dados sensíveis.

O deploy pode ser realizado em ambiente local ou na AWS (EC2, Lambda), conforme as próximas etapas do curso. O README inclui instruções detalhadas para execução local.

## 7. Diagrama ER
O diagrama ER está disponível no README em formato Mermaid e pode ser exportado como imagem. Ele representa claramente os relacionamentos entre Empresa, Estabelecimento e Sócio.

## 8. Considerações Finais
O projeto foi desenvolvido seguindo boas práticas de engenharia de software, com foco em clareza, segurança, escalabilidade e documentação. A estrutura modular facilita manutenção e evolução futura, e o uso de dados reais garante aplicabilidade prática.

Qualquer dúvida ou sugestão de melhoria, estou à disposição.

---
Eliel Guedes
Desenvolvedor Python Sênior
