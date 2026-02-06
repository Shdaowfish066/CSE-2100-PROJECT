"""Comment endpoints for managing post comments."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.comment import Comment
from app.models.post import Post
from app.models.user import User
from app.routers.auth import get_current_user
from app.schemas.comment import CommentCreate, CommentUpdate, CommentOut

router = APIRouter(prefix="/comments", tags=["comments"])


@router.post("/{post_id}", status_code=status.HTTP_201_CREATED)
def create_comment(
    post_id: int,
    payload: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new comment on a post.
    
    Args:
        post_id: Post ID to comment on
        payload: Comment creation data
        db: Database session
        current_user: Currently authenticated user
        
    Returns:
        dict: Success message and created comment object
        
    Raises:
        HTTPException: 404 if post not found
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    comment = Comment(
        content=payload.content,
        post_id=post_id,
        owner_id=current_user.id
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return {"message": "Successfully created comment", "data": CommentOut.from_orm(comment)}


@router.get("/post/{post_id}", response_model=list[CommentOut])
def list_comments(
    post_id: int,
    db: Session = Depends(get_db)
):
    """Retrieve all comments for a specific post.
    
    Args:
        post_id: Post ID
        db: Database session
        
    Returns:
        list[CommentOut]: List of comments on the post
        
    Raises:
        HTTPException: 404 if post not found
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    return db.query(Comment).filter(Comment.post_id == post_id).all()


@router.get("/{comment_id}", response_model=CommentOut)
def get_comment(
    comment_id: int,
    db: Session = Depends(get_db)
):
    """Retrieve a specific comment by ID.
    
    Args:
        comment_id: Comment ID
        db: Database session
        
    Returns:
        CommentOut: Comment object
        
    Raises:
        HTTPException: 404 if comment not found
    """
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    return comment


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
