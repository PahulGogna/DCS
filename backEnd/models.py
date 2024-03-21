from database import Base
from sqlalchemy import Column, Integer,String,Sequence,ARRAY

class Users(Base):
    __tablename__ = "users"
    id = Column("id",Integer,Sequence("id sequence",start=1), primary_key=True, nullable=False)
    name = Column("name",String, nullable=False)
    email = Column("email",String, nullable = False)
    password = Column("password",String, nullable= False)

# class Listing(Base):
#     images = Column("images",ARRAY(String))
