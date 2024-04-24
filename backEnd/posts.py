from fastapi import HTTPException,status,APIRouter,Depends
from utils import hash,verify
from fastapi import BackgroundTasks
import Schemas
from sqlalchemy import func, update, text, delete, or_
from sqlalchemy.orm import Session
from database import get_db
import models
import OAuth
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
import AI

router = APIRouter(
    prefix= "/posts",
    tags=["posts"]
)

@router.get("/get/tags")
def get_nondefault_posts(db: Session = Depends(get_db)):
    tags = db.query(models.Post.tag).distinct().all()
    tag_list = [tag.tag for tag in tags]
    return tag_list


@router.get("/get/tag/{tag}")
def get_posts_by_tag(tag: str, db: Session = Depends(get_db)):
    posts = db.query(models.Post).filter(models.Post.tags.any(tag)).all()
    return posts

@router.get("/search/{query}")
def searchPosts(query: str, db: Session = Depends(get_db)):
    posts = db.query(models.Post).filter(or_(models.Post.data.ilike(f"%{query}%"), models.Post.data.ilike(f"%{query} %"), models.Post.data.ilike(f"% {query}%"))).all()
    return posts    

@router.get("/get/all")
def get_all_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).order_by(models.Post.id).all()
    return posts


@router.post("/create")
def create_post(post: Schemas.post, background_tasks: BackgroundTasks, db: Session = Depends(get_db), get_current_user: int = Depends(OAuth.get_current_user)):
    
    posted_by = get_current_user.id
    new_post = models.Post(data=post.data, post_by=posted_by, tag = post.tag)
    bucket = new_post
    check,score = AI.post_check(bucket.to_dict())

    if score <= 4:
        return {"success": False, "detail": "Post was not suitable"}
    
    new_post.rating = score
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    db.execute(update(models.Users)
               .where(models.Users.id == posted_by)
               .values(posts = text(f'array_append(posts, {new_post.id})'))  # Set the 'post_id' to the newly created post's ID
               )
    db.commit()

    # background_tasks.add_task(AI.post_check, bucket.to_dict(),db,get_current_user)
    return  {"success":check, "detail": new_post.to_dict()}

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
            update(models.Post).where(models.Post.id == id).values(data = post.data, tag = post.tag)
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
        print(get_current_user)
        if get_current_user == 1:
            db.execute(
                delete(models.Post)
                .where(models.Post.id == id)
            )
            db.commit()
            return 
        print(posts_by_user)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)