from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .databaseProvider import DatabaseProvider

databaseProvider = DatabaseProvider()

class Products(databaseProvider.Base):
    __tablename__ = 'Products'

    productId = Column(Integer, primary_key=True, autoincrement=True)
    productName = Column(String, nullable=False)
    productAmount = Column(Integer, nullable=False)