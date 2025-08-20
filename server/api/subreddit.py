from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from server import crud, schemas
from server.dependencies import get_db, get_current_user
from server.core.logging_config import logger
from server.crud.post import get_posts_by_subreddit

router = APIRouter()

@router.post("", response_model=schemas.Subreddit)
def create_subreddit(subreddit: schemas.SubredditCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    logger.info(f"User {current_user.username} is creating subreddit {subreddit.name}")
    db_subreddit = crud.get_subreddit_by_name(db, name=subreddit.name)
    if db_subreddit:
        logger.warning(f"Subreddit {subreddit.name} already exists")
        raise HTTPException(status_code=400, detail="Subreddit with this name already exists")
    new_subreddit = crud.create_subreddit(db=db, subreddit=subreddit, creator_id=current_user.id)
    logger.info(f"Subreddit {new_subreddit.name} created successfully")
    return new_subreddit

@router.get("", response_model=List[schemas.Subreddit])
def read_subreddits(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    subreddits = crud.get_subreddits(db, skip=skip, limit=limit)
    return subreddits

@router.get("/{name}", response_model=schemas.Subreddit)
def read_subreddit(name: str, db: Session = Depends(get_db)):
    db_subreddit = crud.get_subreddit_by_name(db, name=name)
    if db_subreddit is None:
        raise HTTPException(status_code=404, detail="Subreddit not found")
    return db_subreddit

@router.post("/{name}/posts", response_model=schemas.Post)
def create_post_in_subreddit(name: str, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_subreddit = crud.get_subreddit_by_name(db, name=name)
    if db_subreddit is None:
        raise HTTPException(status_code=404, detail="Subreddit not found")
    return crud.create_post(db=db, post=post, user_id=current_user.id, subreddit_id=db_subreddit.id)

@router.get("/{name}/posts", response_model=List[schemas.Post])
def read_posts_in_subreddit(name: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_subreddit = crud.get_subreddit_by_name(db, name=name)
    if db_subreddit is None:
        raise HTTPException(status_code=404, detail="Subreddit not found")
    return get_posts_by_subreddit(db=db, subreddit_id=db_subreddit.id, skip=skip, limit=limit)
