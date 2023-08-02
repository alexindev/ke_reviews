FROM python:3.10.12-slim

WORKDIR /app

COPY requirements.txt /app/

RUN apt-get update && apt-get install -y netcat-openbsd && apt-get clean

RUN pip install -r requirements.txt

COPY . /app