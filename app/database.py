from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER", "user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "12345")
POSTGRES_DB = os.getenv("POSTGRES_DB", "exampledb")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "db")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_async_engine(
    DATABASE_URL,
    echo=os.getenv("SQLALCHEMY_ECHO", "True") == "True",
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=40,
    pool_timeout=60,
    pool_recycle=1800
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()

async def create_tables():
    """Cria todas as tabelas definidas nos modelos"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db() -> AsyncSession:
    """Fornece uma sessão de banco de dados para os endpoints FastAPI"""
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
