"""Pydantic schemas used by the API.

Set configuration depending on Pydantic major version to remain compatible
with both v1 and v2 (avoid declaring both `Config` and `model_config`).
"""

from __future__ import annotations

from typing import Optional, List, Union
import pydantic
from pydantic import BaseModel

PYDANTIC_V2 = int(pydantic.VERSION.split(".")[0]) >= 2


# ---------------------- Usuario (auth) ----------------------
class UsuarioBase(BaseModel):
    username: str
    is_admin: bool = False


class UsuarioCreate(UsuarioBase):
    password: str


class Usuario(UsuarioBase):
    id: int


if PYDANTIC_V2:
    Usuario.model_config = {"from_attributes": True}
else:
    class _UsuarioConfig:
        orm_mode = True
        from_attributes = True

    Usuario.Config = _UsuarioConfig


# ---------------------- Socio ----------------------
class SocioBase(BaseModel):
    nome: str
    estabelecimento_id: int


class SocioCreate(SocioBase):
    pass


class Socio(SocioBase):
    id: int


if PYDANTIC_V2:
    Socio.model_config = {"from_attributes": True}
else:
    class _SocioConfig:
        orm_mode = True
        from_attributes = True

    Socio.Config = _SocioConfig


# ---------------------- Estabelecimento ----------------------
class EstabelecimentoBase(BaseModel):
    nome: str
    empresa_id: int


class EstabelecimentoCreate(EstabelecimentoBase):
    pass


class Estabelecimento(EstabelecimentoBase):
    id: int


if PYDANTIC_V2:
    Estabelecimento.model_config = {"from_attributes": True}
else:
    class _EstabelecimentoConfig:
        orm_mode = True
        from_attributes = True

    Estabelecimento.Config = _EstabelecimentoConfig


# ---------------------- Empresa ----------------------
class EmpresaBase(BaseModel):
    nome: str
    cnpj: str


class EmpresaCreate(EmpresaBase):
    pass


class Empresa(EmpresaBase):
    id: int


if PYDANTIC_V2:
    Empresa.model_config = {"from_attributes": True}
else:
    class _EmpresaConfig:
        orm_mode = True
        from_attributes = True

    Empresa.Config = _EmpresaConfig


# ---------------------- Tag (N:N with Empresa) ----------------------
class TagBase(BaseModel):
    name: str


class TagCreate(TagBase):
    pass


if PYDANTIC_V2:
    class Tag(TagBase):
        id: int
        model_config = {"from_attributes": True}
else:
    class Tag(TagBase):
        id: int
        
        class Config:
            orm_mode = True
            from_attributes = True


# ---------------------- Empresa read (with tags) ----------------------
class EmpresaRead(Empresa):
    tags: List[Tag] = []


if PYDANTIC_V2:
    EmpresaRead.model_config = {"from_attributes": True}
else:
    class _EmpresaReadConfig:
        orm_mode = True
        from_attributes = True

    EmpresaRead.Config = _EmpresaReadConfig
