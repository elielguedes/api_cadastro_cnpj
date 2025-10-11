"""
Serviço para operações de negócio relacionadas aos Sócios.

Este módulo implementa a lógica de negócio para operações CRUD de sócios,
que representam as pessoas físicas ou jurídicas que possuem participação nas empresas.

Relacionamento: Socio pertence a um Estabelecimento (N:1)
- Cada sócio está vinculado a um estabelecimento via estabelecimento_id
- Um estabelecimento pode ter múltiplos sócios
- Indiretamente, sócios estão relacionados às empresas através dos estabelecimentos

Funções disponíveis:
- create_socio_service: Criar novo sócio
- get_socios_service: Listar sócios com paginação
- get_socio_service: Buscar sócio específico por ID
- delete_socio_service: Remover sócio do sistema
"""

from app.models.models import Socio
from app.schemas import SocioCreate

def create_socio_service(db, socio: SocioCreate):
    """
    Cria um novo sócio vinculado a um estabelecimento.
    
    Args:
        db: Sessão do banco de dados SQLAlchemy
        socio: Dados do sócio validados pelo schema Pydantic
        
    Returns:
        Socio: Objeto do sócio criado com ID gerado
        
    Note:
        O sócio deve estar vinculado a um estabelecimento existente via estabelecimento_id
    """
    db_socio = Socio(
        nome=socio.nome, 
        estabelecimento_id=socio.estabelecimento_id
    )
    db.add(db_socio)        # Adiciona à sessão
    db.commit()             # Persiste no banco
    db.refresh(db_socio)    # Atualiza objeto com dados do banco (ID)
    return db_socio

def get_socios_service(db, skip: int = 0, limit: int = 10):
    """
    Lista sócios com suporte a paginação.
    
    Args:
        db: Sessão do banco de dados SQLAlchemy
        skip: Número de registros para pular (offset)
        limit: Número máximo de registros para retornar
        
    Returns:
        List[Socio]: Lista de sócios encontrados
    """
    return db.query(Socio).offset(skip).limit(limit).all()

def get_socio_service(db, socio_id: int):
    """
    Busca um sócio específico pelo ID.
    
    Args:
        db: Sessão do banco de dados SQLAlchemy
        socio_id: ID único do sócio
        
    Returns:
        Socio | None: Objeto do sócio ou None se não encontrado
    """
    return db.query(Socio).filter(Socio.id == socio_id).first()

def delete_socio_service(db, socio_id: int):
    """
    Remove um sócio do banco de dados.
    
    Args:
        db: Sessão do banco de dados SQLAlchemy
        socio_id: ID único do sócio a ser removido
        
    Returns:
        bool: True se removido com sucesso, False se não encontrado
        
    Note:
        Esta operação não afeta o estabelecimento ao qual o sócio pertencia
    """
    socio = db.query(Socio).filter(Socio.id == socio_id).first()
    if socio is None:
        return False  # Sócio não encontrado
    
    db.delete(socio)  # Marca para exclusão
    db.commit()       # Confirma a exclusão
    return True
