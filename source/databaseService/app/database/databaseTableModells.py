from sqlalchemy import Column, Integer, String, ForeignKey, Time
from sqlalchemy.orm import relationship
from datetime import datetime
from databaseProvider import DatabaseProvider

databaseProvider = DatabaseProvider()

class Product(databaseProvider.Base):
    __tablename__ = 'products'

    productId = Column(Integer, primary_key=True, autoincrement=True)
    productName = Column(String, nullable=False)

class StockLog(databaseProvider.Base):
    __tablename__ = 'stockLog'

    stocLogId = Column(Integer, primary_key=True, autoincrement=True)
    productId = Column(Integer, ForeignKey('products.product_id'), nullable=False)
    systemTimeIn = Column(datetime, default=datetime.utcnow)
    systemTimeOut = Column(datetime, nullable=True)

    product = relationship("Product", back_populates="stock_logs")
