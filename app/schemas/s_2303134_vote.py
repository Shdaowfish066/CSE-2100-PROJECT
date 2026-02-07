"""Pydantic schemas for votes (2303134 - Arpon).

Developer: Arpon (2303134)
"""

from pydantic import BaseModel, ConfigDict
from app.models.m_2303134_2303173_vote import VoteType


class VoteCreate(BaseModel):
    vote_type: VoteType


class VoteOut(BaseModel):
    id: int
    user_id: int
    post_id: int | None
    comment_id: int | None
    vote_type: VoteType

    model_config = ConfigDict(from_attributes=True)
