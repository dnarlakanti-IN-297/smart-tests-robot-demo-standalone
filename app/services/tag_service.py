"""Tag service"""

from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.tag import Tag
from app.repositories.tag_repository import TagRepository
from app.schemas.tag import TagCreate


class TagService:
    """Service for tag operations"""

    def __init__(self, db: Session):
        self.db = db
        self.repo = TagRepository(db)

    def get_by_id(self, tag_id: int) -> Tag:
        """Get tag by ID"""
        tag = self.repo.get_by_id(tag_id)
        if not tag:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tag not found",
            )
        return tag

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Tag]:
        """Get all tags"""
        return self.repo.get_all(skip, limit)

    def create(self, tag_data: TagCreate) -> Tag:
        """Create a new tag"""
        # Check if tag name already exists
        if self.repo.get_by_name(tag_data.name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tag with this name already exists",
            )

        tag = Tag(name=tag_data.name, color=tag_data.color)
        return self.repo.create(tag)

    def delete(self, tag_id: int) -> None:
        """Delete a tag"""
        tag = self.get_by_id(tag_id)
        self.repo.delete(tag)
