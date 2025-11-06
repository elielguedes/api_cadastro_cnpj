from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas import EstabelecimentoCreate, Estabelecimento, EstabelecimentoUpdate
from app.deps import get_db, require_admin
from app.services.estabelecimento_service import (
    create_estabelecimento_service,
    get_estabelecimentos_service,
    get_estabelecimento_service,
    delete_estabelecimento_service,
)

router = APIRouter()

@router.post("/", response_model=Estabelecimento)
def create_estabelecimento(payload: EstabelecimentoCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    return create_estabelecimento_service(db, payload)

@router.get("/", response_model=List[Estabelecimento])
def read_estabelecimentos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_estabelecimentos_service(db, skip, limit)

@router.get("/{estabelecimento_id}", response_model=Estabelecimento)
def read_estabelecimento(estabelecimento_id: int, db: Session = Depends(get_db)):
    est = get_estabelecimento_service(db, estabelecimento_id)
    if est is None:
        raise HTTPException(status_code=404, detail="Estabelecimento não encontrado")
    return est

@router.delete("/{estabelecimento_id}")
def delete_estabelecimento(estabelecimento_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    ok = delete_estabelecimento_service(db, estabelecimento_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Estabelecimento não encontrado")
    return {"ok": True}


@router.put("/{estabelecimento_id}", response_model=Estabelecimento, operation_id="update_estabelecimento")
def update_estabelecimento(
    estabelecimento_id: int,
    payload: EstabelecimentoUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    from app.services.estabelecimento_service import update_estabelecimento_service

    updated = update_estabelecimento_service(db, estabelecimento_id, payload)
    if updated is None:
        raise HTTPException(status_code=404, detail="Estabelecimento não encontrado")
    return updated

