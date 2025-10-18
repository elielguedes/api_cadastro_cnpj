from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas import EstabelecimentoCreate, Estabelecimento
from app.deps import get_db, require_admin
from app.services.estabelecimento_service import (
    create_estabelecimento_service,
    get_estabelecimentos_service,
    get_estabelecimento_service,
    delete_estabelecimento_service
)

router = APIRouter()

@router.post("/", response_model=Estabelecimento)
def create_estabelecimento(estabelecimento: EstabelecimentoCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    return create_estabelecimento_service(db, estabelecimento)

@router.get("/", response_model=List[Estabelecimento])
def read_estabelecimentos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_estabelecimentos_service(db, skip, limit)

@router.get("/{estabelecimento_id}", response_model=Estabelecimento)
def read_estabelecimento(estabelecimento_id: int, db: Session = Depends(get_db)):
    estabelecimento = get_estabelecimento_service(db, estabelecimento_id)
    if estabelecimento is None:
        raise HTTPException(status_code=404, detail="Estabelecimento not found")
    return estabelecimento

@router.delete("/{estabelecimento_id}")
def delete_estabelecimento(estabelecimento_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    ok = delete_estabelecimento_service(db, estabelecimento_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Estabelecimento not found")
    return {"ok": True}


@router.put("/{estabelecimento_id}", response_model=Estabelecimento)
def update_estabelecimento(estabelecimento_id: int, estabelecimento: EstabelecimentoCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    db_est = get_estabelecimento_service(db, estabelecimento_id)
    if db_est is None:
        raise HTTPException(status_code=404, detail="Estabelecimento not found")
    db_est.nome = estabelecimento.nome
    db_est.empresa_id = estabelecimento.empresa_id
    db.commit()
    db.refresh(db_est)
    return db_est
