from app.models.models import Empresa
from app.schemas import EmpresaCreate

def create_empresa_service(db, empresa: EmpresaCreate):
    db_empresa = Empresa(nome=empresa.nome, cnpj=empresa.cnpj)
    db.add(db_empresa)
    db.commit()
    db.refresh(db_empresa)
    return db_empresa

def get_empresas_service(db, skip: int = 0, limit: int = 10):
    return db.query(Empresa).offset(skip).limit(limit).all()

def get_empresa_service(db, empresa_id: int):
    return db.query(Empresa).filter(Empresa.id == empresa_id).first()

def delete_empresa_service(db, empresa_id: int):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if empresa is None:
        return False
    db.delete(empresa)
    db.commit()
    return True