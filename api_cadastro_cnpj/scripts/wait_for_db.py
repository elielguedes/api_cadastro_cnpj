import os
import time
from sqlalchemy import create_engine


def get_database_url():
    return os.getenv('DATABASE_URL', 'postgresql+psycopg2://postgres:postgres@db:5432/empresas_db')


def wait_for_db(max_retries=60, delay=1):
    database_url = get_database_url()
    engine = create_engine(database_url)
    retries = 0
    while retries < max_retries:
        try:
            with engine.connect():
                print('Banco disponível!')
                return True
        except Exception as e:
            print(f'Aguardando banco... tentativa {retries+1}/{max_retries}')
            time.sleep(delay)
            retries += 1
    print('Tempo esgotado esperando o banco')
    return False


if __name__ == '__main__':
    ok = wait_for_db()
    if not ok:
        raise SystemExit('Banco não ficou disponível a tempo')
