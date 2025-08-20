from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from server import crud, schemas
from server.dependencies import get_db, get_current_user

router = APIRouter()

@router.get("/posts/{post_id}/comments", response_model=List[schemas.Comment])
def read_comments_for_post(post_id: int, db: Session = Depends(get_db)):
    comments = crud.get_comments_by_post(db, post_id=post_id)
    return comments

@router.post("/posts/{post_id}/comments", response_model=schemas.Comment)
def create_comment_for_post(post_id: int, comment: schemas.CommentCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_post = crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return crud.create_comment(db=db, comment=comment, user_id=current_user.id, post_id=post_id)

@router.put("/comments/{comment_id}", response_model=schemas.Comment)
def update_comment(comment_id: int, comment: schemas.CommentUpdate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_comment = crud.get_comment(db, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    if db_comment.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this comment")
    return crud.update_comment(db=db, comment_id=comment_id, content=comment.content)

@router.delete("/comments/{comment_id}", response_model=schemas.Comment)
def delete_comment(comment_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_comment = crud.get_comment(db, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    if db_comment.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this comment")
    return crud.delete_comment(db=db, comment_id=comment_id)
