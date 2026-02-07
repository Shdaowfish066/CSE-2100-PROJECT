"""Vote endpoints for upvoting and downvoting posts and comments (Arpon's portion).
Developer: Arpon (2303134)
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.m_2303134_2303173_vote import Vote, VoteType
from app.models.m_2303134_post import Post
from app.models.m_2303147_user import User
from app.routers.r_2303147_auth import get_current_user
from app.schemas.s_2303134_vote import VoteCreate, VoteOut
from app.schemas.s_2303173_vote import VoteScoreOut

router = APIRouter(prefix="/votes", tags=["votes"])


@router.post("/post/{post_id}", status_code=status.HTTP_201_CREATED)
def vote_post(
    post_id: int,
    payload: VoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Vote on a post (upvote or downvote).
    
    If the user already voted, the vote type will be updated.
    
    Args:
        post_id: Post ID to vote on
        payload: Vote type (upvote or downvote)
        db: Database session
        current_user: Currently authenticated user
        
    Returns:
        dict: Success message and vote object
        
    Raises:
        HTTPException: 404 if post not found
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    existing = db.query(Vote).filter(
        Vote.post_id == post_id,
        Vote.user_id == current_user.id
    ).first()
    if existing:
        existing.vote_type = payload.vote_type
        db.commit()
        db.refresh(existing)
        return {"message": "Successfully updated vote", "data": VoteOut.from_orm(existing)}

    vote = Vote(
        post_id=post_id,
        user_id=current_user.id,
        vote_type=payload.vote_type
    )
    db.add(vote)
    db.commit()
    db.refresh(vote)
    return {"message": "Successfully voted on post", "data": VoteOut.from_orm(vote)}


@router.delete("/post/{post_id}", status_code=status.HTTP_200_OK)
def unvote_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Remove vote from a post.
    
    Args:
        post_id: Post ID to unvote
        db: Database session
        current_user: Currently authenticated user
        
    Returns:
        dict: Success message
        
    Raises:
        HTTPException: 404 if vote not found
    """
    vote = db.query(Vote).filter(
        Vote.post_id == post_id,
        Vote.user_id == current_user.id
    ).first()
    if not vote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vote not found"
        )
    db.delete(vote)
    db.commit()
    return {"message": "Successfully removed vote"}

@router.get("/post/{post_id}/score", response_model=VoteScoreOut)
def get_post_vote_score(
    post_id: int,
    db: Session = Depends(get_db)
):
    """Retrieve vote score for a post.
    
    Args:
        post_id: Post ID
        db: Database session
        
    Returns:
        VoteScoreOut: Vote counts and calculated score
        
    Raises:
        HTTPException: 404 if post not found
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    upvotes = db.query(func.count(Vote.id)).filter(
        Vote.post_id == post_id,
        Vote.vote_type == VoteType.UPVOTE
    ).scalar()
    downvotes = db.query(func.count(Vote.id)).filter(
        Vote.post_id == post_id,
        Vote.vote_type == VoteType.DOWNVOTE
    ).scalar()

    return {
        "upvotes": upvotes,
        "downvotes": downvotes,
        "score": upvotes - downvotes
    }