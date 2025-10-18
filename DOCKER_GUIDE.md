# 🐳 Docker Setup & Usage Guide

## ⚠️ Problema Atual: Docker Desktop não está rodando

### 🔧 Para iniciar Docker Desktop:

1. **Abrir Docker Desktop**
   - Procure "Docker Desktop" no menu Iniciar
   - Ou execute: `C:\Program Files\Docker\Docker\Docker Desktop.exe`

2. **Aguardar inicialização**
   - O ícone na system tray deve ficar verde
   - Pode levar alguns minutos na primeira vez

3. **Verificar se está funcionando**
   ```powershell
   docker --version
   docker-compose --version
   ```

### 🚀 Usando a API FastAPI:

#### Opção 1: PowerShell Script (Recomendado)
```powershell
# Iniciar aplicação
.\docker-manage.ps1 up

# Parar aplicação  
.\docker-manage.ps1 down

# Rebuild completo
.\docker-manage.ps1 rebuild

# Ver logs
.\docker-manage.ps1 logs

# Status dos containers
.\docker-manage.ps1 status
```

#### Opção 2: Comandos manuais
```powershell
# PowerShell usa ; ao invés de &&
docker-compose down -v; docker-compose up --build

# Ou comandos separados
docker-compose down -v
docker-compose up --build
```

#### Opção 3: Sem Docker (Local)
```powershell
# Ativar ambiente virtual
.\.venv\Scripts\Activate.ps1

# Instalar dependências se necessário
pip install -r requirements.txt

# Iniciar aplicação
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 📍 URLs após iniciar:
- **API Docs**: http://localhost:8000/docs
- **PostgreSQL**: localhost:5432 (usuário: postgres, senha: postgres)

### 🔍 Troubleshooting:

1. **"The system cannot find the file specified"**
   → Docker Desktop não está rodando

2. **"InvalidEndOfLine" com &&**
   → Use `;` no PowerShell ou comandos separados

3. **Porta 8000 em uso**
   ```powershell
   netstat -ano | findstr :8000
   taskkill /PID <PID> /F
   ```

4. **PostgreSQL não conecta**
   → Aguarde container "fastapi_db" estar "healthy"