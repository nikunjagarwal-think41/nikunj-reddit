from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Text
from sqlalchemy.orm import relationship
from server.database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=True)
    media_url = Column(String, nullable=True)
    link_url = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    subreddit_id = Column(Integer, ForeignKey("subreddits.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    owner = relationship("User")
    subreddit = relationship("Subreddit")
