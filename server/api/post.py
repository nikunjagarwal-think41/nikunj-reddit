from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from server import crud, schemas
from server.dependencies import get_db, get_current_user

router = APIRouter()

@router.get("", response_model=List[schemas.Post])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = crud.get_posts(db, skip=skip, limit=limit)
    return posts

@router.get("/{post_id}", response_model=schemas.Post)
def read_post(post_id: int, db: Session = Depends(get_db)):
    db_post = crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@router.put("/{post_id}", response_model=schemas.Post)
def update_post(post_id: int, post: schemas.PostUpdate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_post = crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this post")
    return crud.update_post(db=db, post_id=post_id, post=post)

@router.delete("/{post_id}", response_model=schemas.Post)
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_post = crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this post")
    return crud.delete_post(db=db, post_id=post_id)
