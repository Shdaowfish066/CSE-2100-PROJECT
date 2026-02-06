"""Post CRUD endpoints for managing posts with title and content."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.post import Post
from app.models.user import User
from app.routers.auth import get_current_user
from app.schemas.post import PostCreate, PostUpdate, PostOut

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_post(
    payload: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new post.
    
    Args:
        payload: Post creation data containing title and content
        db: Database session
        current_user: Currently authenticated user
        
    Returns:
        dict: Success message and created post object
    """
    post = Post(title=payload.title, content=payload.content, owner_id=current_user.id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return {"message": "Successfully created post", "data": PostOut.from_orm(post)}


@router.get("/me", response_model=list[PostOut])
def get_my_posts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve all posts created by the currently authenticated user.
    
    Args:
        db: Database session
        current_user: Currently authenticated user
        
    Returns:
        list[PostOut]: List of posts created by the user
    """
    return db.query(Post).filter(Post.owner_id == current_user.id).all()


@router.get("/", response_model=list[PostOut])
def list_posts(db: Session = Depends(get_db)):
    """Retrieve all posts.
    
    Args:
        db: Database session
        
    Returns:
        list[PostOut]: List of all posts
    """
    return db.query(Post).all()


@router.get("/user/{author_id}", response_model=list[PostOut])
def get_posts_by_author(author_id: int, db: Session = Depends(get_db)):
    """Retrieve all posts by a specific author.
    
    Args:
        author_id: User ID of the post author
        db: Database session
        
    Returns:
        list[PostOut]: List of posts by the specified author
        
    Raises:
        HTTPException: 404 if no posts found for the author
    """
    posts = db.query(Post).filter(Post.owner_id == author_id).all()
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No posts found for this author"
        )
    return posts


@router.get("/{post_id}", response_model=PostOut)
def get_post(post_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific post by ID.
    
    Args:
        post_id: Post ID
        db: Database session
        
    Returns:
        PostOut: Post object
        
    Raises:
        HTTPException: 404 if post not found
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    return post


@router.put("/{post_id}")
def update_post(
    post_id: int,
    payload: PostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an existing post.
    
    Args:
        post_id: Post ID to update
        payload: Post update data
        db: Database session
        current_user: Currently authenticated user
        
    Returns:
        dict: Success message and updated post object
        
    Raises:
        HTTPException: 404 if post not found, 403 if user not authorized
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this post"
        )

    if payload.title is not None:
        post.title = payload.title
    if payload.content is not None:
        post.content = payload.content

    db.commit()
    db.refresh(post)
    return {"message": "Successfully updated post", "data": PostOut.from_orm(post)}


@router.delete("/{post_id}", status_code=status.HTTP_200_OK)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a post.
    
    Args:
        post_id: Post ID to delete
        db: Database session
        current_user: Currently authenticated user
        
    Returns:
        dict: Success message
        
    Raises:
        HTTPException: 404 if post not found, 403 if user not authorized
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this post"
        )

    db.delete(post)
    db.commit()
    return {"message": "Successfully deleted post"}
