# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Lade Umgebungsvariablen aus .env-Datei
load_dotenv()

# Lade Umgebungsvariable 'DATABASE_URL'
DATABASE_URL = os.getenv("DATABASE_URL")

# Setze SQLAlchemy-Engine und Session
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)