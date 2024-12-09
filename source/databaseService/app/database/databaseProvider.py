from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

class DatabaseProvider:
    DATABASE_URL = "sqlite:///./test.db"

    def __init__(self):
        # Initilies the engine and the session fabricator
        self.engine = create_engine(self.DATABASE_URL)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.Base = declarative_base()  

    def initDb(self):
        # Initilies the tables in the database
        self.Base.metadata.create_all(bind=self.engine)

    def getSession(self):
        return self.SessionLocal()