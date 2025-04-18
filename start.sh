#!/bin/bash
set -e

echo "⏳ Waiting for PostgreSQL..."
until pg_isready -h db -p 5432 -U "$POSTGRES_USER"; do
    sleep 1
done

echo "🚀 Running migrations..."
alembic upgrade head

echo "🔧 Starting API server..."
exec uvicorn main:app --host 0.0.0.0 --port 8443 --reload
