from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import TagCreate, Tag
from app.deps import get_db, require_admin
from app.services.tag_service import (
    create_tag,
    get_tags,
    get_tag,
    delete_tag,
    add_tag_to_empresa,
    remove_tag_from_empresa,
)

router = APIRouter()

@router.post('/', response_model=Tag)
def create_tag_route(tag: TagCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    return create_tag(db, tag)

@router.get('/', response_model=list[Tag])
def list_tags(db: Session = Depends(get_db)):
    return get_tags(db)

@router.get('/{tag_id}', response_model=Tag)
def read_tag(tag_id: int, db: Session = Depends(get_db)):
    tag = get_tag(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail='Tag not found')
    return tag

@router.delete('/{tag_id}')
def delete_tag_route(tag_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    ok = delete_tag(db, tag_id)
    if not ok:
        raise HTTPException(status_code=404, detail='Tag not found')
    return {'ok': True}

@router.post('/{tag_id}/empresas/{empresa_id}')
def add_tag(tag_id: int, empresa_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    ok = add_tag_to_empresa(db, empresa_id, tag_id)
    if not ok:
        raise HTTPException(status_code=404, detail='Empresa or Tag not found')
    return {'ok': True}

@router.delete('/{tag_id}/empresas/{empresa_id}')
def remove_tag(tag_id: int, empresa_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    ok = remove_tag_from_empresa(db, empresa_id, tag_id)
    if not ok:
        raise HTTPException(status_code=404, detail='Empresa or Tag not found')
    return {'ok': True}
