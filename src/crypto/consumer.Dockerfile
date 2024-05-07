FROM python:3.10-slim

WORKDIR /app

COPY consumer/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY consumer/ consumer/
COPY shared/ consumer/shared/
