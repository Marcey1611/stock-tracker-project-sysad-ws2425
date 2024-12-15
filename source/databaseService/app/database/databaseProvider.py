import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

class DatabaseProvider:
    Base = declarative_base()

    def __init__(self):
        load_dotenv()

        # Initilies the engine and the session fabricator
        self.engine = create_engine(os.getenv("DATABASE_URL"))
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)  

    def initDb(self):
        # Initilies the tables in the database
        self.Base.metadata.create_all(bind=self.engine)

    def getSession(self):
        return self.SessionLocal()