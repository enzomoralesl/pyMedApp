import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from logging.config import fileConfig
import time

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy import create_engine

from alembic import context

# Import models to ensure they are registered with Base.metadata
from app.database import Base
from app.models.patient import Patient

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name:
    fileConfig(config.config_file_name)

# Set target metadata
target_metadata = Base.metadata

# Get URL from environment variables
def get_url():
    user = os.environ.get("POSTGRES_USER", "user")
    password = os.environ.get("POSTGRES_PASSWORD", "12345")
    host = os.environ.get("POSTGRES_HOST", "db")
    port = os.environ.get("POSTGRES_PORT", "5432")
    db = os.environ.get("POSTGRES_DB", "pyexampledb")
    return f"postgresql://{user}:{password}@{host}:{port}/{db}"

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    # Wait for database to be ready
    max_retries = 10
    retries = 0
    
    while retries < max_retries:
        try:
            url = get_url()
            # Test connection
            engine = create_engine(url)
            connection = engine.connect()
            connection.close()
            break
        except Exception as e:
            retries += 1
            print(f"Database connection failed (attempt {retries}/{max_retries}): {e}")
            if retries < max_retries:
                print("Waiting 2 seconds...")
                time.sleep(2)
            else:
                print("Max retries reached, giving up.")
                raise

    # Configure Alembic
    configuration = config.get_section(config.config_ini_section)
    if not configuration:
        configuration = {}
    configuration["sqlalchemy.url"] = get_url()
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        echo=True
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
