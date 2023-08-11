FROM python:3.10.12-slim

WORKDIR /app

ENV PYTHONUNBUFFEERED 1
COPY requirements.txt /app/
COPY entrypoint.sh /app/

RUN apt-get update -y && pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . /app
