from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.database import SessionLocal
from app.models.models import Empresa

with SessionLocal() as s:
    empresas = s.query(Empresa).all()
    if not empresas:
        print('No empresas found')
    for e in empresas:
        print(e.id, e.nome, e.cnpj)
