from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Configurações do banco de dados
POSTGRES_USER = os.getenv("POSTGRES_USER", "user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "12345")
POSTGRES_DB = os.getenv("POSTGRES_DB", "exampledb")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "db")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

# String de conexão para o SQLAlchemy
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Configurações do engine do SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    echo=os.getenv("SQLALCHEMY_ECHO", "True") == "True",
    pool_pre_ping=True,  # Verifica a conexão antes de usá-la
    pool_size=10,  # Número máximo de conexões no pool
    max_overflow=20,  # Número máximo de conexões que podem ser criadas além do pool_size
    pool_timeout=30  # Timeout de espera por uma conexão do pool
)

# Sessão para consultas no banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos ORM
Base = declarative_base()

# Função para criar tabelas
def create_tables():
    """Cria todas as tabelas definidas nos modelos"""
    from app.models.patient import Patient
    Base.metadata.create_all(bind=engine)

# Dependência para uso nos endpoints FastAPI
def get_db():
    """Fornece uma sessão de banco de dados para os endpoints FastAPI"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Função para criar todas as tabelas definidas nos modelos
def create_tables():
    """Cria todas as tabelas no banco de dados"""
    Base.metadata.create_all(bind=engine)
