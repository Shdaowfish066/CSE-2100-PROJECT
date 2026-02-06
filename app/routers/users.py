"""User profile management endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.routers.auth import get_current_user
from app.schemas.user import UserOut, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserOut)
def read_me(
    current_user: User = Depends(get_current_user)
):
    """Retrieve the current authenticated user's profile.
    
    Args:
        current_user: Currently authenticated user
        
    Returns:
        UserOut: Current user profile
    """
    return current_user


@router.get("/{user_id}", response_model=UserOut)
def read_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Retrieve a user's public profile by ID.
    
    Args:
        user_id: User ID
        db: Database session
        
    Returns:
        UserOut: User profile
        
    Raises:
        HTTPException: 404 if user not found
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.get("/by-username/{username}", response_model=UserOut)
def read_user_by_username(
    username: str,
    db: Session = Depends(get_db)
):
    """Retrieve a user's public profile by username.
    
    Args:
        username: Username
        db: Database session
        
    Returns:
        UserOut: User profile
        
    Raises:
        HTTPException: 404 if user not found
    """
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.put("/{user_id}")
def update_user(
    user_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update user account information.
    
    Users can only update their own account. All fields are optional.
    
    Args:
        user_id: User ID to update
        payload: User update data
        db: Database session
        current_user: Currently authenticated user
        
    Returns:
        dict: Success message and updated user profile
        
    Raises:
        HTTPException: 403 if user not authorized, 404 if user not found,
                      400 if username or email already taken
    """
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update another user's account"
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Update only fields that were provided
    if payload.username is not None:
        # Check if username is already taken
        existing = db.query(User).filter(
            User.username == payload.username,
            User.id != user_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        user.username = payload.username

    if payload.email is not None:
        # Check if email is already taken
        existing = db.query(User).filter(
            User.email == payload.email,
            User.id != user_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        user.email = payload.email

    if payload.is_active is not None:
        user.is_active = payload.is_active

    db.commit()
    db.refresh(user)
    return {"message": "Successfully updated user", "data": UserOut.from_orm(user)}


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete user account.
    
    Users can only delete their own account.
    
    Args:
        user_id: User ID to delete
        db: Database session
        current_user: Currently authenticated user
        
    Returns:
        dict: Success message
        
    Raises:
        HTTPException: 403 if user not authorized, 404 if user not found
    """
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete another user's account"
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    db.delete(user)
    db.commit()
    return {"message": "Successfully deleted user account"}

