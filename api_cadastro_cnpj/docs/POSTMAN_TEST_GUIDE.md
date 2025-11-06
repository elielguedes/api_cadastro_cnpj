# Testes com Postman - API de Empresas Brasileiras

Este guia mostra como testar sua API local (Uvicorn) e pública (ngrok) usando o Postman, com exemplos prontos e uma coleção exportada.

## Pré-requisitos
- Postman instalado
- API rodando localmente em http://localhost:8000 (ou via ngrok)
- Se estiver usando ngrok, verifique a URL pública em http://127.0.0.1:4040/api/tunnels

## Variáveis de Ambiente no Postman
Crie um Environment no Postman com as seguintes variáveis:
- baseUrl: http://localhost:8000 (ou sua URL ngrok, exemplo: https://topographical-zula-unconsentaneous.ngrok-free.dev)
- token: (opcional) JWT caso use autenticação em /auth

## Importar a Coleção
- Arquivo: docs/postman_collection.json
- No Postman: Import > File > selecione postman_collection.json

## Endpoints principais

1) Health check
- GET {{baseUrl}}/
- Esperado: 200 OK, JSON com status healthy

2) Docs (Swagger)
- GET {{baseUrl}}/docs
- Esperado: 200 OK (página Swagger)

3) Empresas
- GET {{baseUrl}}/empresas
- Filtros (query): nome, cnpj (verifique conforme seu router)

4) Estabelecimentos
- GET {{baseUrl}}/estabelecimentos

5) Sócios
- GET {{baseUrl}}/socios

6) Lambda (Integração)
- GET {{baseUrl}}/lambda/functions/status
- POST {{baseUrl}}/lambda/validate-cnpj
  - Body (JSON): { "cnpj": "12345678901234" }

7) Auth (se aplicável)
- POST {{baseUrl}}/auth/login
  - Body (JSON): { "username": "...", "password": "..." }
  - Copie o token para a variável `token`
- Headers em requests protegidos: Authorization: Bearer {{token}}

## Como trocar entre Local e ngrok
- No Postman, mude a variável baseUrl do Environment:
  - Local: http://localhost:8000
  - ngrok: cole a URL pública (ex: https://...ngrok-free.dev)

## Depuração Rápida
- Se 502/504 com ngrok, verifique se o Uvicorn está rodando
- Se CORS, já está liberado em app/main.py (allow_origins:*). Ajuste em produção
- Se 401, gere novo token em /auth/login

## Dica
- Deixe o Postman Console aberto (View > Show Postman Console) para ver detalhes das requisições
