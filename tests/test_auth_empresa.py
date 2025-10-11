import os
import pytest
from fastapi.testclient import TestClient

# make sure tests use an in-memory sqlite DB
os.environ['DATABASE_URL'] = ''

from app.main import app
from app.database import engine, Base, SessionLocal

client = TestClient(app)

@pytest.fixture(scope='module', autouse=True)
def setup_db():
    # create tables in the sqlite file used by the app.database fallback
    Base.metadata.create_all(bind=engine)
    yield
    # teardown
    Base.metadata.drop_all(bind=engine)

def test_register_and_login_and_crud():
    # register admin user
    resp = client.post('/auth/register', json={'username': 'admin', 'password': 'pass', 'is_admin': True})
    assert resp.status_code == 200

    # login
    data = {'username': 'admin', 'password': 'pass'}
    resp = client.post('/auth/login', data=data)
    assert resp.status_code == 200
    token = resp.json().get('access_token')
    assert token
    headers = {'Authorization': f'Bearer {token}'}

    # create empresa
    resp = client.post('/empresas/', json={'nome': 'ACME', 'cnpj': '00.000.000/0001-00'}, headers=headers)
    assert resp.status_code == 200
    empresa = resp.json()
    assert empresa['nome'] == 'ACME'

    # list empresas
    resp = client.get('/empresas/', headers=headers)
    assert resp.status_code == 200
    assert any(e['nome'] == 'ACME' for e in resp.json())

    # update empresa
    empresa_id = empresa['id']
    resp = client.put(f'/empresas/{empresa_id}', json={'nome': 'ACME2', 'cnpj': '11.111.111/1111-11'}, headers=headers)
    assert resp.status_code == 200
    assert resp.json()['nome'] == 'ACME2'

    # delete empresa
    resp = client.delete(f'/empresas/{empresa_id}', headers=headers)
    assert resp.status_code == 200
    assert resp.json().get('ok') is True
