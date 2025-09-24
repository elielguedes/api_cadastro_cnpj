from app.models.models import Estabelecimento
from app.schemas import EstabelecimentoCreate

def create_estabelecimento_service(db, estabelecimento: EstabelecimentoCreate):
    db_estabelecimento = Estabelecimento(nome=estabelecimento.nome, empresa_id=estabelecimento.empresa_id)
    db.add(db_estabelecimento)
    db.commit()
    db.refresh(db_estabelecimento)
    return db_estabelecimento

def get_estabelecimentos_service(db, skip: int = 0, limit: int = 10):
    return db.query(Estabelecimento).offset(skip).limit(limit).all()

def get_estabelecimento_service(db, estabelecimento_id: int):
    return db.query(Estabelecimento).filter(Estabelecimento.id == estabelecimento_id).first()

def delete_estabelecimento_service(db, estabelecimento_id: int):
    estabelecimento = db.query(Estabelecimento).filter(Estabelecimento.id == estabelecimento_id).first()
    if estabelecimento is None:
        return False
    db.delete(estabelecimento)
    db.commit()
    return True
