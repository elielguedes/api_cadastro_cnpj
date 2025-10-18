from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import bcrypt
import hashlib
from passlib.context import CryptContext
from jose import jwt, JWTError
from app.models.models import Usuario as UsuarioModel
from app.schemas import UsuarioCreate, Usuario
from app.deps import get_db
import os
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Union, Optional

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Use bcrypt_sha256 to avoid the native bcrypt 72-byte input limit
# bcrypt_sha256 pre-hashes passwords with SHA-256 before bcrypt, so very
# long inputs won't trigger the C backend ValueError during passlib's
# internal self-tests and normal hashing/verification.
pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
    scopes={
        "admin": "Acesso total: criar, ler, deletar",
        "leitor": "Acesso somente leitura"
    }
)

router = APIRouter()

def _prehash(password: Union[str, bytes]) -> bytes:
    """Pre-hash a password using SHA-256 and return raw bytes.

    This keeps the input to bcrypt under its 72-byte limit and is a
    well-known pattern (bcrypt-sha256). We use the stdlib hashlib to
    produce a 32-byte digest which we pass to bcrypt.
    """
    if isinstance(password, str):
        password = password.encode("utf-8")
    return hashlib.sha256(password).digest()


def get_password_hash(password: str) -> str:
    """Hash a password: sha256 -> bcrypt.

    Returns the bcrypt hash as a UTF-8 string for storage in the DB.
    """
    key = _prehash(password)
    hashed = bcrypt.hashpw(key, bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against the stored bcrypt hash.

    We pre-hash the candidate password with SHA-256 then use
    bcrypt.checkpw to compare with the stored hash.
    """
    key = _prehash(plain_password)
    if isinstance(hashed_password, str):
        hashed_bytes = hashed_password.encode("utf-8")
    else:
        hashed_bytes = hashed_password
    return bcrypt.checkpw(key, hashed_bytes)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    scopes = data.get("scopes", ["leitor"])
    # use timezone-aware UTC datetime and encode exp as integer timestamp (seconds)
    expire_dt = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": int(expire_dt.timestamp()), "scopes": scopes})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/register", response_model=Usuario)
def register(user: UsuarioCreate, db: Session = Depends(get_db)):
    db_user = db.query(UsuarioModel).filter(UsuarioModel.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Usuário já existe")
    hashed_password = get_password_hash(user.password)
    new_user = UsuarioModel(username=user.username, hashed_password=hashed_password, is_admin=user.is_admin)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"id": new_user.id, "username": new_user.username, "is_admin": new_user.is_admin}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UsuarioModel).filter(UsuarioModel.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Usuário ou senha inválidos")
    scopes = ["admin"] if bool(user.is_admin) else ["leitor"]
    access_token = create_access_token(data={"sub": user.username, "is_admin": user.is_admin, "scopes": scopes})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=Usuario)
def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
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
    user = db.query(UsuarioModel).filter(UsuarioModel.username == username).first()
    if user is None:
        raise credentials_exception
    return {"id": user.id, "username": user.username, "is_admin": user.is_admin}
