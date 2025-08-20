from sqlalchemy.orm import Session
from server.models import Comment
from server.schemas import CommentCreate

def get_comments_by_post(db: Session, post_id: int, skip: int = 0, limit: int = 100):
    return db.query(Comment).filter(Comment.post_id == post_id).offset(skip).limit(limit).all()

def create_comment(db: Session, comment: CommentCreate, user_id: int, post_id: int):
    db_comment = Comment(**comment.model_dump(), user_id=user_id, post_id=post_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_comment(db: Session, comment_id: int):
    return db.query(Comment).filter(Comment.id == comment_id).first()

def update_comment(db: Session, comment_id: int, content: str):
    db_comment = get_comment(db, comment_id)
    if db_comment:
        db_comment.content = content
        db.commit()
        db.refresh(db_comment)
    return db_comment

def delete_comment(db: Session, comment_id: int):
    db_comment = get_comment(db, comment_id)
    if db_comment:
        db.delete(db_comment)
        db.commit()
    return db_comment