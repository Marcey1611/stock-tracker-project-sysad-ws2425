FROM python:3.12-slim

# System-Pakete installieren Quelle ChatGPT
RUN apt-get update && apt-get install -y \
    build-essential cmake ninja-build python3-dev \
    libjpeg-dev libpng-dev libtiff-dev \
    libopenblas-dev libfreetype6-dev \
    && python -m ensurepip --upgrade \
    && pip install --no-cache-dir --upgrade pip \
    && apt-get clean

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app .

CMD ["python3", "main.py"]
