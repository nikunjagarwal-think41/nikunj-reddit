from pydantic import BaseModel, ConfigDict
from typing import Optional

class VoteBase(BaseModel):
    vote_type: str

class VoteCreate(VoteBase):
    post_id: Optional[int] = None
    comment_id: Optional[int] = None

class Vote(VoteBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)

class VoteMessage(BaseModel):
    message: str
