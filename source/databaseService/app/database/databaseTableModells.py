from sqlalchemy import Column, Integer, String
from .databaseProvider import DatabaseProvider
    
class Products(DatabaseProvider.base):
    __tablename__ = 'products'

    id = Column("product_id", Integer, primary_key=True, autoincrement=True)
    name = Column("product_name", String(255), nullable=False)
    picture = Column("product_picture", String(255), nullable=False)
    amount = Column("product_amount", Integer, nullable=False)

class OverallPicture(DatabaseProvider.base):
    __tablename__ = 'overall_picture'

    id = Column("overall_picture_id", Integer, primary_key=True, autoincrement=True)
    picture = Column("overall_picture", String(255), nullable=False)