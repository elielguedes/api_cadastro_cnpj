# Deploy FastAPI no AWS EC2

## 1. Configuração da Instância EC2

### 1.1 Criando a Instância
1. No console AWS EC2, clique em "Launch Instance"
2. Escolha uma AMI (recomendado: Ubuntu Server 22.04 LTS)
3. Tipo de instância: t3.micro (free tier) ou t3.small para produção
4. Configure Security Group:
   - SSH (22) - Seu IP
   - HTTP (80) - 0.0.0.0/0
   - HTTPS (443) - 0.0.0.0/0
   - Custom TCP (8000) - 0.0.0.0/0 (temporário para testes)

### 1.2 Conectando na Instância
```bash
ssh -i sua-chave.pem ubuntu@seu-ip-publico
```

## 2. Preparação do Servidor

### 2.1 Atualização do Sistema
```bash
sudo apt update && sudo apt upgrade -y
```

### 2.2 Instalação do Python e dependências
```bash
sudo apt install python3 python3-pip python3-venv nginx git -y
```

### 2.3 Instalação do PostgreSQL (opcional)
```bash
sudo apt install postgresql postgresql-contrib -y
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

## 3. Deploy da Aplicação

### 3.1 Clone do Repositório
```bash
cd /home/ubuntu
git clone https://github.com/elielguedes/Relatorio_Eliel_Guedes.git
cd Relatorio_Eliel_Guedes
```

### 3.2 Configuração do Ambiente Virtual
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3.3 Configuração das Variáveis de Ambiente
```bash
sudo nano /etc/environment
```

Adicione:
```
SECRET_KEY="seu-secret-key-super-seguro-aqui"
DATABASE_URL="sqlite:///./app.db"
# Para PostgreSQL: DATABASE_URL="postgresql://user:pass@localhost/dbname"
```

### 3.4 Aplicar Migrations
```bash
source /etc/environment
export PYTHONPATH="/home/ubuntu/Relatorio_Eliel_Guedes"
python -m alembic upgrade head
```

## 4. Configuração do Gunicorn

### 4.1 Teste da Aplicação
```bash
# Teste rápido
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 4.2 Instalação e Configuração do Gunicorn
```bash
pip install gunicorn
```

Criar arquivo de configuração:
```bash
sudo nano /home/ubuntu/Relatorio_Eliel_Guedes/gunicorn.conf.py
```

## 5. Configuração do Nginx

### 5.1 Configuração do Site
```bash
sudo nano /etc/nginx/sites-available/fastapi-app
```

### 5.2 Habilitar o Site
```bash
sudo ln -s /etc/nginx/sites-available/fastapi-app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 6. Configuração do Systemd Service

### 6.1 Criar Service File
```bash
sudo nano /etc/systemd/system/fastapi-app.service
```

### 6.2 Habilitar e Iniciar o Serviço
```bash
sudo systemctl daemon-reload
sudo systemctl enable fastapi-app
sudo systemctl start fastapi-app
```

## 7. Configuração SSL (Opcional)

### 7.1 Instalação do Certbot
```bash
sudo apt install certbot python3-certbot-nginx -y
```

### 7.2 Obter Certificado SSL
```bash
sudo certbot --nginx -d seu-dominio.com
```

## 8. Monitoramento e Logs

### 8.1 Ver Status dos Serviços
```bash
sudo systemctl status fastapi-app
sudo systemctl status nginx
```

### 8.2 Ver Logs
```bash
sudo journalctl -u fastapi-app -f
sudo tail -f /var/log/nginx/error.log
```