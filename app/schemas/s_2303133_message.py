"""Pydantic schemas for messages (2303133 - Tahsan).

Developer: Tahsan (2303133)
"""

from pydantic import BaseModel, ConfigDict
from datetime import datetime


class MessageCreate(BaseModel):
    recipient_id: int
    content: str


class MessageOut(BaseModel):
    id: int
    sender_id: int
    recipient_id: int
    content: str
    created_at: datetime
    is_read: bool

    model_config = ConfigDict(from_attributes=True)
