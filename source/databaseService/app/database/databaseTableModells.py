from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .databaseProvider import DatabaseProvider

databaseProvider = DatabaseProvider()

class Product(databaseProvider.Base):
    __tablename__ = 'Products'

    productId = Column(Integer, primary_key=True, autoincrement=True)
    productName = Column(String, nullable=False)

    # Definiere die back_populates für StockLog
    stockLogs = relationship("StockLog", back_populates="product")


class StockLog(databaseProvider.Base):
    __tablename__ = 'StockLog'

    stockLogId = Column(Integer, primary_key=True, autoincrement=True)
    productId = Column(Integer, ForeignKey('products.ProductID'), nullable=False)
    systemTimeIn = Column(DateTime, nullable=True)
    systemTimeOut = Column(DateTime, nullable=True)

    # Verknüpfung mit Product über back_populates
    product = relationship("Product", back_populates="stockLogs")