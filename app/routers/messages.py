"""Private messaging endpoints for user-to-user communication."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.message import Message
from app.models.user import User
from app.routers.auth import get_current_user
from app.schemas.message import MessageCreate, MessageOut

router = APIRouter(prefix="/messages", tags=["messages"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def send_message(
    payload: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Send a private message to another user.
    
    Args:
        payload: Message creation data
        db: Database session
        current_user: Currently authenticated user
        
    Returns:
        dict: Success message and created message object
        
    Raises:
        HTTPException: 404 if recipient not found
    """
    recipient = db.query(User).filter(User.id == payload.recipient_id).first()
    if not recipient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipient not found"
        )

    message = Message(
        sender_id=current_user.id,
        recipient_id=payload.recipient_id,
        content=payload.content,
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return {"message": "Successfully sent message", "data": MessageOut.from_orm(message)}


@router.get("/conversation/{user_id}", response_model=list[MessageOut])
def get_conversation(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve all messages in a conversation with a specific user.
    
    Args:
        user_id: Other user's ID
        db: Database session
        current_user: Currently authenticated user
        
    Returns:
        list[MessageOut]: List of messages in the conversation
        
    Raises:
        HTTPException: 404 if user not found
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    messages = db.query(Message).filter(
        or_(
            (Message.sender_id == current_user.id) & (Message.recipient_id == user_id),
            (Message.sender_id == user_id) & (Message.recipient_id == current_user.id)
        )
    ).order_by(Message.created_at.asc()).all()

    return messages


@router.get("/inbox", response_model=list[MessageOut])
def get_inbox(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve all messages in the user's inbox.
    
    Args:
        db: Database session
        current_user: Currently authenticated user
        
    Returns:
        list[MessageOut]: List of received messages
    """
    messages = db.query(Message).filter(
        Message.recipient_id == current_user.id
    ).order_by(Message.created_at.desc()).all()
    return messages


@router.get("/sent", response_model=list[MessageOut])
def get_sent(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve all messages sent by the user."""
    messages = db.query(Message).filter(
        Message.sender_id == current_user.id
    ).order_by(Message.created_at.desc()).all()
    return messages


@router.put("/{message_id}/mark-read")
def mark_as_read(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark a message as read.
    
    Args:
        message_id: Message ID to mark as read
        db: Database session
        current_user: Currently authenticated user
        
    Returns:
        dict: Success message and updated message object
        
    Raises:
        HTTPException: 404 if message not found, 403 if user not authorized
    """
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    if message.recipient_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to mark this message"
        )

    message.is_read = True
    db.commit()
    db.refresh(message)
    return {"message": "Successfully marked message as read", "data": MessageOut.from_orm(message)}


@router.delete("/{message_id}", status_code=status.HTTP_200_OK)
def delete_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a message.
    
    Args:
        message_id: Message ID to delete
        db: Database session
        current_user: Currently authenticated user
        
    Returns:
        dict: Success message
        
    Raises:
        HTTPException: 404 if message not found, 403 if user not authorized
    """
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    if message.sender_id != current_user.id and message.recipient_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this message"
        )

    db.delete(message)
    db.commit()
    return {"message": "Successfully deleted message"}


