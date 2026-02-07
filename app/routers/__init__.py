"""Router exports."""

# Shihab (2303147) - Auth, Users, Comments (GET, POST)
from app.routers.r_2303147_auth import router as auth_router
from app.routers.r_2303147_users import router as users_router
from app.routers.r_2303147_comments import router as comments_router

# Arpon (2303134) - Posts, Votes (POST, DELETE for posts)
from app.routers.r_2303134_posts import router as posts_router
from app.routers.r_2303134_votes import router as votes_router_arpon

# Emon (2303173) - Votes (comment portion), Reports, Comments (PUT, DELETE)
from app.routers.r_2303173_votes import router as votes_router_emon
from app.routers.r_2303173_reports import router as moderation_router
from app.routers.r_2303173_comments import router as comments_router_emon

# Tahsan (2303133) - Messages, Files, WebSockets
from app.routers.r_2303133_messages import router as messages_router
from app.routers.r_2303133_files import router as files_router

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
]
