from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import asc, desc
from typing import Optional, List
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.auth import SECRET_KEY, ALGORITHM
from sqlalchemy.orm import Session
from app.schemas import EmpresaCreate, Empresa, EmpresaRead
from app.deps import get_db, require_admin
from app.services.empresa_service import (
    create_empresa_service,
    get_empresas_service,
    get_empresa_service,
    delete_empresa_service
)

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")



@router.post("/", response_model=EmpresaRead, operation_id="create_empresa")
def create_empresa(empresa: EmpresaCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    return create_empresa_service(db, empresa)

@router.get("/", response_model=List[EmpresaRead], operation_id="read_empresas")
def read_empresas(
    skip: int = 0,
    limit: int = 10,
    nome: Optional[str] = None,
    cnpj: Optional[str] = None,
    order_by: str = "id",
    order: str = "asc",
    db: Session = Depends(get_db)
):
    from app.models.models import Empresa
    query = db.query(Empresa)
    if nome:
        query = query.filter(Empresa.nome.like(f"%{nome}%"))
    if cnpj:
        query = query.filter(Empresa.cnpj == cnpj)
    if order_by in ["id", "nome"]:
        order_column = getattr(Empresa, order_by)
        query = query.order_by(asc(order_column) if order == "asc" else desc(order_column))
    empresas = query.offset(skip).limit(limit).all()
    return empresas

@router.get("/{empresa_id}", response_model=EmpresaRead, operation_id="read_empresa")
def read_empresa(empresa_id: int, db: Session = Depends(get_db)):
    empresa = get_empresa_service(db, empresa_id)
    if empresa is None:
        raise HTTPException(status_code=404, detail="Empresa not found")
    return empresa

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não autorizado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not isinstance(username, str) or username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    from app.models.models import Usuario
    user = db.query(Usuario).filter(Usuario.username == username).first()
    if user is None:
        raise credentials_exception
    return user

@router.delete("/{empresa_id}", operation_id="delete_empresa")
def delete_empresa(empresa_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    ok = delete_empresa_service(db, empresa_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Empresa not found")
    return {"ok": True}


@router.put("/{empresa_id}", response_model=EmpresaRead, operation_id="update_empresa")
def update_empresa(empresa_id: int, empresa: EmpresaCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    db_empresa = get_empresa_service(db, empresa_id)
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa not found")
    # delegate normalization to service layer by assigning normalized cnpj
    from app.utils import normalize_cnpj
    from app.utils import validate_cnpj
    if not validate_cnpj(empresa.cnpj):
        raise HTTPException(status_code=400, detail="CNPJ inválido")
    db_empresa.nome = empresa.nome
    db_empresa.cnpj = normalize_cnpj(empresa.cnpj)
    db.commit()
    db.refresh(db_empresa)
    return db_empresa
