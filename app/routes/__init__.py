"""API routes"""

from fastapi import APIRouter

from app.routes import auth, comments, issues, projects, tags, users, web

api_router = APIRouter(prefix="/api")

# API routes
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(projects.router, prefix="/projects", tags=["Projects"])
api_router.include_router(issues.router, prefix="/issues", tags=["Issues"])
api_router.include_router(comments.router, prefix="/comments", tags=["Comments"])
api_router.include_router(tags.router, prefix="/tags", tags=["Tags"])

# Web routes (templates)
web_router = web.router

__all__ = ["api_router", "web_router"]
