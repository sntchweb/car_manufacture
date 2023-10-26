FROM python:3.9-alpine3.16

WORKDIR /app

COPY requirements.txt .

COPY . .

EXPOSE 8000

RUN pip install -r requirements.txt --no-cache-dir
