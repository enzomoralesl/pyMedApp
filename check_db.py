#!/usr/bin/env python
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
import time

# Carrega variáveis de ambiente
load_dotenv()

# Configurações do banco de dados
POSTGRES_USER = os.getenv("POSTGRES_USER", "user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "12345")
POSTGRES_DB = os.getenv("POSTGRES_DB", "pyexampledb")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "db")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

# String de conexão para o SQLAlchemy
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

def check_database():
    """Verifica a conexão com o banco de dados"""
    
    print(f"Tentando conectar em: {DATABASE_URL}")
    
    max_attempts = 5
    for attempt in range(max_attempts):
        try:
            # Tenta criar uma conexão
            engine = create_engine(DATABASE_URL)
            with engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                version = connection.execute(text("SELECT version()"))
                
                print("✅ Conexão com o banco de dados estabelecida com sucesso!")
                print(f"Versão PostgreSQL: {version.fetchone()[0]}")
                
                # Verifica as tabelas
                tables = connection.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema='public'
                """))
                
                print("\nTabelas existentes:")
                for table in tables:
                    print(f"- {table[0]}")
                    
                    # Conta registros
                    count = connection.execute(text(f"SELECT COUNT(*) FROM {table[0]}"))
                    print(f"  Registros: {count.fetchone()[0]}")
                
            return True
        except Exception as e:
            print(f"❌ Erro de conexão (tentativa {attempt + 1}/{max_attempts}):")
            print(f"  {str(e)}")
            if attempt < max_attempts - 1:
                print("Tentando novamente em 2 segundos...")
                time.sleep(2)
    
    print("❌ Falha ao conectar ao banco de dados após várias tentativas.")
    return False

if __name__ == "__main__":
    print("Verificador de conexão com o banco de dados")
    print("------------------------------------------")
    check_database()
