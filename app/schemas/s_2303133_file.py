"""Pydantic schemas for files (2303133 - Tahsan).

Developer: Tahsan (2303133)
"""

from pydantic import BaseModel, ConfigDict


class FileOut(BaseModel):
    id: int
    filename: str
    file_path: str
    file_size: int
    uploader_id: int
    post_id: int | None
    message_id: int | None

    model_config = ConfigDict(from_attributes=True)
