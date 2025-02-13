from sqlalchemy import Column, Integer, String
from .databaseProvider import DatabaseProvider
    
class Products(DatabaseProvider.base):
    __tablename__ = 'products'

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    type_id = Column("type_id", Integer, nullable=False)
    name = Column("name", String(255), nullable=False)
    picture = Column("picture", String(255), nullable=False)
    amount = Column("amount", Integer, nullable=False)

class OverallPicture(DatabaseProvider.base):
    __tablename__ = 'overall_picture'

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    picture = Column("picture", String(255), nullable=False)