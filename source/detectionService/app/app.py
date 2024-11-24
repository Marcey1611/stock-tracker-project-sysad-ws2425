from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# Datenbankverbindung
DATABASE_URL = "postgresql://myuser:mypassword@localhost:5432/mydatabase"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# FastAPI-Anwendung
app = FastAPI()

# Datenbankmodelle
class Product(Base):
    __tablename__ = "products"
    ProductId = Column(Integer, primary_key=True, index=True)
    ProductName = Column(String, nullable=False)

    # Beziehung zur Status-Tabelle
    statuses = relationship("ProductRegalStatus", back_populates="product")


class ProductRegalStatus(Base):
    __tablename__ = "stockLog"
    product_id = Column(Integer, ForeignKey("products.id"), primary_key=True, index=True, nullable=False)
    SystemTimeIN = Column(DateTime, nullable=False) # ,default=datetime.utcnow // ist nicht mehr das aktuelle
    SystemTimeOUT = Column(DateTime, nullable=True)

    # Beziehung zum Produkt
    product = relationship("Product", back_populates="statuses")

# Datenbanktabellen erstellen (bei Bedarf)
Base.metadata.create_all(bind=engine)

# Pydantic-Schema für Validierung
class ProductDetectionSchema(BaseModel):
    product_id: int
    detected_in_regal: bool

    class Config:
        orm_mode = True     # konvertierung von SQLAlchemy in Pydantic-Modelle 

# Lebensdauer db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# REST-Endpunkt
@app.post("/detect", response_model=dict)
def detect_product(data: ProductDetectionSchema, db: SessionLocal = Depends(get_db)):
    """
    Dieser Endpunkt verarbeitet Produktdaten vom Detection-Service
    und speichert Statusänderungen in der Datenbank.
    """
    # Produkt prüfen, ob es existiert
    product = db.query(Product).filter(Product.id == data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produkt nicht gefunden.")

    # Detected-in-Regal-Logik
    if data.detected_in_regal:
        # Prüfen, ob es schon ein offenes `SystemTimeIN` gibt
        existing_status = (
            db.query(ProductRegalStatus)
            .filter(ProductRegalStatus.product_id == data.product_id, ProductRegalStatus.SystemTimeOUT == None)
            .first()
        )
        if existing_status:
            raise HTTPException(
                status_code=400,
                detail="Das Produkt befindet sich bereits im Regal."
            )

        # Neuen `SystemTimeIN`-Eintrag erstellen
        new_status = ProductRegalStatus(product_id=data.product_id, SystemTimeIN=datetime.utcnow())
        db.add(new_status)
        db.commit()
        db.refresh(new_status)
        return {"message": "Produkt als im Regal erkannt."}
    else:
        # Prüfen, ob ein `SystemTimeIN`-Eintrag existiert
        existing_status = (
            db.query(ProductRegalStatus)
            .filter(ProductRegalStatus.product_id == data.product_id, ProductRegalStatus.SystemTimeOUT == None)
            .first()
        )
        if not existing_status:
            raise HTTPException(
                status_code=400,
                detail="Das Produkt wurde nicht als im Regal erkannt."
            )

        # `SystemTimeOUT` setzen
        existing_status.SystemTimeOUT = datetime.utcnow()
        db.commit()
        db.refresh(existing_status)
        return {"message": "Produkt als aus dem Regal entfernt erkannt."}
