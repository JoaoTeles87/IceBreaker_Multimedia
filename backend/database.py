from sqlmodel import create_engine, Session, SQLModel

# Use a variável de ambiente se disponível, senão use o padrão
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database.db")

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Função de dependência para obter a sessão do banco de dados
def get_session():
    with Session(engine) as session:
        yield session