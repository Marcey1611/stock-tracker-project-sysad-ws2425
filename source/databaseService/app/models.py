from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String, nullable=False)

class StockLog(Base):
    __tablename__ = 'stocklog'

    stocklog_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.product_id'), nullable=False)
    systemtimein = Column(DateTime, default=datetime.utcnow)
    systemtimeout = Column(DateTime, nullable=True)

    product = relationship("Product", back_populates="stock_logs")

Product.stock_logs = relationship("StockLog", back_populates="product")
