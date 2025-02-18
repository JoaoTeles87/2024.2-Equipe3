from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define a URL do banco de dados SQLite (pode ser outro banco se precisar)
DATABASE_URL = "sqlite:///./app.db"

# Cria o engine do banco de dados
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Cria a sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para ser herdada pelas classes do ORM
Base = declarative_base()
