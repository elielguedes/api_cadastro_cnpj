# Importa o FastAPI e componentes do projeto
from fastapi import FastAPI
from app.database import Base, engine
from app.routers import empresas, estabelecimentos, socios
from app.auth import router as auth_router

# Inicializa a aplicação FastAPI
app = FastAPI()

# Inclui as rotas das entidades principais na aplicação
app.include_router(empresas.router, prefix="/empresas", tags=["empresas"])
app.include_router(estabelecimentos.router, prefix="/estabelecimentos", tags=["estabelecimentos"])
app.include_router(socios.router, prefix="/socios", tags=["socios"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])

# Cria as tabelas no banco de dados SQLite usando SQLAlchemy
Base.metadata.create_all(bind=engine)

# Arquivos e pastas a serem ignorados pelo Git
venv/
__pycache__/
*.db
*.pyc