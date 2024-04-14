from fastapi import HTTPException,status,APIRouter,Depends
from utils import hash,verify
import Schemas
from sqlalchemy import func, update, text, delete
from sqlalchemy.orm import Session
from database import get_db
import models
import OAuth
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    prefix= "/posts",
    tags=["posts"]
)

@router.get("/get/all")
def get_all_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).order_by(models.Post.id).all()
    return posts

@router.post("/create")
def createPost(post:Schemas.post,db:Session=Depends(get_db),get_current_user: int = Depends(OAuth.get_current_user),update_user = False):
    posted_by = get_current_user.id
    new_post = models.Post(data=post.data, by_user = posted_by)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    bucket = new_post
    if update_user:
        return bucket
    else:
        db.execute(update(models.Users).where(models.Users.id == posted_by)
        .values(posts = text(f'array_append(posts, {new_post.id})'))  # Set the 'post_id' to the newly created post's ID
        )
        db.commit()
        return bucket

@router.get("/get/{id}")
def get_by_id(id:int,db: Session = Depends(get_db)):
    post = db.query(models.Post).where(models.Post.id == id).first()
    return post

@router.post("/update/{id}")
def updatePost(id:int, post : Schemas.post, db: Session = Depends(get_db), get_current_user: int = Depends(OAuth.get_current_user)):
    posted_by = get_current_user.id
    user = db.query(models.Users).where(models.Users.id == get_current_user.id).first()
    posts_by_user = user.posts
    if id in posts_by_user:
        db.execute(
            update(models.Post).where(models.Post.id == id).values(data = post.data)
        )
        db.commit()
        return post
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

@router.delete('/delete/{id}')
def delete_post(id:int,db: Session = Depends(get_db),get_current_user: int = Depends(OAuth.get_current_user)):
    user = db.query(models.Users).where(models.Users.id == get_current_user.id).first()
    posts_by_user = user.posts
    if id in posts_by_user:
        posts_by_user.remove(id)
        db.execute(
            delete(models.Post)
            .where(models.Post.id == id)
        )

        db.execute(
        update(models.Users)
        .where(models.Users.id == get_current_user.id)
        .values(posts = posts_by_user)
        )
        db.commit()

    else:
        print(posts_by_user)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)