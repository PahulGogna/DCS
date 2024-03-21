import  psycopg2
from psycopg2.extras import RealDictCursor
import time
import os
import models
from sqlalchemy.orm import Session
from database import engine, sessionLocal, get_db
from fastapi import Depends,FastAPI
import users
from config import config

models.Base.metadata.create_all(bind=engine)

hostname = config.get('db_hostname')
# hostname = os.environ["db_hostname"]
password= config.get('db_password')
# password = os.environ["db_password"]

# connecting to the database
while True:
    try:
        db = psycopg2.connect(host=hostname,database= "listingai",user= "listingai_user",password = password ,cursor_factory=RealDictCursor)
        cursor = db.cursor()
        print("\nConnected to Database!!\n")
        break
    except Exception as error:
        print("Connection Failed!")
        print("Error: ", error)
        time.sleep(2)

app = FastAPI()

app.include_router(users.router)

@app.get("/")
def ads(db: Session = Depends(get_db)):
    
    return db.query(models.Users).all()
