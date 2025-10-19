#!/usr/bin/env bash
# EC2 setup script for Ubuntu 22.04 to run FastAPI with systemd and Nginx
# Usage:
#   bash ./deploy_now/ec2_setup.sh
# Assumes the project is under /opt/api_cnpj (adjust PROJECT_DIR as needed)

set -euo pipefail

PROJECT_DIR="/opt/api_cnpj"
PYTHON="python3"
USER_SVC="ubuntu"
SERVICE_NAME="fastapi-app.service"
DOMAIN_OR_IP="18.118.167.28"  # change if you use a domain

sudo apt-get update -y
sudo apt-get install -y python3-venv python3-pip nginx git

# Create project dir and copy code if not present (adjust if using git pull instead)
if [ ! -d "$PROJECT_DIR" ]; then
  sudo mkdir -p "$PROJECT_DIR"
  sudo chown -R "$USER_SVC":"$USER_SVC" "$PROJECT_DIR"
fi

# If you prefer to pull from GitHub, uncomment below and set your repo URL
# sudo -u "$USER_SVC" bash -lc "git clone https://github.com/elielguedes/api_cadastro_cnpj.git $PROJECT_DIR || (cd $PROJECT_DIR && git pull)"

cd "$PROJECT_DIR"

# Setup venv
sudo -u "$USER_SVC" bash -lc "python3 -m venv .venv && . .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt"

# Create systemd service
sudo tee /etc/systemd/system/$SERVICE_NAME > /dev/null <<EOF
[Unit]
Description=FastAPI app (Uvicorn)
After=network.target

[Service]
User=$USER_SVC
WorkingDirectory=$PROJECT_DIR
Environment=PYTHONPATH=$PROJECT_DIR
Environment=ENVIRONMENT=production
ExecStart=$PROJECT_DIR/.venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
sudo systemctl restart $SERVICE_NAME

# Configure Nginx reverse proxy
sudo tee /etc/nginx/sites-available/fastapi_app > /dev/null <<NGINX
server {
    listen 80;
    server_name $DOMAIN_OR_IP;

    location / {
        proxy_pass         http://127.0.0.1:8000;
        proxy_redirect     off;
        proxy_http_version 1.1;
        proxy_set_header   Upgrade $http_upgrade;
        proxy_set_header   Connection "upgrade";
        proxy_set_header   Host $host;
        proxy_set_header   X-Real-IP $remote_addr;
        proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto $scheme;
    }
}
NGINX

sudo ln -sf /etc/nginx/sites-available/fastapi_app /etc/nginx/sites-enabled/fastapi_app
sudo rm -f /etc/nginx/sites-enabled/default || true
sudo nginx -t
sudo systemctl restart nginx

# Firewall (if ufw is used)
if command -v ufw >/dev/null 2>&1; then
  sudo ufw allow 'Nginx Full' || true
fi

# Health check
curl -fsS http://127.0.0.1:8000/health || true

echo "✅ EC2 setup concluído. Acesse: http://$DOMAIN_OR_IP/"
