# Gunicorn configuration for FastAPI
bind = "127.0.0.1:8000"
workers = 2  # Ajuste conforme o número de CPUs da instância
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2

# Logging
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
loglevel = "info"

# Process naming
proc_name = "fastapi-app"

# Daemon mode
daemon = False

# PID file
pidfile = "/var/run/gunicorn/fastapi.pid"

# User and group
user = "ubuntu"
group = "www-data"