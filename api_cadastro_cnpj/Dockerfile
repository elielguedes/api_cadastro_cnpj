# Dockerfile para API FastAPI - Compatível com EC2
FROM python:3.12-slim

# Metadados
LABEL maintainer="Eliel Guedes"
LABEL description="API FastAPI para cadastro CNPJ"

# Define diretório de trabalho
WORKDIR /app

# Instala dependências do sistema necessárias
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copia arquivo de requirements
COPY requirements.txt .

# Instala dependências Python
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copia código da aplicação
COPY . .

# Cria diretório para dados e logs
RUN mkdir -p /app/data /app/logs

# Define variáveis de ambiente
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV SECRET_KEY=production-change-me

# Cria usuário não-root para segurança
RUN groupadd -r appuser && useradd -r -g appuser appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expõe porta
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Comando para iniciar aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]