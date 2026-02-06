"""Router exports."""

from app.routers.auth import router as auth_router
from app.routers.posts import router as posts_router
from app.routers.users import router as users_router
from app.routers.votes import router as votes_router
from app.routers.comments import router as comments_router
from app.routers.messages import router as messages_router
from app.routers.files import router as files_router
from app.routers.moderation import router as moderation_router

__all__ = [
    "auth_router",
    "posts_router",
    "users_router",
    "votes_router",
    "comments_router",
    "messages_router",
    "files_router",
    "moderation_router",
]
