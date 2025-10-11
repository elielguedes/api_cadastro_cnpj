import os
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.models import Base, Empresa


def get_database_url():
    return os.getenv('DATABASE_URL', 'postgresql+psycopg2://postgres:postgres@localhost:5432/empresas_db')


def create_tables(engine):
    Base.metadata.create_all(bind=engine)


def seed_empresas(session, csv_path):
    with open(csv_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            nome = row.get('nome') or row.get('Nome') or row.get('NOME') or row.get('RAZAO_SOCIAL') or row.get('razao_social')
            cnpj = row.get('cnpj') or row.get('CNPJ') or None
            if nome:
                empresa = Empresa(nome=nome, cnpj=cnpj)
                session.add(empresa)
        session.commit()


def main():
    database_url = get_database_url()
    engine = create_engine(database_url)
    create_tables(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'Empresas.csv')
    if os.path.exists(csv_path):
        seed_empresas(session, csv_path)
        print('Seed concluído')
    else:
        print('CSV não encontrado em', csv_path)


if __name__ == '__main__':
    main()
