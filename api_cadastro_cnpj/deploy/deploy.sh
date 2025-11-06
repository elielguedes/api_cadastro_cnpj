#!/bin/bash

# deploy.sh - Script de deploy automatizado para AWS EC2

set -e  # Parar em caso de erro

echo "=== Deploy FastAPI no AWS EC2 ==="

# 1. Atualizar sistema
echo "Atualizando sistema..."
sudo apt update && sudo apt upgrade -y

# 2. Instalar dependências
echo "Instalando dependências..."
sudo apt install python3 python3-pip python3-venv nginx git postgresql postgresql-contrib -y

# 3. Criar diretórios necessários
echo "Criando diretórios..."
sudo mkdir -p /var/log/gunicorn
sudo mkdir -p /var/run/gunicorn
sudo chown ubuntu:www-data /var/log/gunicorn
sudo chown ubuntu:www-data /var/run/gunicorn

# 4. Configurar ambiente virtual
echo "Configurando ambiente virtual..."
cd /home/ubuntu/Relatorio_Eliel_Guedes
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn

# 5. Configurar PYTHONPATH
export PYTHONPATH="/home/ubuntu/Relatorio_Eliel_Guedes"

# 6. Aplicar migrations
echo "Aplicando migrations..."
python -m alembic upgrade head

# 7. Copiar arquivos de configuração
echo "Copiando arquivos de configuração..."
sudo cp deploy/fastapi-app.service /etc/systemd/system/
sudo cp deploy/nginx.conf /etc/nginx/sites-available/fastapi-app
sudo cp deploy/gunicorn.conf.py /home/ubuntu/Relatorio_Eliel_Guedes/

# 8. Configurar nginx
echo "Configurando nginx..."
sudo ln -sf /etc/nginx/sites-available/fastapi-app /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t

# 9. Configurar e iniciar serviços
echo "Configurando serviços..."
sudo systemctl daemon-reload
sudo systemctl enable fastapi-app
sudo systemctl enable nginx

# 10. Iniciar serviços
echo "Iniciando serviços..."
sudo systemctl start fastapi-app
sudo systemctl restart nginx

# 11. Verificar status
echo "Verificando status dos serviços..."
sudo systemctl status fastapi-app --no-pager
sudo systemctl status nginx --no-pager

echo ""
echo "=== Deploy concluído! ==="
echo "Aplicação disponível em: http://$(curl -s http://checkip.amazonaws.com):80"
echo "Documentação da API: http://$(curl -s http://checkip.amazonaws.com)/docs"
echo ""
echo "Para monitorar logs:"
echo "sudo journalctl -u fastapi-app -f"
echo "sudo tail -f /var/log/nginx/fastapi_error.log"