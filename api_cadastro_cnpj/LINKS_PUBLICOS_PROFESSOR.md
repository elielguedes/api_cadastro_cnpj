# 🌐 GUIA DE ACESSO PÚBLICO - API CADASTRO CNPJ

## 🎯 Links Públicos Funcionais

### 🔗 **OPÇÕES DE ACESSO PARA O PROFESSOR**

---

## ⚡ **OPÇÃO 1: Ngrok (Recomendado)**

### 📥 **1. Baixar Ngrok**
- **Site**: [https://ngrok.com/download](https://ngrok.com/download)
- **Download**: `ngrok-v3-stable-windows-amd64.zip`
- **Descompactar** em `C:\ngrok\`

### 🚀 **2. Comandos para Executar**
```powershell
# Terminal 1: Iniciar API
python start_sqlite.py

# Terminal 2: Criar túnel ngrok
C:\ngrok\ngrok.exe http 8000
```

### 🌍 **3. Link Público Gerado**
```
https://abc123def456.ngrok-free.app
```
**📚 Documentação**: `https://abc123def456.ngrok-free.app/docs`

---

## 🌐 **OPÇÃO 2: Localtunnel (Alternativa)**

### 📥 **1. Instalar Node.js**
- **Site**: [https://nodejs.org](https://nodejs.org)
- **Versão**: LTS (Long Term Support)

### 🚀 **2. Comandos para Executar**
```powershell
# Instalar localtunnel
npm install -g localtunnel

# Terminal 1: Iniciar API
python start_sqlite.py

# Terminal 2: Criar túnel
lt --port 8000 --subdomain eliel-fastapi
```

### 🌍 **3. Link Público Gerado**
```
https://eliel-fastapi.loca.lt
```

---

## 🏠 **OPÇÃO 3: Rede Local (Mais Simples)**

### 🔧 **1. Configurar Firewall Windows**
```powershell
# Permitir porta 8000 no Windows Firewall
netsh advfirewall firewall add rule name="FastAPI" dir=in action=allow protocol=TCP localport=8000
```

### 🚀 **2. Iniciar Servidor Público**
```powershell
python start_public.py
```

### 🌍 **3. Link da Rede Local**
```
http://192.168.3.21:8000/docs
```
**⚠️ Nota**: Funciona apenas na mesma rede Wi-Fi

---

## 🌟 **OPÇÃO 4: Deploy Render (Gratuito 24/7)**

### 📂 **1. Criar Conta**
- **Site**: [https://render.com](https://render.com)
- **GitHub**: Conectar repositório

### ⚙️ **2. Configuração Deploy**
```yaml
# render.yaml
services:
  - type: web
    name: api-cnpj-eliel
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: DATABASE_URL
        value: sqlite:///./app.db
```

### 🌍 **3. Link Público Permanente**
```
https://api-cnpj-eliel.onrender.com/docs
```

---

## 🚀 **OPÇÃO 5: Deploy Vercel (Serverless)**

### 📂 **1. Criar Conta**
- **Site**: [https://vercel.com](https://vercel.com)
- **GitHub**: Import repository

### ⚙️ **2. Configuração**
```json
// vercel.json
{
  "builds": [
    {
      "src": "app/main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app/main.py"
    }
  ]
}
```

### 🌍 **3. Link Público Automático**
```
https://relatorio-eliel-guedes.vercel.app/docs
```

---

## 💡 **RECOMENDAÇÃO PARA APRESENTAÇÃO**

### 🎯 **Melhor Estratégia**
1. **✅ Use NGROK** (mais confiável)
2. **⏰ 15min antes** da apresentação, execute:
   ```powershell
   python start_sqlite.py
   C:\ngrok\ngrok.exe http 8000
   ```
3. **📋 Copie o link** gerado pelo ngrok
4. **📱 Envie para professor**: 
   - WhatsApp/Email/Teams
   - Exemplo: `https://abc123def456.ngrok-free.app/docs`

### 📝 **Template de Mensagem**
```
Professor,

Segue o link da minha API funcionando ao vivo:
🌐 https://abc123def456.ngrok-free.app/docs

Credenciais para teste:
👨‍💼 Admin: admin / admin123
👤 Leitor: leitor / leitor123

Funcionalidades:
✅ Autenticação JWT
✅ CRUD completo (Empresas, Estabelecimentos, Sócios)
✅ Dados reais do dados.gov.br
✅ Documentação interativa Swagger

Att,
Eliel Guedes
```

---

## ⚠️ **TROUBLESHOOTING**

### 🚫 **Se Ngrok não funcionar**
1. **Verificar antivírus** - Pode bloquear
2. **Usar Localtunnel** - Alternativa mais leve
3. **Deploy Render** - Solução permanente

### 🔧 **Se Windows Firewall bloquear**
```powershell
# Desabilitar temporariamente (apenas para apresentação)
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False

# Reativar depois
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True
```

### 📡 **Se rede da faculdade bloquear**
- **Use hotspot** do celular
- **Deploy na nuvem** (Render/Vercel)
- **Apresentação local** no seu notebook

---

## 🏆 **STATUS FINAL**

### ✅ **Links Preparados**
- 🏠 **Local**: http://127.0.0.1:8000/docs
- 🌐 **Rede**: http://192.168.3.21:8000/docs  
- 🚀 **Ngrok**: `Gerar na hora da apresentação`
- ☁️ **Cloud**: `Deploy quando necessário`

### 📱 **Pronto para Enviar**
- **API 100% funcional**
- **Múltiplas opções de acesso**
- **Documentação completa**
- **Credenciais de teste**

**🎯 Escolha a opção que preferir e mande o link para o professor! 🚀**