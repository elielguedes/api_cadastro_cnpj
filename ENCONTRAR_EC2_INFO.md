# 🔑 ENCONTRAR SUAS INFORMAÇÕES DA EC2

## 📋 VOCÊ PRECISA LOCALIZAR:

### 1. **Chave SSH (.pem)**
Procure nos locais comuns:
```powershell
# Verificar Downloads
Get-ChildItem C:\Users\eliel\Downloads -Filter "*.pem"

# Verificar Desktop
Get-ChildItem C:\Users\eliel\Desktop -Filter "*.pem"

# Verificar Documents
Get-ChildItem C:\Users\eliel\Documents -Filter "*.pem"

# Buscar em todo C:\Users\eliel
Get-ChildItem C:\Users\eliel -Recurse -Filter "*.pem" -ErrorAction SilentlyContinue
```

### 2. **IP da EC2**
- Acesse o **AWS Console**
- Vá em **EC2** → **Instances**
- Copie o **Public IPv4 address**

### 3. **Verificar Security Group**
- Na instância EC2, aba **Security**
- Verificar se tem **porta 22** (SSH) liberada

## 🚀 COMANDOS CORRETOS APÓS ENCONTRAR:

### Exemplo com dados reais:
```powershell
# Navegar para onde está a chave
cd C:\Users\eliel\Downloads  # ou onde encontrou a chave

# Conectar (substitua pelos dados reais)
ssh -i "minha-chave-ec2.pem" ubuntu@18.223.123.45

# Dentro da EC2, então executar:
curl -fsSL https://raw.githubusercontent.com/elielguedes/api_cadastro_cnpj/main/deploy/quick-deploy.sh | bash
```

## 🔧 SE NÃO TIVER AS INFORMAÇÕES:

### Opção 1: Criar nova EC2
1. AWS Console → EC2 → Launch Instance
2. **Ubuntu Server 22.04 LTS**
3. **t3.micro** (Free Tier)
4. **Criar nova chave SSH** (baixar .pem)
5. **Security Group**: SSH (22), HTTP (80), HTTPS (443), Custom TCP (8000)

### Opção 2: Instalar PostgreSQL local (mais rápido)
```powershell
# Baixar PostgreSQL para Windows
Invoke-WebRequest -Uri "https://get.enterprisedb.com/postgresql/postgresql-15.8-1-windows-x64.exe" -OutFile "postgresql-installer.exe"

# Executar instalador
.\postgresql-installer.exe
```

## 💡 ENQUANTO ISSO, CONTINUE COM SQLITE:

Sua aplicação **JÁ FUNCIONA** localmente:
```powershell
# Rodar aplicação local (funciona 100%)
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## 📞 ME DIGA:
1. **Você tem a chave SSH salva?** Se sim, onde?
2. **Você lembra o IP da EC2?** 
3. **Prefere criar nova EC2** ou **instalar PostgreSQL local?**