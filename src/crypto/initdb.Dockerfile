FROM python:3.10-slim

WORKDIR /app

COPY consumer/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY consumer/database database/
COPY consumer/migration migration/
COPY consumer/alembic.ini .