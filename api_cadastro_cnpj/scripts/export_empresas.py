"""Exporta todas as empresas da tabela `empresas` para data/empresas_importadas.csv

Executar:
    venv/Scripts/python.exe scripts/export_empresas.py

O script imprime o número de linhas exportadas e o caminho do arquivo.
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.database import SessionLocal, Base, engine
from app.models.models import Empresa
import pandas as pd

OUT = ROOT / 'data' / 'empresas_importadas.csv'

with SessionLocal() as db:
    # garante que a tabela exista
    Base.metadata.create_all(bind=engine)
    rows = []
    for e in db.query(Empresa).all():
        rows.append({'id': e.id, 'nome': e.nome, 'cnpj': e.cnpj})

if rows:
    df = pd.DataFrame(rows)
    df.to_csv(OUT, index=False, sep=';')
    print(f'Exportadas {len(rows)} empresas para: {OUT}')
else:
    # cria arquivo vazio com cabeçalho
    df = pd.DataFrame(columns=['id','nome','cnpj'])
    df.to_csv(OUT, index=False, sep=';')
    print('Nenhuma empresa encontrada no banco. Arquivo criado com cabeçalho em:', OUT)
