"""Tag routes"""

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_active_user
from app.database import get_db
from app.models.user import User
from app.schemas.tag import Tag, TagCreate
from app.services.tag_service import TagService

router = APIRouter()


@router.get("", response_model=List[Tag])
def get_tags(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get all tags"""
    tag_service = TagService(db)
    return tag_service.get_all(skip, limit)


@router.post("", response_model=Tag, status_code=201)
def create_tag(
    tag_data: TagCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Create a new tag"""
    tag_service = TagService(db)
    return tag_service.create(tag_data)


@router.delete("/{tag_id}", status_code=204)
def delete_tag(
    tag_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Delete tag"""
    tag_service = TagService(db)
    tag_service.delete(tag_id)
