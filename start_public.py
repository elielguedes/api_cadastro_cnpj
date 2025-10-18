import os
import sys
import subprocess

print("🌐 Iniciando FastAPI com acesso público...")
print("📦 Banco: sqlite:///./app.db")
print("🌍 Servidor: 0.0.0.0:8000 (acessível externamente)")
print("📚 Docs: http://0.0.0.0:8000/docs")
print("--" * 25)

# Remove variável de ambiente DATABASE_URL para forçar SQLite
if 'DATABASE_URL' in os.environ:
    del os.environ['DATABASE_URL']
    print("✅ DATABASE_URL removida - forçando SQLite")

try:
    # Inicia o servidor FastAPI com host 0.0.0.0 para aceitar conexões externas
    subprocess.run([
        sys.executable, "-m", "uvicorn", 
        "app.main:app", 
        "--host", "0.0.0.0", 
        "--port", "8000", 
        "--reload"
    ])
except KeyboardInterrupt:
    print("\n✅ Servidor parado pelo usuário")