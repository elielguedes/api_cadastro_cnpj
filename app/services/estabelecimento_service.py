
#Serviço para operações de negócio relacionadas aos Estabelecimentos.

#Este módulo implementa a lógica de negócio para operações CRUD de estabelecimentos,
#que representam as filiais, matriz ou unidades de uma empresa.

#Relacionamento: Estabelecimento pertence a uma Empresa (N:1)
#- Cada estabelecimento está vinculado a uma empresa via empresa_id
#- Uma empresa pode ter múltiplos estabelecimentos

#Funções disponíveis:
#- create_estabelecimento_service: Criar novo estabelecimento
#- get_estabelecimentos_service: Listar estabelecimentos com paginação
#- get_estabelecimento_service: Buscar estabelecimento específico por ID
#- delete_estabelecimento_service: Remover estabelecimento do sistema


from fastapi import HTTPException
from app.models.models import Estabelecimento, Empresa
from app.schemas import EstabelecimentoCreate

def create_estabelecimento_service(db, estabelecimento: EstabelecimentoCreate):
    """
    Cria um novo estabelecimento vinculado a uma empresa.
    
    Args:
        db: Sessão do banco de dados SQLAlchemy
        estabelecimento: Dados do estabelecimento validados pelo schema Pydantic
        
    Returns:
        Estabelecimento: Objeto do estabelecimento criado com ID gerado
        
    Note:
        O estabelecimento deve estar vinculado a uma empresa existente via empresa_id
    """
    # valida se a empresa referenciada existe
    empresa = db.query(Empresa).filter(Empresa.id == estabelecimento.empresa_id).first()
    if empresa is None:
        raise HTTPException(status_code=400, detail="Empresa referenciada não existe")

    db_estabelecimento = Estabelecimento(
        nome=estabelecimento.nome,
        empresa_id=estabelecimento.empresa_id
    )
    db.add(db_estabelecimento)      # Adiciona à sessão
    db.commit()                     # Persiste no banco
    db.refresh(db_estabelecimento)  # Atualiza objeto com dados do banco (ID)
    return db_estabelecimento

def get_estabelecimentos_service(db, skip: int = 0, limit: int = 10):
    """
    Lista estabelecimentos com suporte a paginação.
    
    Args:
        db: Sessão do banco de dados SQLAlchemy
        skip: Número de registros para pular (offset)
        limit: Número máximo de registros para retornar
        
    Returns:
        List[Estabelecimento]: Lista de estabelecimentos encontrados
    """
    return db.query(Estabelecimento).offset(skip).limit(limit).all()

def get_estabelecimento_service(db, estabelecimento_id: int):
    """
    Busca um estabelecimento específico pelo ID.
    
    Args:
        db: Sessão do banco de dados SQLAlchemy
        estabelecimento_id: ID único do estabelecimento
        
    Returns:
        Estabelecimento or None: Objeto do estabelecimento ou None se não encontrado
    """
    return db.query(Estabelecimento).filter(Estabelecimento.id == estabelecimento_id).first()

def delete_estabelecimento_service(db, estabelecimento_id: int):
    """
    Remove um estabelecimento do banco de dados.
    
    Args:
        db: Sessão do banco de dados SQLAlchemy
        estabelecimento_id: ID único do estabelecimento a ser removido
        
    Returns:
        bool: True se removido com sucesso, False se não encontrado
        
    Note:
        Esta operação não afeta a empresa à qual o estabelecimento pertencia
    """
    estabelecimento = db.query(Estabelecimento).filter(Estabelecimento.id == estabelecimento_id).first()
    if estabelecimento is None:
        return False  # Estabelecimento não encontrado
    
    db.delete(estabelecimento)  # Marca para exclusão
    db.commit()                 # Confirma a exclusão
    return True


def update_estabelecimento_service(db, estabelecimento_id: int, payload):
    """Atualiza um estabelecimento existente (parcial).

    O payload deve conter somente os campos a atualizar. Retorna o objeto atualizado ou None se não existir.
    """
    # import here to avoid circular import if payload type isn't strictly enforced
    from app.models.models import Estabelecimento as EstModel

    est = db.query(EstModel).filter(EstModel.id == estabelecimento_id).first()
    if est is None:
        return None

    if hasattr(payload, "nome") and payload.nome is not None:
        est.nome = payload.nome
    if hasattr(payload, "empresa_id") and payload.empresa_id is not None:
        empresa = db.query(Empresa).filter(Empresa.id == payload.empresa_id).first()
        if empresa is None:
            raise HTTPException(status_code=400, detail="Empresa referenciada não existe")
        est.empresa_id = payload.empresa_id

    db.add(est)
    db.commit()
    db.refresh(est)
    return est
