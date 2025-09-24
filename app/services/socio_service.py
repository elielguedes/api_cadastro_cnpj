from app.models.models import Socio
from app.schemas import SocioCreate

def create_socio_service(db, socio: SocioCreate):
    db_socio = Socio(nome=socio.nome, estabelecimento_id=socio.estabelecimento_id)
    db.add(db_socio)
    db.commit()
    db.refresh(db_socio)
    return db_socio

def get_socios_service(db, skip: int = 0, limit: int = 10):
    return db.query(Socio).offset(skip).limit(limit).all()

def get_socio_service(db, socio_id: int):
    return db.query(Socio).filter(Socio.id == socio_id).first()

def delete_socio_service(db, socio_id: int):
    socio = db.query(Socio).filter(Socio.id == socio_id).first()
    if socio is None:
        return False
    db.delete(socio)
    db.commit()
    return True
