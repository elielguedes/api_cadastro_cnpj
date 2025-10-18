# 🚀 DEPLOY RÁPIDO RENDER.COM

## Passos para Deploy Definitivo:

### 1️⃣ Preparar Repositório
```bash
git add .
git commit -m "Deploy para apresentação"
git push origin main
```

### 2️⃣ Deploy Render
1. **Acessar**: https://render.com
2. **Conectar GitHub**: Autorizar acesso ao repo
3. **New Web Service**: Selecionar "Relatorio_Eliel_Guedes"

### 3️⃣ Configurações Deploy:
- **Name**: api-cnpj-eliel
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Environment Variables**:
  ```
  DATABASE_URL = sqlite:///./app.db
  SECRET_KEY = minha_chave_secreta_super_segura
  ```

### 4️⃣ Link Final:
```
https://api-cnpj-eliel.onrender.com/docs
```

## ⚡ Tempo de Deploy: 3-5 minutos
## 💰 Custo: Gratuito
## 🔄 Disponibilidade: 24/7