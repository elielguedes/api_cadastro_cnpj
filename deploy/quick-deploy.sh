#!/bin/bash

# quick-deploy.sh - Deploy super rápido
echo "🚀 Iniciando deploy rápido da aplicação FastAPI..."

# Definir variáveis
APP_DIR="/home/ubuntu/Relatorio_Eliel_Guedes"
REPO_URL="https://github.com/elielguedes/Relatorio_Eliel_Guedes.git"

# Função para log
log() {
    echo "✅ $1"
}

error() {
    echo "❌ $1"
    exit 1
}

# 1. Atualizar sistema
log "Atualizando sistema..."
sudo apt update -y || error "Falha ao atualizar sistema"

# 2. Instalar dependências básicas
log "Instalando dependências..."
sudo apt install -y python3 python3-pip python3-venv nginx git curl || error "Falha ao instalar dependências"

# 3. Clonar ou atualizar repositório
if [ -d "$APP_DIR" ]; then
    log "Atualizando repositório..."
    cd $APP_DIR && git pull
else
    log "Clonando repositório..."
    git clone $REPO_URL $APP_DIR || error "Falha ao clonar repositório"
fi

cd $APP_DIR

# 4. Configurar ambiente Python
log "Configurando ambiente Python..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt || error "Falha ao instalar dependências Python"

# 5. Configurar variáveis de ambiente
log "Configurando variáveis de ambiente..."
sudo tee /etc/environment > /dev/null <<EOF
SECRET_KEY="$(openssl rand -base64 32)"
DATABASE_URL="sqlite:///./app.db"
PYTHONPATH="$APP_DIR"
EOF

# 6. Aplicar migrations
log "Aplicando migrations..."
source /etc/environment
export PYTHONPATH="$APP_DIR"
python -m alembic upgrade head || log "Migrations falharam (pode ser normal se não há DB)"

# 7. Configurar Gunicorn
log "Instalando Gunicorn..."
pip install gunicorn

# 8. Criar diretórios de log
sudo mkdir -p /var/log/gunicorn /var/run/gunicorn
sudo chown ubuntu:www-data /var/log/gunicorn /var/run/gunicorn

# 9. Configurar systemd service
log "Configurando serviço systemd..."
sudo cp deploy/fastapi-app.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable fastapi-app

# 10. Configurar Nginx
log "Configurando Nginx..."
sudo cp deploy/nginx.conf /etc/nginx/sites-available/fastapi-app
sudo ln -sf /etc/nginx/sites-available/fastapi-app /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t || error "Configuração do Nginx inválida"

# 11. Iniciar serviços
log "Iniciando serviços..."
sudo systemctl start fastapi-app
sudo systemctl restart nginx

# 12. Verificar status
log "Verificando status..."
sleep 3
sudo systemctl is-active fastapi-app || error "FastAPI service não está ativo"
sudo systemctl is-active nginx || error "Nginx não está ativo"

# 13. Obter IP público
PUBLIC_IP=$(curl -s http://checkip.amazonaws.com)

echo ""
echo "🎉 Deploy concluído com sucesso!"
echo ""
echo "📱 Acesse sua aplicação:"
echo "   🌐 App: http://$PUBLIC_IP"
echo "   📚 Docs: http://$PUBLIC_IP/docs"
echo "   📖 Redoc: http://$PUBLIC_IP/redoc"
echo ""
echo "🔍 Para monitorar:"
echo "   sudo journalctl -u fastapi-app -f"
echo "   sudo systemctl status fastapi-app"
echo ""