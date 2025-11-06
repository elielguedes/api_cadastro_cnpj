# 🚀 DEPLOY NA EC2 - PASSO A PASSO

## 📋 VOCÊ JÁ TEM TUDO PRONTO!

### ✅ O que já está configurado:
- ✅ **Instância EC2** criada
- ✅ **Security Groups** configurados (22, 80, 443, 8000)
- ✅ **Scripts de deploy** prontos
- ✅ **Repositório GitHub** com código atualizado
- ✅ **Aplicação funcionando** localmente

## 🎯 AGORA VAMOS FAZER O DEPLOY!

### 1. **Conectar na EC2**

No PowerShell (não precisa ser admin):
```powershell
# Navegar para onde está sua chave SSH
cd C:\Users\eliel\Downloads  # ou onde salvou a chave

# Conectar na EC2 (substitua pela sua chave e IP)
ssh -i "sua-chave.pem" ubuntu@SEU-IP-EC2
```

### 2. **Executar Deploy Automático**

Dentro da EC2, execute:
```bash
# Baixar e executar script de deploy rápido
curl -fsSL https://raw.githubusercontent.com/elielguedes/Relatorio_Eliel_Guedes/main/deploy/quick-deploy.sh | bash

# OU se preferir passo a passo:
git clone https://github.com/elielguedes/Relatorio_Eliel_Guedes.git
cd Relatorio_Eliel_Guedes
chmod +x deploy/quick-deploy.sh
./deploy/quick-deploy.sh
```

### 3. **Verificar Deploy**

```bash
# Verificar se aplicação está rodando
sudo systemctl status fastapi-app

# Ver logs se houver problemas
sudo journalctl -u fastapi-app -f

# Testar aplicação
curl http://localhost:8000
curl http://localhost:8000/docs
```

### 4. **Acessar via Browser**

```
http://SEU-IP-EC2:8000/docs
http://SEU-IP-EC2/docs  # Se nginx configurado
```

## 🔧 SE HOUVER PROBLEMAS:

### Problema 1: SSH não conecta
```powershell
# Verificar permissões da chave (Windows)
icacls sua-chave.pem /grant:r "%USERNAME%:(R)" /inheritance:r
```

### Problema 2: Aplicação não sobe
```bash
# Verificar logs
sudo journalctl -u fastapi-app -n 50

# Verificar se PostgreSQL está rodando
sudo systemctl status postgresql

# Recriar banco se necessário
sudo -u postgres createdb empresas_db
```

### Problema 3: Nginx não funciona
```bash
# Verificar configuração nginx
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx
```

## 📊 COMANDOS ÚTEIS NA EC2:

```bash
# Parar aplicação
sudo systemctl stop fastapi-app

# Iniciar aplicação  
sudo systemctl start fastapi-app

# Restart aplicação
sudo systemctl restart fastapi-app

# Ver logs em tempo real
sudo journalctl -u fastapi-app -f

# Atualizar código
cd /home/ubuntu/Relatorio_Eliel_Guedes
git pull origin main
sudo systemctl restart fastapi-app
```

## 🎯 INFORMAÇÕES DA SUA EC2:

Complete com seus dados:
- **IP Público**: `_______________`
- **Chave SSH**: `_______________`
- **Security Group**: ✅ Já configurado
- **Região**: `_______________`

## 🚀 APÓS O DEPLOY:

1. **Testar todos os endpoints**
2. **Configurar SSL/HTTPS** (opcional)
3. **Configurar backup automático**
4. **Monitoramento** (opcional)

## 💡 LEMBRE-SE:

- **Sua aplicação LOCAL continua funcionando** com SQLite
- **EC2 usará PostgreSQL** automaticamente
- **Código é o mesmo**, só muda o banco de dados
- **Deploy é automatizado** pelo script