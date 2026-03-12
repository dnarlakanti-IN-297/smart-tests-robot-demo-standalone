"""Comment routes"""

from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_active_user
from app.database import get_db
from app.models.user import User
from app.schemas.comment import Comment, CommentCreate, CommentUpdate
from app.services.comment_service import CommentService

router = APIRouter()


@router.get("", response_model=List[Comment])
def get_comments(
    issue_id: int = Query(...),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get comments for an issue"""
    comment_service = CommentService(db)
    return comment_service.get_by_issue(issue_id, skip, limit)


@router.post("", response_model=Comment, status_code=201)
def create_comment(
    comment_data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Create a new comment"""
    comment_service = CommentService(db)
    return comment_service.create(comment_data, current_user)


@router.put("/{comment_id}", response_model=Comment)
def update_comment(
    comment_id: int,
    comment_data: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Update comment"""
    comment_service = CommentService(db)
    return comment_service.update(comment_id, comment_data, current_user)


@router.delete("/{comment_id}", status_code=204)
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Delete comment"""
    comment_service = CommentService(db)
    comment_service.delete(comment_id, current_user)
