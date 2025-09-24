from pydantic import BaseModel

# Schemas de Usuário para autenticação JWT
class UsuarioBase(BaseModel):
    username: str
    is_admin: bool = False

class UsuarioCreate(UsuarioBase):
    password: str

class Usuario(UsuarioBase):
    id: int
    class Config:
        from_attributes = True
class SocioBase(BaseModel):
    nome: str
    estabelecimento_id: int

class SocioCreate(SocioBase):
    pass

class Socio(SocioBase):
    id: int
    class Config:
        from_attributes = True
from pydantic import BaseModel

class EstabelecimentoBase(BaseModel):
    nome: str
    empresa_id: int

class EstabelecimentoCreate(EstabelecimentoBase):
    pass

class Estabelecimento(EstabelecimentoBase):
    id: int
    class Config:
        from_attributes = True

class EmpresaBase(BaseModel):
    nome: str
    cnpj: str

class EmpresaCreate(EmpresaBase):
    pass

class Empresa(EmpresaBase):
    id: int
    class Config:
        from_attributes = True
