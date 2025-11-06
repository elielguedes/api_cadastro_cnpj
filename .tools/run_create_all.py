import traceback, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    from app.database import Base, engine
    print('Got Base and engine, calling create_all...')
    Base.metadata.create_all(bind=engine)
    print('create_all finished OK')
except Exception:
    traceback.print_exc()
