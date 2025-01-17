from sqlalchemy import Column, Integer, String
from .databaseProvider import DatabaseProvider
    
class Products(DatabaseProvider.Base):
    __tablename__ = 'products'

    product_id = Column("product_id", Integer, primary_key=True, autoincrement=True)
    product_picture = Column("product_picture", String(255), nullable=False)
    product_name = Column("product_name", String(255), nullable=False)
    product_amount = Column("product_amount", Integer, nullable=False)

class Products(DatabaseProvider.Base):
    __tablename__ = 'overall_picture'

    overall_picture = Column("overall_picture", String(255), nullable=False)