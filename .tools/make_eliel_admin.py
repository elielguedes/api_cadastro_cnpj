from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.database import SessionLocal
from app.models.models import Usuario

with SessionLocal() as s:
    u = s.query(Usuario).filter(Usuario.username == 'eliel').first()
    if u:
        setattr(u, 'is_admin', True)
        s.add(u)
        s.commit()
        print(f"Usuário '{u.username}' atualizado para admin (id={u.id}).")
    else:
        print("Usuário 'eliel' não encontrado no banco de dados.")
