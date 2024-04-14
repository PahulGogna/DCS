from database import Base
from sqlalchemy import Column, Integer,String,Sequence,ARRAY

class Users(Base):
    __tablename__ = "users"
    id = Column("id",Integer,Sequence("id sequence",start=1), primary_key=True, nullable=False)
    name = Column("name",String, nullable=False)
    email = Column("email",String, nullable = False)
    password = Column("password",String, nullable= False)
    posts = Column("posts", ARRAY(Integer), default = [])

class Post(Base):
    __tablename__ = "posts"
    id = Column("id",Integer,Sequence("id sequence",start=1), primary_key=True, nullable=False)
    data = Column("data", String, nullable = False)
    by_user = Column("post_py", Integer, nullable = False)
