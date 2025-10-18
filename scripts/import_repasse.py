"""Importador CSV para data/repasse-s.csv.
Executar usando o venv do projeto:

    venv\Scripts\python.exe scripts\import_repasse.py

O script valida CNPJ (usando app.utils.validate_cnpj), normaliza e insere
empresas únicas no banco via SessionLocal. Exibe um resumo no final.
"""
import os
import sys
from pathlib import Path

# Ajusta path para permitir import app
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pandas as pd
from app.database import SessionLocal, Base, engine
from app.models.models import Empresa
from app.utils import normalize_cnpj, validate_cnpj

CSV_PATH = ROOT / 'data' / 'repasse-s.csv'
if not CSV_PATH.exists():
    print('CSV não encontrado em', CSV_PATH)
    sys.exit(1)

print('Lendo CSV:', CSV_PATH)
try:
    df = pd.read_csv(CSV_PATH, sep=';')
except Exception as e:
    print('Erro ao ler CSV:', e)
    sys.exit(1)

processed = 0
inserted = 0
skipped_invalid = 0
skipped_duplicate = 0
errors = 0

with SessionLocal() as db:
    # garante que as tabelas existam (útil quando o script é executado isoladamente)
    Base.metadata.create_all(bind=engine)
    for idx, row in df.iterrows():
        processed += 1
        nome = row.get('Entidade') or row.get('entidade') or row.get('nome')
        raw_cnpj = row.get('UC/CNPJ') or row.get('CNPJ') or row.get('cnpj')
        if nome is None:
            # sem nome, pular
            skipped_invalid += 1
            continue
        if raw_cnpj is None:
            skipped_invalid += 1
            continue
        cnpj_norm = normalize_cnpj(str(raw_cnpj))
        if not validate_cnpj(cnpj_norm):
            skipped_invalid += 1
            continue
        # checar duplicata por cnpj
        existing = db.query(Empresa).filter(Empresa.cnpj == cnpj_norm).first()
        if existing:
            skipped_duplicate += 1
            continue
        try:
            empresa = Empresa(nome=str(nome), cnpj=cnpj_norm)
            db.add(empresa)
            db.commit()
            inserted += 1
        except Exception as e:
            db.rollback()
            errors += 1
            print(f'Erro inserindo linha {idx}: {e}')

print('\nResumo da importação:')
print('processados:', processed)
print('inseridos:', inserted)
print('duplicados (pulados):', skipped_duplicate)
print('inválidos (pulados):', skipped_invalid)
print('erros:', errors)
print('Fim')
