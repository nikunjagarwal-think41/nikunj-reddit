from sqlalchemy.orm import Session
from server.models import Post
from server.schemas import PostCreate, PostUpdate

def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Post).offset(skip).limit(limit).all()

def get_posts_by_subreddit(db: Session, subreddit_id: int, skip: int = 0, limit: int = 100):
    return db.query(Post).filter(Post.subreddit_id == subreddit_id).offset(skip).limit(limit).all()

def get_post(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()

def create_post(db: Session, post: PostCreate, user_id: int, subreddit_id: int):
    post_data = post.model_dump(exclude={"subreddit_name"})
    db_post = Post(**post_data, user_id=user_id, subreddit_id=subreddit_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def update_post(db: Session, post_id: int, post: PostUpdate):
    db_post = get_post(db, post_id)
    if db_post:
        db_post.title = post.title
        db_post.content = post.content
        db.commit()
        db.refresh(db_post)
    return db_post

def delete_post(db: Session, post_id: int):
    db_post = get_post(db, post_id)
    if db_post:
        db.delete(db_post)
        db.commit()
    return db_post
