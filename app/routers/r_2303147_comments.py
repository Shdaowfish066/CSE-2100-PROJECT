"""Content moderation and reporting endpoints.
Developer: Shihab (2303147)
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.m_2303173_report import Report, ReportStatus
from app.models.m_2303134_post import Post
from app.models.m_2303147_comment import Comment
from app.models.m_2303147_user import User
from app.routers.r_2303147_auth import get_current_user
from app.schemas.s_2303173_report import ReportCreate, ReportOut

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_report(
    payload: ReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new content report.
    
    Args:
        payload: Report creation data
        db: Database session
        current_user: Currently authenticated user
        
    Returns:
        dict: Success message and created report object
        
    Raises:
        HTTPException: 400 if neither post nor comment specified, 404 if content not found
    """
    if not payload.post_id and not payload.comment_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Must report either a post or comment"
        )

    if payload.post_id:
        post = db.query(Post).filter(Post.id == payload.post_id).first()
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )

    if payload.comment_id:
        comment = db.query(Comment).filter(Comment.id == payload.comment_id).first()
        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment not found"
            )

    report = Report(
        reporter_id=current_user.id,
        post_id=payload.post_id,
        comment_id=payload.comment_id,
        reason=payload.reason,
        description=payload.description
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return {"message": "Successfully created report", "data": ReportOut.from_orm(report)}


@router.get("/", response_model=list[ReportOut])
def list_reports(
    status_filter: ReportStatus | None = None,
    db: Session = Depends(get_db)
):
    """Retrieve all reports with optional filtering by status.
    
    Args:
        status_filter: Optional report status filter
        db: Database session
        
    Returns:
        list[ReportOut]: List of reports
        
    Note:
        TODO: Add admin role verification
    """
    query = db.query(Report)
    if status_filter:
        query = query.filter(Report.status == status_filter)
    return query.all()


@router.get("/{report_id}", response_model=ReportOut)
def get_report(
    report_id: int,
    db: Session = Depends(get_db)
):
    """Retrieve a specific report by ID.
    
    Args:
        report_id: Report ID
        db: Database session
        
    Returns:
        ReportOut: Report object
        
    Raises:
        HTTPException: 404 if report not found
    """
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    return report


@router.put("/{report_id}/review")
def review_report(
    report_id: int,
    new_status: ReportStatus,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update the status of a report during review.
    
    Args:
        report_id: Report ID to review
        new_status: New report status
        db: Database session
        current_user: Currently authenticated user
        
    Returns:
        dict: Success message and updated report object
        
    Raises:
        HTTPException: 404 if report not found
        
    Note:
        TODO: Add admin role verification
    """
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )

    report.status = new_status
    db.commit()
    db.refresh(report)
    return {"message": "Successfully reviewed report", "data": ReportOut.from_orm(report)}


@router.delete("/{report_id}", status_code=status.HTTP_200_OK)
def delete_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a report.
    
    Args:
        report_id: Report ID to delete
        db: Database session
        current_user: Currently authenticated user
        
    Raises:
        HTTPException: 404 if report not found
        
    Note:
        TODO: Add admin role verification
    """
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )

    db.delete(report)
    db.commit()
    return {"message": "Successfully deleted report"}
