from typing import Generator
from app.database import SessionLocal
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from typing import Any
import os

from app.models.models import Usuario

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
ALGORITHM = os.getenv("ALGORITHM", "HS256")


def get_db() -> Generator:
    """FastAPI dependency that yields a SQLAlchemy Session and ensures it's closed."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)) -> Usuario:
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
    user = db.query(Usuario).filter(Usuario.username == username).first()
    if user is None:
        raise credentials_exception
    return user


def require_admin(current_user: Usuario = Depends(get_current_user)) -> Usuario:
    if not getattr(current_user, 'is_admin', False):
        raise HTTPException(status_code=403, detail="Apenas admin pode executar esta ação")
    return current_user
