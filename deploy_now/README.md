# Deploy Now (Demonstração Rápida)

Scripts e passos para subir a API e expor publicamente via ngrok em menos de 1 minuto.

## Pré-requisitos
- Windows + PowerShell
- Python 3.12/3.13 com venv ativo (\_.venv já existe)
- Dependências instaladas: `pip install -r requirements.txt`
- ngrok autenticado: `ngrok config add-authtoken <TOKEN>`

## Uso (1 clique)

1. Execute:
   
   PowerShell
   ./deploy_now/start_public.ps1

2. O script irá:
   - Ativar o venv
   - Iniciar Uvicorn (app.main:app) em 0.0.0.0:8000
   - Iniciar ngrok apontando para 8000
   - Buscar e imprimir a URL pública
   - (Opcional) Abrir o Swagger automaticamente

## Verificação
- Local: http://localhost:8000/docs
- Público (exemplo): https://<seu-subdominio>.ngrok-free.dev/docs

## Problemas comuns
- Porta 8000 ocupada: feche outros Uvicorn/servers
- Ngrok sem token: execute `ngrok config add-authtoken <TOKEN>`
- Ambiente não ativado: rode `.\.venv\Scripts\Activate.ps1`

## Alternativas
- Dev Tunnels (VS Code) ou Cloudflare Tunnel
- Deploy em EC2/Lambda conforme docs na raiz (AWS_*.md)
