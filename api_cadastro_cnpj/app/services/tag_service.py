from app.models.models import Tag, Empresa, empresa_tags
from app.schemas import TagCreate


def create_tag(db, tag: TagCreate):
    db_tag = Tag(name=tag.name)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


def get_tags(db, skip: int = 0, limit: int = 10):
    return db.query(Tag).offset(skip).limit(limit).all()


def get_tag(db, tag_id: int):
    return db.query(Tag).filter(Tag.id == tag_id).first()


def delete_tag(db, tag_id: int):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if tag is None:
        return False
    db.delete(tag)
    db.commit()
    return True


def add_tag_to_empresa(db, empresa_id: int, tag_id: int):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not empresa or not tag:
        return False
    empresa.tags.append(tag)
    db.commit()
    return True


def remove_tag_from_empresa(db, empresa_id: int, tag_id: int):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not empresa or not tag:
        return False
    if tag in empresa.tags:
        empresa.tags.remove(tag)
        db.commit()
    return True
