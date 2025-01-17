from sqlalchemy import Column, Integer, String
from .databaseProvider import DatabaseProvider

class Products(DatabaseProvider.Base):
    __tablename__ = 'products'

    productId = Column("productId", Integer, primary_key=True)
    productName = Column("product_picture", String(255), nullable=False)
    productName = Column("productName", String(30), nullable=False)
    productAmount = Column("productAmount", Integer, nullable=False)

class Products(DatabaseProvider.Base):
    __tablename__ = 'overall_picture'

    overall_picture = Column("overall_picture", String(255), nullable=False)