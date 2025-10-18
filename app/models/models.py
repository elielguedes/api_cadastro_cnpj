from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy import Table, Column, Integer, ForeignKey

# Association table for Empresa <-> Tag (N:N)
empresa_tags = Table(
    'empresa_tags',
    Base.metadata,
    Column('empresa_id', Integer, ForeignKey('empresas.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False)

class Empresa(Base):
    __tablename__ = "empresas"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    cnpj = Column(String, index=True, unique=True)
    estabelecimentos = relationship("Estabelecimento", back_populates="empresa")
    tags = relationship("Tag", secondary=empresa_tags, back_populates="empresas")

class Estabelecimento(Base):
    __tablename__ = "estabelecimentos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    empresa_id = Column(Integer, ForeignKey("empresas.id"))
    empresa = relationship("Empresa", back_populates="estabelecimentos")
    socios = relationship("Socio", back_populates="estabelecimento")

class Socio(Base):
    __tablename__ = "socios"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    estabelecimento_id = Column(Integer, ForeignKey("estabelecimentos.id"))
    estabelecimento = relationship("Estabelecimento", back_populates="socios")


class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    empresas = relationship('Empresa', secondary=empresa_tags, back_populates='tags')

# Sample data
empresa_sample = {
  "nome": "PETROBRAS",
  "cnpj": "12.345.678/00001-99"
}