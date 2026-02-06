"""SQLAlchemy Vote model."""

from sqlalchemy import Column, ForeignKey, Integer, Enum
from sqlalchemy.orm import relationship
import enum

from app.database import Base


class VoteType(str, enum.Enum):
    UPVOTE = "upvote"
    DOWNVOTE = "downvote"


class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=True, index=True)
    comment_id = Column(Integer, ForeignKey("comments.id"), nullable=True, index=True)
    vote_type = Column(Enum(VoteType), nullable=False)

    user = relationship("User")
    post = relationship("Post")
