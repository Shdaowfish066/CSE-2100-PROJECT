"""Pydantic schemas for votes (2303173 - Emon).

Developer: Emon (2303173)
"""

from pydantic import BaseModel, ConfigDict
from app.models.m_2303134_2303173_vote import VoteType


class VoteScoreOut(BaseModel):
    """Response model for vote score endpoints."""
    upvotes: int
    downvotes: int
    score: int
