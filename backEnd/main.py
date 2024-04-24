import models
from sqlalchemy.orm import Session
from database import engine, sessionLocal, get_db
from fastapi import Depends,FastAPI
import users, posts

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
try:
    @app.get("/")
    def ads(db: Session = Depends(get_db)):
        return db.query(models.Users).all()
    
except Exception as e:
    print(e)