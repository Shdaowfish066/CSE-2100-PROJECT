"""Vote endpoints for upvoting and downvoting posts and comments."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.vote import Vote, VoteType
from app.models.post import Post
from app.models.comment import Comment
from app.models.user import User
from app.routers.auth import get_current_user
from app.schemas.vote import VoteCreate, VoteOut, VoteScoreOut

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


@router.post("/comment/{comment_id}", status_code=status.HTTP_201_CREATED)
def vote_comment(
    comment_id: int,
    payload: VoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Vote on a comment (upvote or downvote).
    
    If the user already voted, the vote type will be updated.
    
    Args:
        comment_id: Comment ID to vote on
        payload: Vote type (upvote or downvote)
        db: Database session
        current_user: Currently authenticated user
        
    Returns:
        dict: Success message and vote object
        
    Raises:
        HTTPException: 404 if comment not found
    """
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )

    existing = db.query(Vote).filter(
        Vote.comment_id == comment_id,
        Vote.user_id == current_user.id
    ).first()
    if existing:
        existing.vote_type = payload.vote_type
        db.commit()
        db.refresh(existing)
        return {"message": "Successfully updated vote", "data": VoteOut.from_orm(existing)}

    vote = Vote(
        comment_id=comment_id,
        user_id=current_user.id,
        vote_type=payload.vote_type
    )
    db.add(vote)
    db.commit()
    db.refresh(vote)
    return {"message": "Successfully voted on comment", "data": VoteOut.from_orm(vote)}


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


@router.delete("/comment/{comment_id}", status_code=status.HTTP_200_OK)
def unvote_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Remove vote from a comment.
    
    Args:
        comment_id: Comment ID to unvote
        db: Database session
        current_user: Currently authenticated user
        
    Returns:
        dict: Success message
        
    Raises:
        HTTPException: 404 if vote not found
    """
    vote = db.query(Vote).filter(
        Vote.comment_id == comment_id,
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


@router.get("/comment/{comment_id}/score", response_model=VoteScoreOut)
def get_comment_vote_score(
    comment_id: int,
    db: Session = Depends(get_db)
):
    """Retrieve vote score for a comment.
    
    Args:
        comment_id: Comment ID
        db: Database session
        
    Returns:
        VoteScoreOut: Vote counts and calculated score
        
    Raises:
        HTTPException: 404 if comment not found
    """
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )

    upvotes = db.query(func.count(Vote.id)).filter(
        Vote.comment_id == comment_id,
        Vote.vote_type == VoteType.UPVOTE
    ).scalar()
    downvotes = db.query(func.count(Vote.id)).filter(
        Vote.comment_id == comment_id,
        Vote.vote_type == VoteType.DOWNVOTE
    ).scalar()

    return {
        "upvotes": upvotes,
        "downvotes": downvotes,
        "score": upvotes - downvotes
    }
