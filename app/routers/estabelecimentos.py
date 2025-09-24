from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import EstabelecimentoCreate, Estabelecimento
from app.database import SessionLocal
from app.services.estabelecimento_service import (
    create_estabelecimento_service,
    get_estabelecimentos_service,
    get_estabelecimento_service,
    delete_estabelecimento_service
)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=Estabelecimento)
def create_estabelecimento(estabelecimento: EstabelecimentoCreate, db: Session = Depends(get_db)):
    return create_estabelecimento_service(db, estabelecimento)

@router.get("/", response_model=list[Estabelecimento])
def read_estabelecimentos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_estabelecimentos_service(db, skip, limit)

@router.get("/{estabelecimento_id}", response_model=Estabelecimento)
def read_estabelecimento(estabelecimento_id: int, db: Session = Depends(get_db)):
    estabelecimento = get_estabelecimento_service(db, estabelecimento_id)
    if estabelecimento is None:
        raise HTTPException(status_code=404, detail="Estabelecimento not found")
    return estabelecimento

@router.delete("/{estabelecimento_id}")
def delete_estabelecimento(estabelecimento_id: int, db: Session = Depends(get_db)):
    ok = delete_estabelecimento_service(db, estabelecimento_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Estabelecimento not found")
    return {"ok": True}
