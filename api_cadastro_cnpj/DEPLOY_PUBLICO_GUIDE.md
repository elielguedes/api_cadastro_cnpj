# 🌐 Guia Rápido: Tornar Link Público

**Projeto**: Sistema FastAPI  
**Objetivo**: Link público para apresentação  
**Status**: ✅ Aplicação funcionando localmente

---

## ⚡ **OPÇÃO 1: ngrok (Mais Rápido - 2 minutos)**

### 📥 **1. Baixar ngrok**
- Acesse: https://ngrok.com/download
- Baixe para Windows
- Extraia para uma pasta (ex: C:\ngrok)

### 🚀 **2. Usar ngrok**
```powershell
# Terminal 1: Manter aplicação rodando
cd C:\Users\eliel\.vscode\framework_udf
$env:DATABASE_URL = ""
python -m uvicorn app.main:app --reload --port 8000

# Terminal 2: Criar túnel público
cd C:\ngrok  # (onde extraiu o ngrok)
.\ngrok http 8000

# ✅ Resultado: Link público como https://abc123.ngrok.io
```

### 🔗 **3. Link Público Gerado**
```
Forwarding  https://abc123.ngrok.io -> http://localhost:8000

✅ Documentação: https://abc123.ngrok.io/docs
✅ API: https://abc123.ngrok.io/empresas/
✅ Lambda: https://abc123.ngrok.io/lambda/functions/status
```

---

## 🚂 **OPÇÃO 2: Railway (Deploy Permanente)**

### 📥 **1. Instalar Railway CLI**
```powershell
npm install -g @railway/cli
# OU baixar em: https://railway.app/cli
```

### 🚀 **2. Deploy**
```powershell
cd C:\Users\eliel\.vscode\framework_udf
railway login
railway init
railway deploy

# ✅ Resultado: Link permanente como https://seu-projeto.railway.app
```

---

## ☁️ **OPÇÃO 3: Render (Gratuito)**

### 📥 **1. Criar conta**
- Acesse: https://render.com
- Conecte GitHub

### 🚀 **2. Deploy direto do GitHub**
1. Push para GitHub
2. New Web Service no Render
3. Conectar repositório
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

---

## 🎯 **RECOMENDAÇÃO RÁPIDA**

### Para apresentação HOJE:
**USE ngrok** (2 minutos):

```powershell
# 1. Baixar ngrok: https://ngrok.com/download
# 2. Extrair e abrir 2 terminais:

# Terminal 1:
cd C:\Users\eliel\.vscode\framework_udf
python -m uvicorn app.main:app --port 8000

# Terminal 2:
.\ngrok http 8000

# 3. Copiar o link https://xyz.ngrok.io
# 4. Compartilhar: https://xyz.ngrok.io/docs
```

---

## 🔧 **Scripts Prontos**

### **start_app.ps1**
```powershell
# Salve como start_app.ps1
cd C:\Users\eliel\.vscode\framework_udf
$env:DATABASE_URL = ""
python -m uvicorn app.main:app --reload --port 8000
```

### **create_tunnel.ps1** 
```powershell
# Salve como create_tunnel.ps1 (após baixar ngrok)
cd C:\ngrok
.\ngrok http 8000
```

---

## 📱 **Links para Compartilhar**

Depois do ngrok/deploy, você terá:

```
✅ Aplicação: https://seu-link.ngrok.io
✅ Documentação: https://seu-link.ngrok.io/docs  
✅ API Empresas: https://seu-link.ngrok.io/empresas/
✅ Lambda Status: https://seu-link.ngrok.io/lambda/functions/status
✅ Teste Lambda: https://seu-link.ngrok.io/lambda/test-integration
```

---

## ⭐ **Para Apresentação**

### **Roteiro sugerido:**
1. **Mostrar documentação**: `https://seu-link.ngrok.io/docs`
2. **Fazer login**: POST `/auth/login`
3. **Testar CRUD**: GET `/empresas/`
4. **Demonstrar Lambda**: POST `/lambda/validate-cnpj-async`
5. **Mostrar status**: GET `/lambda/functions/status`

### **Dados de teste:**
```json
// Login
{"username": "admin", "password": "admin123"}

// CNPJ para testar
{"cnpj": "11.222.333/0001-81"}

// Nova empresa  
{
  "cnpj": "12.345.678/0001-90",
  "razao_social": "Demo Corp LTDA", 
  "nome_fantasia": "Demo"
}
```

---

**🎯 Escolha uma opção e em poucos minutos terá o link público funcionando!**