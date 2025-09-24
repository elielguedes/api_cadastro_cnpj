from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

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
    cnpj = Column(String, index=True)
    estabelecimentos = relationship("Estabelecimento", back_populates="empresa")

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

# Sample data
empresa_sample = {
  "nome": "PETROBRAS",
  "cnpj": "12.345.678/00001-99"
}