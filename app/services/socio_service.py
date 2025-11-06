

from fastapi import HTTPException
from app.models.models import Socio, Estabelecimento
from app.schemas import SocioCreate, SocioUpdate

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
    # valida se o estabelecimento referenciado existe
    est = db.query(Estabelecimento).filter(Estabelecimento.id == socio.estabelecimento_id).first()
    if est is None:
        raise HTTPException(status_code=400, detail="Estabelecimento referenciado não existe")

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
        Socio or None: Objeto do sócio ou None se não encontrado
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


def update_socio_service(db, socio_id: int, payload: SocioUpdate):
    """Atualiza um sócio existente com os campos fornecidos (parciais).

    Retorna o objeto atualizado ou None se não existir.
    """
    socio = db.query(Socio).filter(Socio.id == socio_id).first()
    if socio is None:
        return None

    # Atualiza somente os campos presentes (não-None)
    if payload.nome is not None:
        socio.nome = payload.nome
    if payload.estabelecimento_id is not None:
        # valida se o estabelecimento existe
        est = db.query(Estabelecimento).filter(Estabelecimento.id == payload.estabelecimento_id).first()
        if est is None:
            raise HTTPException(status_code=400, detail="Estabelecimento referenciado não existe")
        socio.estabelecimento_id = payload.estabelecimento_id

    db.add(socio)
    db.commit()
    db.refresh(socio)
    return socio
