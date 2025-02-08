from sqlalchemy import Column, Integer, String
from .databaseProvider import DatabaseProvider
    
class Products(DatabaseProvider.base):
    __tablename__ = 'products'

    product_id = Column("product_id", Integer, primary_key=True, autoincrement=True)
    product_picture = Column("product_picture", String(255), nullable=False)
    product_name = Column("product_name", String(255), nullable=False)
    product_amount = Column("product_amount", Integer, nullable=False)

class OverallPicture(DatabaseProvider.base):
    __tablename__ = 'overall_picture'

    overall_picture_id = Column("overall_picture_id", Integer, primary_key=True, autoincrement=True)
    overall_picture = Column("overall_picture", String(255), nullable=False)
