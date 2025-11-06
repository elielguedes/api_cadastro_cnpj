from __future__ import annotations
from typing import List
import pydantic
from pydantic import BaseModel

PYDANTIC_V2 = int(pydantic.VERSION.split(".")[0]) >= 2

def orm_model(cls):
    """Decorador para ajustar orm_mode dependendo da versão do Pydantic"""
    if PYDANTIC_V2:
        cls.model_config = {"from_attributes": True}
    else:
        class _Config:
            orm_mode = True
            from_attributes = True
        cls.Config = _Config
    return cls


# ---------------------- Usuario ----------------------
class UsuarioBase(BaseModel):
    username: str
    is_admin: bool = False


class UsuarioCreate(UsuarioBase):
    password: str


@orm_model
class Usuario(UsuarioBase):
    id: int


# ---------------------- Socio ----------------------
class SocioBase(BaseModel):
    nome: str
    estabelecimento_id: int


class SocioCreate(SocioBase):
    pass


@orm_model
class Socio(SocioBase):
    id: int


# ---------------------- Estabelecimento ----------------------
class EstabelecimentoBase(BaseModel):
    nome: str
    empresa_id: int


class EstabelecimentoCreate(EstabelecimentoBase):
    pass


@orm_model
class Estabelecimento(EstabelecimentoBase):
    id: int


# ---------------------- Empresa ----------------------
class EmpresaBase(BaseModel):
    nome: str
    cnpj: str


class EmpresaCreate(EmpresaBase):
    pass


@orm_model
class Empresa(EmpresaBase):
    id: int


# ---------------------- Tag ----------------------
class TagBase(BaseModel):
    name: str


class TagCreate(TagBase):
    pass


@orm_model
class Tag(TagBase):
    id: int


# ---------------------- Empresa read (with tags) ----------------------
@orm_model
class EmpresaRead(Empresa):
    tags: List[Tag] = []
