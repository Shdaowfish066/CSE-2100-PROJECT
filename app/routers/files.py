from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File as FastAPIFile
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.file import File
from app.models.user import User
from app.routers.auth import get_current_user
from app.schemas.file import FileOut
from app.utils.storage import is_allowed_media, save_upload_file

router = APIRouter(prefix="/files", tags=["files"])

@router.post("/upload", status_code=status.HTTP_201_CREATED)
def upload_file(
    file: UploadFile = FastAPIFile(...),
    post_id: int | None = None,
    message_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not post_id and not message_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either post_id or message_id must be provided"
        )
    
    if not is_allowed_media(file):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only images, gifs, and videos are allowed"
        )

    file_path, file_size = save_upload_file(file)

    new_file = File(
        filename=file.filename,
        file_path=file_path,
        file_size=file_size,
        uploader_id=current_user.id,
        post_id=post_id,
        message_id=message_id
    )
    db.add(new_file)
    db.commit()
    db.refresh(new_file)
    return {"message": "Successfully uploaded file", "data": FileOut.model_validate(new_file)}

@router.get("/{file_id}", response_model=FileOut)
def get_file(
    file_id: int,
    db: Session = Depends(get_db)
):
    file = db.query(File).filter(File.id == file_id).first()
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    return file

@router.get("/user/{user_id}", response_model=list[FileOut])
def list_user_files(
    user_id: int,
    db: Session = Depends(get_db)
):
    files = db.query(File).filter(File.uploader_id == user_id).all()
    return files

@router.delete("/{file_id}", status_code=status.HTTP_200_OK)
def delete_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    file = db.query(File).filter(File.id == file_id).first()
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    if file.uploader_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this file"
        )

    db.delete(file)
    db.commit()
    return {"message": "Successfully deleted file"}
