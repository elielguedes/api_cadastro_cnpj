import os
from fastapi.testclient import TestClient

os.environ['DATABASE_URL'] = ''

from app.main import app
from app.database import engine, Base

client = TestClient(app)


def setup_module(module):
    Base.metadata.create_all(bind=engine)


def teardown_module(module):
    Base.metadata.drop_all(bind=engine)


def test_create_and_update_cnpj_normalization():
    # register admin
    resp = client.post('/auth/register', json={'username': 'cnpjadmin', 'password': 'pass', 'is_admin': True})
    assert resp.status_code == 200

    # login
    resp = client.post('/auth/login', data={'username': 'cnpjadmin', 'password': 'pass'})
    assert resp.status_code == 200
    token = resp.json().get('access_token')
    headers = {'Authorization': f'Bearer {token}'}

    # create empresa with masked cnpj
    resp = client.post('/empresas/', json={'nome': 'CNPJCO', 'cnpj': '00.000.000/0001-99'}, headers=headers)
    assert resp.status_code == 200
    empresa = resp.json()
    assert empresa['cnpj'] == '00000000000199'

    # update empresa with different masked cnpj
    empresa_id = empresa['id']
    resp = client.put(f'/empresas/{empresa_id}', json={'nome': 'CNPJCO', 'cnpj': '11.111.111/1111-11'}, headers=headers)
    assert resp.status_code == 200
    assert resp.json()['cnpj'] == '11111111111111'
