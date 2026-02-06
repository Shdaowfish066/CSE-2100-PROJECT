"""Storage helpers for media uploads."""

from __future__ import annotations

import os
import shutil
import uuid
from pathlib import Path

from fastapi import UploadFile

ALLOWED_IMAGE_MIME_TYPES = {
	"image/jpeg",
	"image/png",
	"image/gif",
	"image/webp",
}

ALLOWED_VIDEO_MIME_TYPES = {
	"video/mp4",
	"video/webm",
	"video/quicktime",
}

ALLOWED_MEDIA_MIME_TYPES = ALLOWED_IMAGE_MIME_TYPES | ALLOWED_VIDEO_MIME_TYPES

ALLOWED_MEDIA_EXTENSIONS = {
	".jpg",
	".jpeg",
	".png",
	".gif",
	".webp",
	".mp4",
	".webm",
	".mov",
}


def is_allowed_media(upload_file: UploadFile) -> bool:
	"""Validate media type based on MIME and file extension."""
	if not upload_file.filename or not upload_file.content_type:
		return False
	ext = Path(upload_file.filename).suffix.lower()
	return (
		upload_file.content_type in ALLOWED_MEDIA_MIME_TYPES
		and ext in ALLOWED_MEDIA_EXTENSIONS
	)


def save_upload_file(upload_file: UploadFile, upload_dir: str = "uploads") -> tuple[str, int]:
	"""Save uploaded file to disk and return (path, size)."""
	os.makedirs(upload_dir, exist_ok=True)
	ext = Path(upload_file.filename).suffix.lower()
	stored_name = f"{uuid.uuid4().hex}{ext}"
	file_path = os.path.join(upload_dir, stored_name)

	with open(file_path, "wb") as buffer:
		shutil.copyfileobj(upload_file.file, buffer)

	file_size = os.path.getsize(file_path)
	return file_path, file_size
