import importlib, traceback, sys
from pathlib import Path

# Ensure repo root is on sys.path so 'app' package resolves like running from repo root
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    importlib.import_module('app.main')
    print('import ok')
except Exception:
    traceback.print_exc()
