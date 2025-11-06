import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Usa DATABASE_URL se definida (ex: postgresql+psycopg2://user:pass@host:port/db)
DATABASE_URL = os.getenv('DATABASE_URL')

# Ajustes úteis:
# - Heroku pode fornecer 'postgres://' em vez de 'postgresql://'; o SQLAlchemy
#   espera 'postgresql://', então corrigimos automaticamente.
# - Habilitamos pool_pre_ping para evitar conexões mortas em pools.
# - SQL_ECHO=true ativa echo do SQL para depuração.
if DATABASE_URL:
	# Corrige URL do Heroku (postgres:// -> postgresql://)
	if DATABASE_URL.startswith('postgres://'):
		DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

	echo = os.getenv('SQL_ECHO', 'false').lower() in ('1', 'true', 'yes')
	engine = create_engine(DATABASE_URL, echo=echo, pool_pre_ping=True)
	SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
else:
	# Fallback para SQLite local (prático para desenvolvimento sem Docker)
	SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"
	engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
	SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
