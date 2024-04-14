from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# from config import config
import os

try:
    DATABASE_URL = os.environ['DATABASE_URL']
    # DATABASE_URL = config.get('DATABASE_URL')
except Exception as e:
    raise e

engine = create_engine(DATABASE_URL)

sessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()