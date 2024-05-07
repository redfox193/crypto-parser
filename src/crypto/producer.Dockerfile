FROM python:3.10-slim

WORKDIR /app

COPY producer/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY producer/ producer/
COPY shared/ producer/shared/
