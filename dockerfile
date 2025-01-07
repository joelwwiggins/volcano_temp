FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    libgpiod2 \
    python3-dev \
    gcc \
    python3-rpi.gpio \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["python", "app.py"]

