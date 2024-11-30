from sqlalchemy import Column, Integer, String, ForeignKey, Time
from sqlalchemy.orm import relationship
from datetime import datetime
from database_provider import DatabaseProvider

dbProvider = DatabaseProvider()

class Product(dbProvider.Base):
    __tablename__ = 'products'

    productId = Column(Integer, primary_key=True, autoincrement=True)
    productName = Column(String, nullable=False)

class StockLog(dbProvider.Base):
    __tablename__ = 'stockLog'

    stocLogId = Column(Integer, primary_key=True, autoincrement=True)
    productId = Column(Integer, ForeignKey('products.product_id'), nullable=False)
    systemTimeIn = Column(datetime, default=datetime.utcnow)
    systemTimeOut = Column(datetime, nullable=True)

    product = relationship("Product", back_populates="stock_logs")
