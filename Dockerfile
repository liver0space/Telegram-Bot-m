FROM python:3.11-slim

ENV BOT_NAME=telegram_bot

WORKDIR /usr/src/app/${BOT_NAME}

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt 

COPY . /usr/src/app/${BOT_NAME}