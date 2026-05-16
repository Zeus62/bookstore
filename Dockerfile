FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y openssl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 3000

# Generate a self-signed certificate and run gunicorn with it
CMD openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365 -subj "/CN=localhost" && \
    gunicorn -b 0.0.0.0:3000 --certfile=cert.pem --keyfile=key.pem app:app