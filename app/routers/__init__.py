from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.reports import router as comments_router

from app.routers.posts import router as posts_router
from app.routers.votes import router as votes_router_arpon

from app.routers.comment_votes import router as votes_router_emon
from app.routers.comment_routes import router as moderation_router
from app.routers.comment_updates import router as comments_router_emon

from app.routers.messages import router as messages_router
from app.routers.files import router as files_router
from app.routers.communities import router as communities_router

__all__ = [
    "auth_router",
    "posts_router",
    "users_router",
    "votes_router_arpon",
    "votes_router_emon",
    "comments_router",
    "comments_router_emon",
    "messages_router",
    "files_router",
    "moderation_router",
    "communities_router",
]
