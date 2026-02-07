"""Pydantic schemas for comments (2303173 - Emon).

Developer: Emon (2303173)
"""

from pydantic import BaseModel, ConfigDict


class CommentUpdate(BaseModel):
    content: str | None = None


class CommentOut(BaseModel):
    id: int
    content: str
    post_id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)
