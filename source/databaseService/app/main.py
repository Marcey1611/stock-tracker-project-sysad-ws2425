# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Product, StockLog
from database import SessionLocal, init_db
from schemas import ProductCreate, StockLogCreate, StockLogResponse
from datetime import datetime

# Initialisiere die Datenbank
init_db()

app = FastAPI()

# Hilfsfunktion, um die Session zu bekommen
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/addProduct", response_model=StockLogResponse)
async def add_product(stock_log: StockLogCreate, db: Session = Depends(get_db)):
    # Überprüfen, ob das Produkt bereits existiert
    product = db.query(Product).filter(Product.product_id == stock_log.product_id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Füge einen StockLog-Eintrag hinzu
    db_stock_log = StockLog(**stock_log.dict())
    db.add(db_stock_log)
    db.commit()
    db.refresh(db_stock_log)
    
    return db_stock_log

@app.post("/addDetectedProduct", response_model=ProductCreate)
async def add_detected_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(product_name=product.product_name)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    return db_product
