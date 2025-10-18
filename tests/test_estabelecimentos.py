import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal

client = TestClient(app)


def get_admin_token():
    # register and promote to admin via direct DB for tests convenience
    resp = client.post("/auth/register", json={"username": "admin_est", "password": "secret"})
    # usuário pode já existir de execuções anteriores; aceitar 200 ou 400
    if resp.status_code not in (200, 400):
        assert False, f"register failed: {resp.status_code} {resp.text}"
    # make admin in DB
    db = SessionLocal()
    from app.models.models import Usuario
    u = db.query(Usuario).filter(Usuario.username == "admin_est").first()
    if u:
        setattr(u, 'is_admin', True)
        db.commit()
    db.close()
    resp = client.post("/auth/login", data={"username": "admin_est", "password": "secret"})
    assert resp.status_code == 200
    return resp.json()["access_token"]


def test_create_estabelecimento_and_list():
    token = get_admin_token()
    headers = {"Authorization": f"Bearer {token}"}
    # create empresa first with a valid generated CNPJ
    def gen_cnpj(base12: str = "123456780001") -> str:
        def calc(digs, mult):
            s = sum(int(d) * m for d, m in zip(digs, mult))
            r = s % 11
            return "0" if r < 2 else str(11 - r)
        first = calc(base12, [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
        second = calc(base12 + first, [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
        full = base12 + first + second
        return f"{full[:2]}.{full[2:5]}.{full[5:8]}/{full[8:12]}-{full[12:]}"

    resp = client.post("/empresas/", json={"nome": "ACME Ltda", "cnpj": gen_cnpj()}, headers=headers)
    assert resp.status_code == 200
    empresa = resp.json()

    # create estabelecimento valid
    resp = client.post("/estabelecimentos/", json={"nome": "Filial 1", "empresa_id": empresa["id"]}, headers=headers)
    assert resp.status_code == 200
    est = resp.json()
    assert est["nome"] == "Filial 1"

    # list estabelecimentos
    resp = client.get("/estabelecimentos/")
    assert resp.status_code == 200
    lst = resp.json()
    assert any(e["id"] == est["id"] for e in lst)


def test_create_estabelecimento_invalid_empresa():
    token = get_admin_token()
    headers = {"Authorization": f"Bearer {token}"}
    # try to create estabelecimento with non-existent empresa_id
    resp = client.post("/estabelecimentos/", json={"nome": "Filial X", "empresa_id": 999999}, headers=headers)
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Empresa referenciada não existe"
