import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Usa DATABASE_URL se definida (ex: postgresql+psycopg2://user:pass@host:port/db)
DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL:
	# Conexão para Postgres (ou outra DB especificada na URL)
	engine = create_engine(DATABASE_URL)
	SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
else:
	# Fallback para SQLite local (prático para desenvolvimento sem Docker)
	SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"
	engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
	SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
