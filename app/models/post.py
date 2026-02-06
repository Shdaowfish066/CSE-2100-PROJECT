"""SQLAlchemy Post model."""

from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Post(Base):
	__tablename__ = "posts"

	id = Column(Integer, primary_key=True, index=True)
	title = Column(String(255), nullable=False, index=True)
	content = Column(Text, nullable=False)
	owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

	owner = relationship("User")
