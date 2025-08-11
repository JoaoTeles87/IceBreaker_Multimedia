from sqlmodel import create_engine, SQLModel
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./icebreaker.db")

# Cria o engine do banco de dados
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    """Cria as tabelas do banco de dados"""
    SQLModel.metadata.create_all(engine)

def get_engine():
    """Retorna o engine do banco de dados"""
    return engine 