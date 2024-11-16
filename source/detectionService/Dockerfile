FROM python:3.11

RUN python -m ensurepip --upgrade
RUN pip install --no-cache-dir --upgrade pip

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# FastAPI-Anwendung starten
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]