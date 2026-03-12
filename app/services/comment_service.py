"""Comment service"""

from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.comment import Comment
from app.models.user import User
from app.repositories.comment_repository import CommentRepository
from app.schemas.comment import CommentCreate, CommentUpdate
from app.services.issue_service import IssueService


class CommentService:
    """Service for comment operations"""

    def __init__(self, db: Session):
        self.db = db
        self.repo = CommentRepository(db)
        self.issue_service = IssueService(db)

    def get_by_id(self, comment_id: int) -> Comment:
        """Get comment by ID"""
        comment = self.repo.get_by_id(comment_id)
        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment not found",
            )
        return comment

    def get_by_issue(self, issue_id: int, skip: int = 0, limit: int = 100) -> List[Comment]:
        """Get comments for an issue"""
        return self.repo.get_by_issue(issue_id, skip, limit)

    def create(self, comment_data: CommentCreate, author: User) -> Comment:
        """Create a new comment"""
        # Verify issue exists and user has access
        issue = self.issue_service.get_by_id(comment_data.issue_id)

        comment = Comment(
            content=comment_data.content,
            issue_id=comment_data.issue_id,
            author_id=author.id,
        )

        return self.repo.create(comment)

    def update(self, comment_id: int, comment_data: CommentUpdate, user: User) -> Comment:
        """Update a comment"""
        comment = self.get_by_id(comment_id)

        # Only author can update their comment
        if comment.author_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only edit your own comments",
            )

        comment.content = comment_data.content
        return self.repo.update(comment)

    def delete(self, comment_id: int, user: User) -> None:
        """Delete a comment"""
        comment = self.get_by_id(comment_id)

        # Only author can delete their comment
        if comment.author_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only delete your own comments",
            )

        self.repo.delete(comment)
