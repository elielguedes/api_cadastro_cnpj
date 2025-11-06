from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas import SocioCreate, Socio, SocioUpdate
from app.deps import get_db, require_admin
from app.services.socio_service import (
    create_socio_service,
    get_socios_service,
    get_socio_service,
    delete_socio_service,
    update_socio_service,
)

router = APIRouter()

@router.post("/", response_model=Socio)
def create_socio(socio: SocioCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    return create_socio_service(db, socio)

@router.get("/", response_model=List[Socio])
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

@router.put("/{socio_id}", response_model=Socio, operation_id="update_socio")
def update_socio(
    socio_id: int,
    payload: SocioUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_admin)  # Mantido consistência com as outras funções
):
    updated = update_socio_service(db, socio_id, payload)
    if updated is None:
        raise HTTPException(status_code=404, detail="Sócio não encontrado")
    return updated
