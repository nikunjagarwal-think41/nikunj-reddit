from sqlalchemy.orm import Session
from server.models import Vote
from server.schemas import VoteCreate

def get_vote(db: Session, user_id: int, post_id: int = None, comment_id: int = None):
    if post_id:
        return db.query(Vote).filter(Vote.user_id == user_id, Vote.post_id == post_id).first()
    if comment_id:
        return db.query(Vote).filter(Vote.user_id == user_id, Vote.comment_id == comment_id).first()

def create_vote(db: Session, vote: VoteCreate, user_id: int):
    db_vote = Vote(**vote.model_dump(), user_id=user_id)
    db.add(db_vote)
    db.commit()
    db.refresh(db_vote)
    return db_vote

def delete_vote(db: Session, vote_id: int):
    db_vote = db.query(Vote).filter(Vote.id == vote_id).first()
    if db_vote:
        db.delete(db_vote)
        db.commit()
    return db_vote