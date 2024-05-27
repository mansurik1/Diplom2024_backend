FROM python:3.10-slim-bookworm

WORKDIR /chat-bot

COPY requirements.txt .
COPY config-example.yaml ./config.yaml

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python", "./main.py"]
