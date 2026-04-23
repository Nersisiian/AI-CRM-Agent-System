#!/bin/bash
set -e
echo "Waiting for Postgres..."; while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do sleep 0.5; done
echo "Waiting for Redis..."; while ! nc -z $REDIS_HOST $REDIS_PORT; do sleep 0.5; done
python scripts/init_db.py
python scripts/seed_data.py
exec uvicorn main:app --host 0.0.0.0 --port 8000