FROM python:3.6

RUN apt update && apt install -y awscli

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt