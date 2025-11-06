# Configuração de Produção para AWS EC2

Este documento contém as configurações específicas para deploy em produção no AWS EC2.

## Variáveis de Ambiente de Produção

Crie um arquivo `.env.production` na instância EC2:

```bash
# Segurança
SECRET_KEY=sua-chave-secreta-muito-segura-aqui-com-pelo-menos-32-caracteres
DEBUG=False

# Banco de dados
DATABASE_URL=postgresql://usuario:senha@localhost:5432/nome_do_banco

# Configurações do FastAPI
HOST=0.0.0.0
PORT=8000

# Logs
LOG_LEVEL=info

# CORS (ajuste conforme necessário)
ALLOWED_ORIGINS=["https://seu-dominio.com", "https://www.seu-dominio.com"]
```

## Configuração do PostgreSQL

```bash
# 1. Conectar ao PostgreSQL
sudo -u postgres psql

# 2. Criar banco e usuário
CREATE DATABASE relatorio_db;
CREATE USER app_user WITH ENCRYPTED PASSWORD 'senha_super_segura';
GRANT ALL PRIVILEGES ON DATABASE relatorio_db TO app_user;
ALTER USER app_user CREATEDB;
\q

# 3. Configurar pg_hba.conf
sudo nano /etc/postgresql/14/main/pg_hba.conf
# Adicionar: local   all   app_user   md5

# 4. Reiniciar PostgreSQL
sudo systemctl restart postgresql
```

## Configuração de Firewall

```bash
# Configurar UFW
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw --force enable
```

## Backup Automático

```bash
# Criar script de backup
sudo nano /home/ubuntu/backup.sh
```

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -h localhost -U app_user relatorio_db > /home/ubuntu/backups/backup_$DATE.sql
find /home/ubuntu/backups -name "backup_*.sql" -mtime +7 -delete
```

```bash
# Tornar executável
chmod +x /home/ubuntu/backup.sh

# Adicionar ao crontab
crontab -e
# Adicionar: 0 2 * * * /home/ubuntu/backup.sh
```

## Monitoramento

### Logs importantes:
- Aplicação: `sudo journalctl -u fastapi-app -f`
- Nginx: `sudo tail -f /var/log/nginx/fastapi_error.log`
- Sistema: `sudo tail -f /var/log/syslog`

### Comandos úteis:
```bash
# Status dos serviços
sudo systemctl status fastapi-app nginx postgresql

# Reiniciar serviços
sudo systemctl restart fastapi-app
sudo systemctl reload nginx

# Ver uso de recursos
htop
df -h
free -h
```

## SSL com Let's Encrypt

```bash
# Instalar certbot
sudo apt install certbot python3-certbot-nginx -y

# Obter certificado (substitua pelo seu domínio)
sudo certbot --nginx -d seu-dominio.com -d www.seu-dominio.com

# Renovação automática
sudo crontab -e
# Adicionar: 0 12 * * * /usr/bin/certbot renew --quiet
```

## Configuração de Domínio

1. No Route 53 (ou seu provedor DNS):
   - Criar record A apontando para o IP público da instância EC2
   - Opcional: criar record CNAME para www

2. Atualizar arquivo nginx com o domínio correto

3. Testar configuração:
```bash
nslookup seu-dominio.com
curl -I http://seu-dominio.com
```