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
    # teardown is a no-op; conftest handles schema lifecycle for the whole session
    pass

def test_register_and_login_and_crud():
    # register admin user
    resp = client.post('/auth/register', json={'username': 'admin', 'password': 'pass', 'is_admin': True})
    # allow existing user (previous test runs) as acceptable
    if resp.status_code not in (200, 400):
        assert False, f"register failed: {resp.status_code} {resp.text}"

    # login
    data = {'username': 'admin', 'password': 'pass'}
    resp = client.post('/auth/login', data=data)
    assert resp.status_code == 200
    token = resp.json().get('access_token')
    assert token
    headers = {'Authorization': f'Bearer {token}'}

    # create empresa
    # create empresa with valid cnpj
    def gen_cnpj(base12: str = "000000000001") -> str:
        def calc(digs, mult):
            s = sum(int(d) * m for d, m in zip(digs, mult))
            r = s % 11
            return "0" if r < 2 else str(11 - r)
        first = calc(base12, [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
        second = calc(base12 + first, [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
        full = base12 + first + second
        return f"{full[:2]}.{full[2:5]}.{full[5:8]}/{full[8:12]}-{full[12:]}"

    resp = client.post('/empresas/', json={'nome': 'ACME', 'cnpj': gen_cnpj()}, headers=headers)
    assert resp.status_code == 200
    empresa = resp.json()
    assert empresa['nome'] == 'ACME'

    # list empresas
    resp = client.get('/empresas/', headers=headers)
    assert resp.status_code == 200
    assert any(e['nome'] == 'ACME' for e in resp.json())

    # update empresa
    empresa_id = empresa['id']
    # update empresa with another valid CNPJ
    new_cnpj = gen_cnpj("111111111111")
    resp = client.put(f'/empresas/{empresa_id}', json={'nome': 'ACME2', 'cnpj': new_cnpj}, headers=headers)
    assert resp.status_code == 200
    assert resp.json()['nome'] == 'ACME2'

    # delete empresa
    resp = client.delete(f'/empresas/{empresa_id}', headers=headers)
    assert resp.status_code == 200
    assert resp.json().get('ok') is True
