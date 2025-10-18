import os
from fastapi.testclient import TestClient

# ensure tests use the fallback sqlite DB
os.environ['DATABASE_URL'] = ''

from app.main import app
from app.database import engine, Base

client = TestClient(app)


def setup_module(module):
    # create tables
    Base.metadata.create_all(bind=engine)


def teardown_module(module):
    # teardown handled by tests/conftest.py
    pass


def test_tags_lifecycle():
    # register admin
    resp = client.post('/auth/register', json={'username': 'admin2', 'password': 'pass', 'is_admin': True})
    assert resp.status_code == 200

    # login
    resp = client.post('/auth/login', data={'username': 'admin2', 'password': 'pass'})
    assert resp.status_code == 200
    token = resp.json().get('access_token')
    assert token
    headers = {'Authorization': f'Bearer {token}'}

    # create empresa with a valid generated CNPJ
    def gen_cnpj(base12: str = "222222220001") -> str:
        def calc(digs, mult):
            s = sum(int(d) * m for d, m in zip(digs, mult))
            r = s % 11
            return "0" if r < 2 else str(11 - r)
        first = calc(base12, [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
        second = calc(base12 + first, [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
        full = base12 + first + second
        return f"{full[:2]}.{full[2:5]}.{full[5:8]}/{full[8:12]}-{full[12:]}"

    resp = client.post('/empresas/', json={'nome': 'TAGCO', 'cnpj': gen_cnpj()}, headers=headers)
    assert resp.status_code == 200
    empresa = resp.json()
    empresa_id = empresa['id']

    # create tag
    resp = client.post('/tags/', json={'name': 'financeiro'}, headers=headers)
    assert resp.status_code == 200
    tag = resp.json()
    tag_id = tag['id']

    # associate tag to empresa
    resp = client.post(f'/tags/{tag_id}/empresas/{empresa_id}', headers=headers)
    assert resp.status_code == 200

    # fetch empresa and verify tag present
    resp = client.get(f'/empresas/{empresa_id}', headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert 'tags' in data
    assert any(t['name'] == 'financeiro' for t in data['tags'])

    # remove association
    resp = client.delete(f'/tags/{tag_id}/empresas/{empresa_id}', headers=headers)
    assert resp.status_code == 200

    # fetch again, tags should be empty or not contain that tag
    resp = client.get(f'/empresas/{empresa_id}', headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert all(t['name'] != 'financeiro' for t in data.get('tags', []))

    # delete tag
    resp = client.delete(f'/tags/{tag_id}', headers=headers)
    assert resp.status_code == 200

    # list tags and ensure it's gone
    resp = client.get('/tags/', headers=headers)
    assert resp.status_code == 200
    assert all(t['id'] != tag_id for t in resp.json())
