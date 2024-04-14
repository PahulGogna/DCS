from pydantic import BaseModel,EmailStr
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id : Optional[int] = None


class User(BaseModel):
    name: str
    email: EmailStr


class login(BaseModel):
    email: EmailStr
    password: str


class create_user(User):
    password: str

class post(BaseModel):
    data : str

class UserInDB(User):
    password: str