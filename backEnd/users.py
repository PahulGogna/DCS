from fastapi import HTTPException,status,APIRouter,Depends
from utils import hash,verify
import Schemas
from sqlalchemy.orm import Session
from database import get_db
import models
import OAuth
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    prefix= "/users",
    tags=["Users"]
)

@router.post('/create')
def create_user(user_data:Schemas.create_user,db: Session = Depends(get_db)):

    existing_users = db.query(models.Users).filter(models.Users.email==user_data.email).first()
    if existing_users:
        raise HTTPException(status.HTTP_409_CONFLICT, detail="Email already exists")

    password = user_data.password
    user_data.password = hash(password)
    new_user = models.Users(**user_data.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post('/login')
def user_login(payLoad: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.email == payLoad.username).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")
    
    if verify(payLoad.password, user.password):

        created_token = OAuth.create_access_token({"user_id": user.id})

        return {"Token":created_token, "token_type":"bearer"}
    
    return {"user not found"}

    
@router.post('/logout')
def user_logout():
    pass