# Demonstração Técnica Completa

Este documento consolida como executar e demonstrar o projeto em 4 frentes: Local, Público (ngrok), Docker e AWS (EC2 + Lambda), além de testes com Postman e banco de dados.

## 1) Executar Local (Windows)
- Pré-requisitos: Python 3.12/3.13, venv, requirements instalados
- Rodar:
  - .\.venv\Scripts\Activate.ps1
  - python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
- Verificar:
  - http://127.0.0.1:8000/ (health)
  - http://127.0.0.1:8000/docs (Swagger)

## 2) Link Público (ngrok)
- ngrok config add-authtoken <TOKEN>
- Iniciar com 1 clique:
  - ./deploy_now/start_public.ps1
- O script imprime a URL pública e abre o Swagger.

## 3) Docker
- Build:
  - docker build -t api-cnpj:latest .
- Run (SQLite):
  - docker run -p 8000:8000 --name api-cnpj api-cnpj:latest
- Run (PostgreSQL):
  - docker run -e DATABASE_URL="postgresql+psycopg2://USER:SENHA@HOST:5432/DB" -p 8000:8000 api-cnpj:latest

## 4) AWS
### EC2 (produção)
- Recomendado: Nginx como proxy reverso + systemd service
- Passos (resumo):
  - ssh -i fastapi_app_key ubuntu@18.118.167.28
  - sudo apt update && sudo apt install -y python3-venv nginx
  - (opcional) usar Dockerfile
  - Configurar serviço/PM2/systemd para uvicorn/gunicorn

### Lambda (serverless)
- Pré-requisito: AWS CLI configurado (us-east-2, Account 217466752219)
- Rode o script:
  - ./deploy_now/aws_deploy.ps1
- Funções criadas/atualizadas:
  - validate-cnpj-async
  - process-csv
  - generate-report

## 5) Testes com Postman
- Importar: docs/postman_collection.json
- Environment:
  - baseUrl = http://localhost:8000 (ou sua URL do ngrok)
- Endpoints principais:
  - GET /, GET /docs, GET /empresas, /estabelecimentos, /socios
  - GET /lambda/functions/status
  - POST /lambda/validate-cnpj { "cnpj": "12345678901234" }

## 6) Banco de Dados
- Fallback: SQLite em sqlite:///./app.db na raiz do projeto
- Produção: use DATABASE_URL
  - Ex.: postgresql+psycopg2://USER:SENHA@HOST:5432/DB
- DBeaver/Beekeeper: use driver PostgreSQL e a mesma URL (sem +psycopg2 se necessário)

## 7) Credenciais e Segurança
- JWT: /auth/login → usar Bearer Token
- CORS aberto no dev (ajustar em prod)
- Segredos via variáveis de ambiente (.env, secrets do host ou orquestrador)

## 8) Roteiro rápido de apresentação
1. start_public.ps1 → mostrar URL pública + Swagger
2. GET /health
3. CRUD empresas (listar, criar, editar, deletar)
4. Relacionamentos (estabelecimentos, sócios, tags)
5. Lambda status e validate-cnpj
6. Postman collection e troca de baseUrl (local ↔ ngrok)
7. Docker run e evidenciar healthcheck
8. Falar da EC2/Lambda (mostrando scripts e arquitetura)
