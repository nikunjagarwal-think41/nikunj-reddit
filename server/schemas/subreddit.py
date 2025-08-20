from pydantic import BaseModel, ConfigDict
from typing import Optional

class SubredditBase(BaseModel):
    name: str
    description: str

class SubredditCreate(SubredditBase):
    pass

class Subreddit(SubredditBase):
    id: int
    creator_id: int

    model_config = ConfigDict(from_attributes=True)