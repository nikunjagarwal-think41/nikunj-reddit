from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from server.database import Base

class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=True)
    comment_id = Column(Integer, ForeignKey("comments.id"), nullable=True)
    vote_type = Column(Enum("upvote", "downvote", name="vote_type_enum"), nullable=False)
