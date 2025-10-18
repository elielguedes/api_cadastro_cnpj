import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal

client = TestClient(app)


def get_admin_token():
    resp = client.post("/auth/register", json={"username": "admin_socio", "password": "secret"})
    if resp.status_code not in (200, 400):
        assert False, f"register failed: {resp.status_code} {resp.text}"
    db = SessionLocal()
    from app.models.models import Usuario
    u = db.query(Usuario).filter(Usuario.username == "admin_socio").first()
    u.is_admin = True
    db.commit()
    db.close()
    resp = client.post("/auth/login", data={"username": "admin_socio", "password": "secret"})
    assert resp.status_code == 200
    return resp.json()["access_token"]


def test_create_socio_flow():
    token = get_admin_token()
    headers = {"Authorization": f"Bearer {token}"}
    # create empresa with generated valid CNPJ
    def gen_cnpj(base12: str = "112223330001") -> str:
        def calc(digs, mult):
            s = sum(int(d) * m for d, m in zip(digs, mult))
            r = s % 11
            return "0" if r < 2 else str(11 - r)
        first = calc(base12, [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
        second = calc(base12 + first, [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
        full = base12 + first + second
        return f"{full[:2]}.{full[2:5]}.{full[5:8]}/{full[8:12]}-{full[12:]}"

    resp = client.post("/empresas/", json={"nome": "Empresa Socio", "cnpj": gen_cnpj()}, headers=headers)
    assert resp.status_code == 200
    empresa = resp.json()
    # create estabelecimento
    resp = client.post("/estabelecimentos/", json={"nome": "Matriz", "empresa_id": empresa["id"]}, headers=headers)
    assert resp.status_code == 200
    est = resp.json()
    # create socio valid
    resp = client.post("/socios/", json={"nome": "Joao", "estabelecimento_id": est["id"]}, headers=headers)
    assert resp.status_code == 200
    socio = resp.json()
    assert socio["nome"] == "Joao"


def test_create_socio_invalid_estabelecimento():
    token = get_admin_token()
    headers = {"Authorization": f"Bearer {token}"}
    resp = client.post("/socios/", json={"nome": "Maria", "estabelecimento_id": 99999}, headers=headers)
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Estabelecimento referenciado não existe"
