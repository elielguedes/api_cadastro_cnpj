# Importa o FastAPI e componentes do projeto
from fastapi import FastAPI  # Framework principal para API RESTful
from fastapi.middleware.cors import CORSMiddleware  # Middleware CORS para produção
from app.database import Base, engine  # ORM e engine do banco de dados
from app.routers import empresas, estabelecimentos, socios, tags  # Rotas das entidades
from app.auth import router as auth_router  # Rotas de autenticação JWT
import os  # Para variáveis de ambiente

# Inicializa a aplicação FastAPI com configurações de produção
app = FastAPI(
    title="API de Empresas Brasileiras",
    description="API RESTful para consulta de dados de empresas, estabelecimentos e sócios do dados.gov.br",
    version="1.0.0",
    docs_url="/docs" if os.getenv("ENVIRONMENT") != "production" else None,  # Desabilita docs em produção
    redoc_url="/redoc" if os.getenv("ENVIRONMENT") != "production" else None  # Desabilita redoc em produção
)

# Configuração CORS para produção
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios específicos
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

# Inclui as rotas das entidades principais na aplicação
app.include_router(empresas.router, prefix="/empresas", tags=["empresas"])  # Endpoints de empresas
app.include_router(estabelecimentos.router, prefix="/estabelecimentos", tags=["estabelecimentos"])  # Endpoints de estabelecimentos
app.include_router(socios.router, prefix="/socios", tags=["socios"])  # Endpoints de sócios
app.include_router(auth_router, prefix="/auth", tags=["auth"])  # Endpoints de autenticação
app.include_router(tags.router, prefix="/tags", tags=["tags"])  # Endpoints de tags (N:N)

# Cria as tabelas no banco de dados SQLite usando SQLAlchemy
Base.metadata.create_all(bind=engine)  # Gera as tabelas conforme os modelos ORM

# Script de carga automática dos dados a partir de CSV
import pandas as pd  # Biblioteca para manipulação de dados
from app.models.models import Empresa, Estabelecimento, Socio  # Modelos ORM
from sqlalchemy.orm import Session  # Sessão para transações
import os  # Biblioteca para manipulação de arquivos
import threading

# Função para importar dados do CSV automaticamente
# Lê o arquivo repasse-s.csv e insere empresas no banco
# Pode ser adaptada para importar estabelecimentos e sócios

def carregar_dados_csv():
    caminho_csv = os.path.join(os.path.dirname(__file__), '../data/repasse-s.csv')  # Caminho do arquivo CSV
    if not os.path.exists(caminho_csv):  # Verifica se o arquivo existe
        print('Arquivo CSV não encontrado:', caminho_csv)
        return
    try:
        df = pd.read_csv(caminho_csv, sep=';')  # Lê o CSV com separador ponto e vírgula
        with Session(engine) as session:  # Abre sessão com o banco
            for _, row in df.iterrows():  # Itera sobre as linhas do CSV
                # Usa as colunas corretas do CSV
                nome_entidade = row.get('Entidade')  # Nome da entidade
                cnpj_info = row.get('UC/CNPJ')  # CNPJ ou código
                # Verifica se já existe no banco para evitar duplicatas
                existing = session.query(Empresa).filter_by(nome=nome_entidade).first()
                if not existing:
                    empresa = Empresa(nome=nome_entidade, cnpj=str(cnpj_info))  # Cria objeto Empresa
                    session.add(empresa)  # Adiciona ao banco
            session.commit()  # Salva todas as transações de uma vez
        print('Carga de dados concluída.')  # Mensagem de sucesso
    except Exception as exc:
        # Log para depuração; não relança para evitar crash do processo principal
        print(f"Erro durante carregar_dados_csv: {exc}")

# A carga automática do CSV NÃO é executada no import para evitar bloqueios
# Para ativar a importação automática ao iniciar a aplicação, defina a
# variável de ambiente AUTO_LOAD=true. A carga será executada em background
# durante o evento de startup do FastAPI.

@app.on_event("startup")
def startup_tasks():
    if os.getenv("AUTO_LOAD", "false").lower() in ("1", "true", "yes"):
        # roda em background para não bloquear o servidor
        threading.Thread(target=carregar_dados_csv, daemon=True).start()


@app.on_event("startup")
def _log_startup():
    # Log simples para diagnóstico (aparece no stdout do Uvicorn)
    try:
        print("[APP] startup event triggered")
    except Exception:
        pass


@app.on_event("shutdown")
def _log_shutdown():
    try:
        print("[APP] shutdown event triggered")
    except Exception:
        pass

class Config:
    orm_mode = True
    from_attributes = True

