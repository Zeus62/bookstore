FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y openssl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 3000

CMD ["gunicorn", "-b", "0.0.0.0:3000", "app:app"]