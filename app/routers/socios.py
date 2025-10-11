from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import SocioCreate, Socio
from app.deps import get_db, require_admin
from app.services.socio_service import (
    create_socio_service,
    get_socios_service,
    get_socio_service,
    delete_socio_service
)

router = APIRouter()

@router.post("/", response_model=Socio)
def create_socio(socio: SocioCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    return create_socio_service(db, socio)

@router.get("/", response_model=list[Socio])
def read_socios(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_socios_service(db, skip, limit)

@router.get("/{socio_id}", response_model=Socio)
def read_socio(socio_id: int, db: Session = Depends(get_db)):
    socio = get_socio_service(db, socio_id)
    if socio is None:
        raise HTTPException(status_code=404, detail="Sócio não encontrado")
    return socio

@router.delete("/{socio_id}")
def delete_socio(socio_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    ok = delete_socio_service(db, socio_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Sócio não encontrado")
    return {"ok": True}


@router.put("/{socio_id}", response_model=Socio)
def update_socio(socio_id: int, socio: SocioCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    db_socio = get_socio_service(db, socio_id)
    if db_socio is None:
        raise HTTPException(status_code=404, detail="Sócio não encontrado")
    db_socio.nome = socio.nome
    db_socio.estabelecimento_id = socio.estabelecimento_id
    db.commit()
    db.refresh(db_socio)
    return db_socio
