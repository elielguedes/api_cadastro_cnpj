from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.database import SessionLocal
from app.models.models import Usuario

with SessionLocal() as s:
    u = s.query(Usuario).filter(Usuario.username == 'eliel').first()
    if u:
        print('Found user:')
        print(' id:', u.id)
        print(' username:', u.username)
        print(' is_admin:', u.is_admin)
        print(' hashed_password repr:', repr(u.hashed_password)[:60])
    else:
        print("Usuário 'eliel' não encontrado no banco de dados.")
