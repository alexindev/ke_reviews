FROM python:3.10.12-slim
WORKDIR /app
COPY requirements.txt .
RUN apt update && apt upgrade -y && apt install curl -y && pip install --no-cache-dir -r requirements.txt
COPY . .
