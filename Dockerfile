FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y openssl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

RUN openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365 -subj "/CN=localhost"

EXPOSE 3000

CMD ["gunicorn", "--certfile=cert.pem", "--keyfile=key.pem", "-b", "0.0.0.0:3000", "app:app"]