# Verwende ein Python-Basis-Image
FROM python:3.11

# pip aktualisieren, um sicherzustellen, dass es auf dem neuesten Stand ist
RUN python -m ensurepip --upgrade
RUN pip install --no-cache-dir --upgrade pip

# Arbeitsverzeichnis erstellen
WORKDIR /app

# Anforderungen kopieren und installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Anwendungscode kopieren
COPY . .

# FastAPI-Anwendung starten
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]