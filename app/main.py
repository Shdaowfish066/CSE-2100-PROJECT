from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError

from app.database import Base, engine
from app import models
from app.routers import (
    auth_router,
    posts_router,
    users_router,
    votes_router_arpon,
    votes_router_emon,
    comments_router,
    comments_router_emon,
    messages_router,
    files_router,
    moderation_router,
    communities_router,
)
from app.routers.websocket import router as websocket_router
from app.config import settings

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
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
app.include_router(votes_router_arpon)
app.include_router(votes_router_emon)
app.include_router(comments_router)
app.include_router(comments_router_emon)
app.include_router(messages_router)
app.include_router(files_router)
app.include_router(moderation_router)
app.include_router(communities_router)
app.include_router(websocket_router)