"""Pydantic schemas for posts (2303134 - Arpon).

Developer: Arpon (2303134)
"""

from pydantic import BaseModel, ConfigDict


class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None


class PostOut(PostBase):
    id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)
