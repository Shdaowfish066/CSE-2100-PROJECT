"""Comment endpoints for managing post comments (Emon's portion).
Developer: Emon (2303173)
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.m_2303147_comment import Comment
from app.models.m_2303147_user import User
from app.routers.r_2303147_auth import get_current_user
from app.schemas.s_2303173_comment import CommentUpdate, CommentOut

router = APIRouter(prefix="/comments", tags=["comments"])


@router.put("/{comment_id}")
def update_comment(
    comment_id: int,
    payload: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an existing comment.
    
    Args:
        comment_id: Comment ID to update
        payload: Comment update data
        db: Database session
        current_user: Currently authenticated user
        
    Returns:
        dict: Success message and updated comment object
        
    Raises:
        HTTPException: 404 if comment not found, 403 if user not authorized
    """
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    if comment.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this comment"
        )

    if payload.content:
        comment.content = payload.content

    db.commit()
    db.refresh(comment)
    return {"message": "Successfully updated comment", "data": CommentOut.from_orm(comment)}


@router.delete("/{comment_id}", status_code=status.HTTP_200_OK)
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a comment.
    
    Args:
        comment_id: Comment ID to delete
        db: Database session
        current_user: Currently authenticated user
        
    Returns:
        dict: Success message
        
    Raises:
        HTTPException: 404 if comment not found, 403 if user not authorized
    """
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    if comment.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this comment"
        )

    db.delete(comment)
    db.commit()
    return {"message": "Successfully deleted comment"}
