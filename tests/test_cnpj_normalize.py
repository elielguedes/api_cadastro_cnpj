import os
from fastapi.testclient import TestClient

os.environ['DATABASE_URL'] = ''

from app.main import app
from app.database import engine, Base

client = TestClient(app)


def setup_module(module):
    Base.metadata.create_all(bind=engine)


def teardown_module(module):
    # teardown handled by tests/conftest.py
    pass


def test_create_and_update_cnpj_normalization():
    # register admin
    resp = client.post('/auth/register', json={'username': 'cnpjadmin', 'password': 'pass', 'is_admin': True})
    assert resp.status_code == 200

    # login
    resp = client.post('/auth/login', data={'username': 'cnpjadmin', 'password': 'pass'})
    assert resp.status_code == 200
    token = resp.json().get('access_token')
    headers = {'Authorization': f'Bearer {token}'}

    # helper to generate valid CNPJs (same algorithm used in other tests)
    def gen_cnpj(base12: str = "000000000001") -> str:
        def calc(digs, mult):
            s = sum(int(d) * m for d, m in zip(digs, mult))
            r = s % 11
            return "0" if r < 2 else str(11 - r)
        first = calc(base12, [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
        second = calc(base12 + first, [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
        full = base12 + first + second
        return f"{full[:2]}.{full[2:5]}.{full[5:8]}/{full[8:12]}-{full[12:]}"

    # create empresa with masked (formatted) but valid cnpj
    valid = gen_cnpj()
    resp = client.post('/empresas/', json={'nome': 'CNPJCO', 'cnpj': valid}, headers=headers)
    assert resp.status_code == 200
    empresa = resp.json()
    # normalized stored value should be digits-only
    assert empresa['cnpj'] == valid.replace('.', '').replace('/', '').replace('-', '')

    # update empresa with another valid masked cnpj
    empresa_id = empresa['id']
    new_valid = gen_cnpj("111111111111")
    resp = client.put(f'/empresas/{empresa_id}', json={'nome': 'CNPJCO', 'cnpj': new_valid}, headers=headers)
    assert resp.status_code == 200
    assert resp.json()['cnpj'] == new_valid.replace('.', '').replace('/', '').replace('-', '')
