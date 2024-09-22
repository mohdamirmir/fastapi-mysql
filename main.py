from fastapi import FastAPI,HTTPException,Depends,status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine,SessionLocal
from sqlalchemy.orm import Session


app = FastAPI()
models.Base.metadata.create_all(bind=engine)


class PostBase(BaseModel):
    title: str
    content: str
    user_id: int
    
class UserBase(BaseModel):
    username: str
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]


@app.post("/posts",status_code=status.HTTP_201_CREATED)
async def create_post(post: PostBase, db: db_dependency):
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()


@app.get("/posts/{post_id}",status_code=status.HTTP_200_OK) 
async def read_post(post_id: int, db: db_dependency):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post == None:
        raise HTTPException(status_code=404,detail='Post Not Found')
    return post

@app.delete("posts/{post_id}",status_code=status.HTTP_200_OK)
async def delete_post(post_id: int, db: db_dependency):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post == None:
        raise HTTPException(status_code=404,detail='Post Not Found')
    db.delete(db_post)
    db.commit()

@app.post("/users",status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    


@app.get("/users/{user_id}",status_code=status.HTTP_200_OK) 
async def read_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user == None:
        raise HTTPException(status_code=404,detail='User Not Found')
    return user


@app.delete("/users/{username}",status_code=status.HTTP_200_OK) 
async def delete_user(username: str, db: db_dependency):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if db_user == None:
        raise HTTPException(status_code=404,detail='User Not Found')
    db.delete(db_user)
    db.commit()