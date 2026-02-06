"""Pydantic schemas for votes."""

from pydantic import BaseModel, ConfigDict
from app.models.vote import VoteType


class VoteCreate(BaseModel):
    vote_type: VoteType


class VoteOut(BaseModel):
    id: int
    user_id: int
    post_id: int | None
    comment_id: int | None
    vote_type: VoteType

    model_config = ConfigDict(from_attributes=True)


class VoteScoreOut(BaseModel):
    """Response model for vote score endpoints."""
    upvotes: int
    downvotes: int
    score: int
