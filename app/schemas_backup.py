"""Pydantic schemas used by the API.

Set configuration depending on Pydantic major version to remain compatible
with both v1 and v2 (avoid declaring both `Config` and `model_config`).
"""

from __future__ import annotations
from typing import Optional, List
import pydantic
from pydantic import BaseModel

PYDANTIC_V2 = int(pydantic.VERSION.split(".")[0]) >= 2


# ---------------------- BaseModel compatível v1/v2 ----------------------
class BaseSchema(BaseModel):
    if PYDANTIC_V2:
        model_config = {"from_attributes": True}
    else:
        class Config:
            orm_mode = True
            from_attributes = True


# ---------------------- Usuario (auth) ----------------------
class UsuarioBase(BaseSchema):
    username: str
    is_admin: bool = False


class UsuarioCreate(UsuarioBase):
    password: str


class Usuario(UsuarioBase):
    id: int


# ---------------------- Socio ----------------------
class SocioBase(BaseSchema):
    nome: str
    estabelecimento_id: int


class SocioCreate(SocioBase):
    pass


class Socio(SocioBase):
    id: int


# ---------------------- Estabelecimento ----------------------
class EstabelecimentoBase(BaseSchema):
    nome: str
    empresa_id: int


class EstabelecimentoCreate(EstabelecimentoBase):
    pass


class Estabelecimento(EstabelecimentoBase):
    id: int


# ---------------------- Empresa ----------------------
class EmpresaBase(BaseSchema):
    nome: str
    cnpj: str


class EmpresaCreate(EmpresaBase):
    pass


class Empresa(EmpresaBase):
    id: int


# ---------------------- Tag (N:N with Empresa) ----------------------
class TagBase(BaseSchema):
    name: str


class TagCreate(TagBase):
    pass


class Tag(TagBase):
    id: int


# ---------------------- Empresa read (with tags) ----------------------
class EmpresaRead(Empresa):
    tags: List[Tag] = []
