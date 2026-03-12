"""Tag repository"""

from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.tag import Tag


class TagRepository:
    """Repository for Tag model"""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, tag_id: int) -> Optional[Tag]:
        """Get tag by ID"""
        return self.db.query(Tag).filter(Tag.id == tag_id).first()

    def get_by_name(self, name: str) -> Optional[Tag]:
        """Get tag by name"""
        return self.db.query(Tag).filter(Tag.name == name).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Tag]:
        """Get all tags with pagination"""
        return self.db.query(Tag).offset(skip).limit(limit).all()

    def get_by_ids(self, tag_ids: List[int]) -> List[Tag]:
        """Get tags by list of IDs"""
        return self.db.query(Tag).filter(Tag.id.in_(tag_ids)).all()

    def create(self, tag: Tag) -> Tag:
        """Create a new tag"""
        self.db.add(tag)
        self.db.commit()
        self.db.refresh(tag)
        return tag

    def delete(self, tag: Tag) -> None:
        """Delete a tag"""
        self.db.delete(tag)
        self.db.commit()
