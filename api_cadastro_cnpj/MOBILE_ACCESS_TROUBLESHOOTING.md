# 📱 Troubleshooting: Acesso pelo Celular

**Problema**: Não conseguir acessar https://7fbvhccr-8000.brs.devtunnels.ms/ pelo celular  
**Status**: ✅ Servidor configurado corretamente para acesso externo  
**Data**: Outubro 2025

---

## ✅ **Verificações Realizadas**

### 🔧 **Servidor FastAPI**
- ✅ **Host**: 0.0.0.0 (aceita conexões externas)
- ✅ **Porta**: 8000  
- ✅ **Status**: Online e respondendo
- ✅ **Logs**: Mostra acessos externos funcionando (IP 187.63.105.235)

### 🌐 **DevTunnel VS Code**
- ✅ **URL**: https://7fbvhccr-8000.brs.devtunnels.ms/
- ✅ **Tipo**: VS Code DevTunnel (público)
- ✅ **Região**: Brasil (.brs)

---

## 🔍 **Diagnóstico do Problema**

### **Possíveis Causas:**

#### 1️⃣ **DevTunnel Não Público**
O DevTunnel pode estar configurado como privado.

**Solução:**
```bash
# No VS Code, verifique:
1. Terminal → Ports
2. Clique com botão direito na porta 8000
3. Port Visibility → Public
4. Novo link será gerado
```

#### 2️⃣ **Firewall/Antivírus**
Bloqueio de conexões externas.

**Solução:**
```powershell
# Verificar Windows Defender
1. Windows Security → Firewall & network protection
2. Allow an app through firewall
3. Adicionar Python se necessário
```

#### 3️⃣ **Rede do Celular**
Algumas redes corporativas/móveis bloqueiam túneis.

**Solução:**
- Trocar para dados móveis ou WiFi diferente
- Testar com outro celular

---

## 🚀 **Soluções Alternativas**

### **Opção 1: ngrok (Mais Confiável)**
```powershell
# 1. Baixar: https://ngrok.com/download
# 2. Extrair e executar:
.\ngrok http 8000

# ✅ Resultado: https://abc123.ngrok.io
# ✅ Funciona em qualquer rede
```

### **Opção 2: Cloudflare Tunnel**
```powershell
# Instalar cloudflared
winget install Cloudflare.cloudflared

# Criar túnel
cloudflared tunnel --url http://localhost:8000

# ✅ Resultado: https://xyz.trycloudflare.com
```

### **Opção 3: VS Code Port Forward**
```bash
# No VS Code:
1. Ctrl+Shift+P → "Ports: Focus on Ports View"
2. Clique em "Forward a Port"  
3. Digite: 8000
4. Defina como "Public"
5. Copie novo link gerado
```

---

## 🧪 **Testes para Verificar**

### **1. Teste Local (PC)**
```bash
# Deve funcionar:
http://localhost:8000/docs
http://127.0.0.1:8000/docs
```

### **2. Teste DevTunnel (PC)**  
```bash
# Deve funcionar no PC:
https://7fbvhccr-8000.brs.devtunnels.ms/docs
```

### **3. Teste Celular (mesma rede WiFi)**
```bash
# IP local do PC (encontrar com ipconfig):
http://192.168.x.x:8000/docs
```

### **4. Teste Público (qualquer rede)**
```bash
# DevTunnel ou ngrok:
https://seu-link.ngrok.io/docs
```

---

## 📋 **Checklist de Debug**

### ✅ **Já Verificado:**
- [x] Servidor rodando em 0.0.0.0:8000
- [x] FastAPI respondendo localmente  
- [x] Logs mostram acessos externos
- [x] DevTunnel configurado

### 🔍 **Para Verificar:**
- [ ] DevTunnel é público no VS Code
- [ ] Celular está em rede diferente
- [ ] Testar outro navegador no celular
- [ ] Testar dados móveis vs WiFi

---

## 🎯 **Ação Imediata Recomendada**

### **Usar ngrok (100% confiável):**

```powershell
# 1. Baixar ngrok
Invoke-WebRequest -Uri "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip" -OutFile "ngrok.zip"
Expand-Archive ngrok.zip -DestinationPath C:\ngrok

# 2. Executar  
cd C:\ngrok
.\ngrok http 8000

# 3. Copiar link HTTPS gerado
# 4. Testar no celular: https://xyz.ngrok.io/docs
```

---

## 📱 **URLs para Testar no Celular**

Depois de configurar ngrok ou corrigir DevTunnel:

```
✅ Documentação: https://seu-link/docs
✅ Página inicial: https://seu-link/  
✅ Lambda status: https://seu-link/lambda/functions/status
✅ API empresas: https://seu-link/empresas/
```

---

## 🔧 **Status Atual**

### ✅ **Funcionando:**
- Servidor FastAPI online
- Aceita conexões externas
- DevTunnel ativo  

### 🔍 **Investigar:**
- Por que celular não acessa DevTunnel
- Configuração de visibilidade pública
- Rede do dispositivo móvel

### 🎯 **Próximo Passo:**
1. **Verificar se DevTunnel é público** no VS Code
2. **OU baixar ngrok** para alternativa 100% confiável
3. **Testar** novo link no celular

---

**💡 Dica**: ngrok é a opção mais confiável para apresentações, pois funciona em qualquer rede!