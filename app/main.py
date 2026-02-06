# FastAPI application entry point
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.database import Base, engine
from app import models
from app.routers import (
    auth_router,
    posts_router,
    users_router,
    votes_router,
    comments_router,
    messages_router,
    files_router,
    moderation_router,
)
from app.config import settings

# Ensure database tables are created on startup (models must be imported first)
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name, version="1.0.0")


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    """Custom handler for validation errors - returns 400 with 'Invalid email' for email errors."""
    errors = exc.errors()
    for error in errors:
        if "email" in error.get("loc", ()):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": "Invalid email"}
            )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Validation error"}
    )


app.include_router(auth_router)
app.include_router(posts_router)
app.include_router(users_router)
app.include_router(votes_router)
app.include_router(comments_router)
app.include_router(messages_router)
app.include_router(files_router)
app.include_router(moderation_router)