#!/usr/bin/env python3
"""
Script para iniciar a aplicação FastAPI com SQLite local
Força o uso do SQLite removendo qualquer DATABASE_URL
"""

import os
import sys
import subprocess

def main():
    # Remove DATABASE_URL para forçar SQLite
    if 'DATABASE_URL' in os.environ:
        del os.environ['DATABASE_URL']
    
    print("🔧 Iniciando FastAPI com SQLite local...")
    print("📦 Banco: sqlite:///./app.db")
    print("🌐 URL: http://127.0.0.1:8000")
    print("📚 Docs: http://127.0.0.1:8000/docs")
    print("-" * 50)
    
    # Inicia o servidor
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--reload", 
            "--host", "127.0.0.1", 
            "--port", "8000"
        ], check=True)
    except KeyboardInterrupt:
        print("\n✅ Servidor parado pelo usuário")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()