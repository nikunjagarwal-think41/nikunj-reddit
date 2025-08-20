from sqlalchemy.orm import Session
from server.models import Subreddit
from server.schemas import SubredditCreate

def get_subreddit_by_name(db: Session, name: str):
    return db.query(Subreddit).filter(Subreddit.name == name).first()

def get_subreddits(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Subreddit).offset(skip).limit(limit).all()

def create_subreddit(db: Session, subreddit: SubredditCreate, creator_id: int):
    db_subreddit = Subreddit(**subreddit.model_dump(), creator_id=creator_id)
    db.add(db_subreddit)
    db.commit()
    db.refresh(db_subreddit)
    return db_subreddit