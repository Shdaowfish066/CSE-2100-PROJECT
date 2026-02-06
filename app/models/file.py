"""SQLAlchemy File model."""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False, index=True)
    file_size = Column(Integer, nullable=False)
    uploader_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=True)
    message_id = Column(Integer, ForeignKey("messages.id"), nullable=True)

    uploader = relationship("User")
    post = relationship("Post")
