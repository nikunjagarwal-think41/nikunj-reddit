from pydantic import BaseModel, ConfigDict
from typing import Optional

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    parent_comment_id: Optional[int] = None

class CommentUpdate(BaseModel):
    content: str

class Comment(CommentBase):
    id: int
    user_id: int
    post_id: int
    parent_comment_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
