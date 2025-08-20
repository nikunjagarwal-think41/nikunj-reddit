from pydantic import BaseModel, ConfigDict
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: Optional[str] = None
    media_url: Optional[str] = None
    link_url: Optional[str] = None

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: str
    content: str

class Post(PostBase):
    id: int
    user_id: int
    subreddit_id: int

    model_config = ConfigDict(from_attributes=True)
