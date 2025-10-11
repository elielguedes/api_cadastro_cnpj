"""
Serviço para operações de negócio relacionadas às Empresas.

Este módulo implementa a lógica de negócio para operações CRUD de empresas,
abstraindo as operações de banco de dados dos endpoints da API.

Funções disponíveis:
- create_empresa_service: Criar nova empresa
- get_empresas_service: Listar empresas com paginação
- get_empresa_service: Buscar empresa específica por ID
- delete_empresa_service: Remover empresa do sistema

Padrão utilizado: Service Layer
- Separa lógica de negócio dos controllers (routers)
- Facilita testes unitários
- Permite reutilização de código
"""

from app.models.models import Empresa
from app.schemas import EmpresaCreate
from app.utils import normalize_cnpj

def create_empresa_service(db, empresa: EmpresaCreate):
    """
    Cria uma nova empresa no banco de dados.
    
    Args:
        db: Sessão do banco de dados SQLAlchemy
        empresa: Dados da empresa validados pelo schema Pydantic
        
    Returns:
        Empresa: Objeto da empresa criada com ID gerado
    """
    # normaliza o CNPJ antes de salvar
    db_empresa = Empresa(nome=empresa.nome, cnpj=normalize_cnpj(empresa.cnpj))
    db.add(db_empresa)  # Adiciona à sessão
    db.commit()         # Persiste no banco
    db.refresh(db_empresa)  # Atualiza objeto com dados do banco (ID)
    return db_empresa

def get_empresas_service(db, skip: int = 0, limit: int = 10):
    """
    Lista empresas com suporte a paginação.
    
    Args:
        db: Sessão do banco de dados SQLAlchemy
        skip: Número de registros para pular (offset)
        limit: Número máximo de registros para retornar
        
    Returns:
        List[Empresa]: Lista de empresas encontradas
    """
    return db.query(Empresa).offset(skip).limit(limit).all()

def get_empresa_service(db, empresa_id: int):
    """
    Busca uma empresa específica pelo ID.
    
    Args:
        db: Sessão do banco de dados SQLAlchemy
        empresa_id: ID único da empresa
        
    Returns:
        Empresa | None: Objeto da empresa ou None se não encontrada
    """
    return db.query(Empresa).filter(Empresa.id == empresa_id).first()

def delete_empresa_service(db, empresa_id: int):
    """
    Remove uma empresa do banco de dados.
    
    Args:
        db: Sessão do banco de dados SQLAlchemy
        empresa_id: ID único da empresa a ser removida
        
    Returns:
        bool: True se removida com sucesso, False se não encontrada
    """
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if empresa is None:
        return False  # Empresa não encontrada
    
    db.delete(empresa)  # Marca para exclusão
    db.commit()         # Confirma a exclusão
    return True