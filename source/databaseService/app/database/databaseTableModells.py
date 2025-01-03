from sqlalchemy import Column, Integer, String
from .databaseProvider import DatabaseProvider

'''
class Products(DatabaseProvider.Base):
    __tablename__ = 'products'

    productId = Column("productid", Integer, primary_key=True)
    productName = Column("productname", String(30), nullable=False)
    productAmount = Column("productamount", Integer, nullable=False)
'''
    
class Products(DatabaseProvider.Base):
    __tablename__ = 'products'

    productId = Column(Integer, primary_key=True, autoincrement=True)
    productName = Column(String(255), nullable=False)
    productAmount = Column(Integer, nullable=False)