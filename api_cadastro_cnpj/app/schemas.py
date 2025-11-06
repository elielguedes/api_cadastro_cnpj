"""Pydantic schemas used by the API."""

from typing import List
from pydantic import BaseModel, ConfigDict


# ---------------------- Usuario (auth) ----------------------
class UsuarioBase(BaseModel):
    username: str
    is_admin: bool = False


class UsuarioCreate(UsuarioBase):
    password: str


class Usuario(UsuarioBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# ---------------------- Socio ----------------------
class SocioBase(BaseModel):
    nome: str
    estabelecimento_id: int


class SocioCreate(SocioBase):
    pass


class Socio(SocioBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# ---------------------- Estabelecimento ----------------------
class EstabelecimentoBase(BaseModel):
    nome: str
    empresa_id: int


class EstabelecimentoCreate(EstabelecimentoBase):
    pass


class Estabelecimento(EstabelecimentoBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# ---------------------- Empresa ----------------------
class EmpresaBase(BaseModel):
    nome: str
    cnpj: str


class EmpresaCreate(EmpresaBase):
    pass


class Empresa(EmpresaBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# ---------------------- Tag (N:N with Empresa) ----------------------
class TagBase(BaseModel):
    name: str


class TagCreate(TagBase):
    pass


class Tag(TagBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# ---------------------- Empresa read (with tags) ----------------------
class EmpresaRead(Empresa):
    tags: List[Tag] = []
    model_config = ConfigDict(from_attributes=True)
