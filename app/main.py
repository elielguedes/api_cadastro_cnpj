
from fastapi import FastAPI  
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware  
from app.database import Base, engine  
from app.routers import empresas, estabelecimentos, socios, tags  
from app.routers import lambda_routes  
from app.auth import router as auth_router  
import os  

app = FastAPI(
    title="API de Empresas Brasileiras",
    description="API RESTful para consulta de dados de empresas, estabelecimentos e sócios do dados.gov.br",
    version="1.0.0",
    docs_url="/docs" if os.getenv("ENVIRONMENT") != "production" else None,  
    redoc_url="/redoc" if os.getenv("ENVIRONMENT") != "production" else None,  
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) 

# Endpoint de health check para monitoramento
@app.get("/", tags=["health"])
async def health_check():
    """Endpoint de verificação de saúde da aplicação"""
    return {
        "status": "healthy",
        "message": "API de Empresas Brasileiras funcionando corretamente",
        "version": "1.0.0"
    }

@app.get("/health", tags=["health"])
async def detailed_health():
    """Endpoint detalhado de verificação de saúde"""
    return {
        "status": "healthy",
        "database": "connected",
        "services": ["empresas", "estabelecimentos", "socios", "auth"]
    }


app.include_router(empresas.router, prefix="/empresas", tags=["empresas"])  
app.include_router(estabelecimentos.router, prefix="/estabelecimentos", tags=["estabelecimentos"])  
app.include_router(socios.router, prefix="/socios", tags=["socios"]) 
app.include_router(auth_router, prefix="/auth", tags=["auth"])  
app.include_router(tags.router, prefix="/tags", tags=["tags"])  
app.include_router(lambda_routes.router)  

try:
    Base.metadata.create_all(bind=engine)  
except Exception as exc:
    print(f"Aviso: falha ao criar tabelas automaticamente: {exc}")


import pandas as pd  
from app.models.models import Empresa, Estabelecimento, Socio  
from sqlalchemy.orm import Session  
import threading



def carregar_dados_csv():
    caminho_csv = os.path.join(os.path.dirname(__file__), '../data/repasse-s.csv')
    if not os.path.exists(caminho_csv):  
        print('Arquivo CSV não encontrado:', caminho_csv)
        return
    try:
        df = pd.read_csv(caminho_csv, sep=';')  
        with Session(engine) as session:  
            for _, row in df.iterrows():  
                nome_entidade = row.get('Entidade')  
                cnpj_info = row.get('UC/CNPJ')  
                
                existing = session.query(Empresa).filter_by(nome=nome_entidade).first()
                if not existing:
                    empresa = Empresa(nome=nome_entidade, cnpj=str(cnpj_info))  
                    session.add(empresa) 
            session.commit()  
        print('Carga de dados concluída.')  
    except Exception as exc:
        print(f"Erro durante carregar_dados_csv: {exc}")



@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    print("[APP] startup event triggered")
    try:
        if os.getenv("AUTO_LOAD", "false").lower() in ("1", "true", "yes"):
            threading.Thread(target=carregar_dados_csv, daemon=True).start()
        yield
    finally:
        # shutdown
        print("[APP] shutdown event triggered")


app.router.lifespan_context = lifespan

class Config:
    orm_mode = True
    from_attributes = True

