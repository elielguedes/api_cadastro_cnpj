"""Importador CSV com relatório de linhas rejeitadas.

Gera `data/import_rejeitados.csv` contendo as linhas puladas com uma coluna adicional
`motivo` (ex.: 'cnpj_invalido', 'duplicado', 'sem_nome').

Executar:
    venv\\Scripts\\python.exe scripts\\import_repasse_with_report.py
"""
import os
import sys
from pathlib import Path
import argparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pandas as pd
from app.database import SessionLocal, Base, engine
from app.models.models import Empresa
from app.utils import normalize_cnpj, validate_cnpj

CSV_PATH = ROOT / 'data' / 'repasse-s.csv'
DEFAULT_OUT = ROOT / 'data' / 'import_rejeitados.csv'

parser = argparse.ArgumentParser()
parser.add_argument('--dry-run', action='store_true', help='Processa e gera relatório sem inserir no DB')
parser.add_argument('--limit', type=int, default=0, help='Limita número de linhas processadas (0 = sem limite)')
parser.add_argument('--out', type=str, default=str(DEFAULT_OUT), help='Caminho do arquivo de rejeitados')
args = parser.parse_args()

OUT_PATH = Path(args.out)

if not CSV_PATH.exists():
    print('CSV não encontrado em', CSV_PATH)
    sys.exit(1)

print('Lendo CSV:', CSV_PATH)
try:
    df = pd.read_csv(CSV_PATH, sep=';', dtype=str, keep_default_na=False)
except Exception as e:
    print('Erro ao ler CSV:', e)
    sys.exit(1)

if args.limit and args.limit > 0:
    df = df.head(args.limit)

processed = 0
inserted = 0
skipped_invalid = 0
skipped_duplicate = 0
errors = 0

rejected_rows = []

with SessionLocal() as db:
    Base.metadata.create_all(bind=engine)
    for idx, row in df.iterrows():
        processed += 1
        nome = row.get('Entidade') or row.get('entidade') or row.get('nome') or ''
        raw_cnpj = row.get('UC/CNPJ') or row.get('CNPJ') or row.get('cnpj') or ''

        motivo = None
        if not nome or str(nome).strip() == '':
            motivo = 'sem_nome'
        cnpj_norm = normalize_cnpj(str(raw_cnpj))
        if not motivo and (not cnpj_norm or not validate_cnpj(cnpj_norm)):
            motivo = 'cnpj_invalido'
        if not motivo:
            existing = db.query(Empresa).filter(Empresa.cnpj == cnpj_norm).first()
            if existing:
                motivo = 'duplicado'
        if motivo:
            if motivo in ('cnpj_invalido', 'sem_nome'):
                skipped_invalid += 1
            elif motivo == 'duplicado':
                skipped_duplicate += 1
            # anexa linha original + motivo
            out = row.to_dict()
            out['motivo'] = motivo
            out['cnpj_normalizado'] = cnpj_norm
            rejected_rows.append(out)
            continue
        # inserir (ou simular se dry-run)
        try:
            if not args.dry_run:
                empresa = Empresa(nome=str(nome), cnpj=cnpj_norm)
                db.add(empresa)
                db.commit()
            inserted += 1
        except Exception as e:
            if not args.dry_run:
                db.rollback()
            errors += 1
            out = row.to_dict()
            out['motivo'] = f'erro_insercao: {e}'
            rejected_rows.append(out)

# salva csv de rejeitados
if rejected_rows:
    out_df = pd.DataFrame(rejected_rows)
    out_df.to_csv(OUT_PATH, index=False, sep=';')
    print('Arquivo de rejeitados gerado em:', OUT_PATH)
else:
    print('Nenhuma linha rejeitada; arquivo não gerado.')

print('\nResumo da importação:')
print('processados:', processed)
print('inseridos (ou simulados):', inserted)
print('duplicados (pulados):', skipped_duplicate)
print('inválidos (pulados):', skipped_invalid)
print('erros:', errors)
print('Fim')
