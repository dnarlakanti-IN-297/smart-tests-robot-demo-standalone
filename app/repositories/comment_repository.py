"""Comment repository"""

from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.comment import Comment


class CommentRepository:
    """Repository for Comment model"""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, comment_id: int) -> Optional[Comment]:
        """Get comment by ID"""
        return self.db.query(Comment).filter(Comment.id == comment_id).first()

    def get_by_issue(self, issue_id: int, skip: int = 0, limit: int = 100) -> List[Comment]:
        """Get comments by issue"""
        return (
            self.db.query(Comment)
            .filter(Comment.issue_id == issue_id)
            .order_by(Comment.created_at)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, comment: Comment) -> Comment:
        """Create a new comment"""
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def update(self, comment: Comment) -> Comment:
        """Update an existing comment"""
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def delete(self, comment: Comment) -> None:
        """Delete a comment"""
        self.db.delete(comment)
        self.db.commit()
