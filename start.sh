#!/bin/bash
set -e

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
until PGPASSWORD=$POSTGRES_PASSWORD psql -h $POSTGRES_HOST -U $POSTGRES_USER -d $POSTGRES_DB -c '\q'; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 2
done
echo "PostgreSQL is up - executing command"

# List tables to check if they exist
echo "Checking if tables exist..."
tables=$(PGPASSWORD=$POSTGRES_PASSWORD psql -h $POSTGRES_HOST -U $POSTGRES_USER -d $POSTGRES_DB -t -c '\dt' | grep -c 'tb_')

if [ "$tables" -eq "0" ]; then
  echo "No tables found. Running initialization SQL..."
  PGPASSWORD=$POSTGRES_PASSWORD psql -h $POSTGRES_HOST -U $POSTGRES_USER -d $POSTGRES_DB -f /app/init.sql
  echo "Database initialized with tables."
else
  echo "Tables already exist. Skipping initialization."
fi

# Initialize database tables using SQLAlchemy models
echo "Setting up SQLAlchemy models..."
python -c "import asyncio; from app.database import create_tables; asyncio.run(create_tables())"
echo "Database setup completed."

# Start the application
echo "Starting FastAPI application with Gunicorn..."
exec gunicorn main:app --workers 5 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8081
