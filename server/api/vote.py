from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import Union
from server import crud, schemas
from server.dependencies import get_db, get_current_user

router = APIRouter()

@router.post("/posts/{post_id}/vote")
def vote_on_post(post_id: int, vote: schemas.VoteCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_post = crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    existing_vote = crud.get_vote(db, user_id=current_user.id, post_id=post_id)
    if existing_vote:
        if existing_vote.vote_type == vote.vote_type:
            crud.delete_vote(db, vote_id=existing_vote.id)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            crud.delete_vote(db, vote_id=existing_vote.id)
    
    vote.post_id = post_id
    return crud.create_vote(db=db, vote=vote, user_id=current_user.id)

@router.post("/comments/{comment_id}/vote")
def vote_on_comment(comment_id: int, vote: schemas.VoteCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_comment = crud.get_comment(db, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    existing_vote = crud.get_vote(db, user_id=current_user.id, comment_id=comment_id)
    if existing_vote:
        if existing_vote.vote_type == vote.vote_type:
            crud.delete_vote(db, vote_id=existing_vote.id)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            crud.delete_vote(db, vote_id=existing_vote.id)

    vote.comment_id = comment_id
    return crud.create_vote(db=db, vote=vote, user_id=current_user.id)