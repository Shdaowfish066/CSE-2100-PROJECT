from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, String
from sqlalchemy.orm import relationship

from app.database import Base

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    owner = relationship("User")
    post = relationship("Post")
