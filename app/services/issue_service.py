"""Issue service"""

from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.issue import Issue
from app.models.user import User
from app.repositories.issue_repository import IssueRepository
from app.repositories.tag_repository import TagRepository
from app.schemas.issue import IssueCreate, IssueUpdate
from app.services.project_service import ProjectService


class IssueService:
    """Service for issue operations"""

    def __init__(self, db: Session):
        self.db = db
        self.repo = IssueRepository(db)
        self.tag_repo = TagRepository(db)
        self.project_service = ProjectService(db)

    def get_by_id(self, issue_id: int) -> Issue:
        """Get issue by ID"""
        issue = self.repo.get_by_id(issue_id)
        if not issue:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Issue not found",
            )
        return issue

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Issue]:
        """Get all issues"""
        return self.repo.get_all(skip, limit)

    def get_by_project(self, project_id: int, skip: int = 0, limit: int = 100) -> List[Issue]:
        """Get issues by project"""
        return self.repo.get_by_project(project_id, skip, limit)

    def get_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Issue]:
        """Get issues assigned to user"""
        return self.repo.get_by_assignee(user_id, skip, limit)

    def create(self, issue_data: IssueCreate, creator: User) -> Issue:
        """Create a new issue"""
        # Check if user has access to project
        if not self.project_service.check_access(issue_data.project_id, creator.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to this project",
            )

        # Create issue
        issue = Issue(
            title=issue_data.title,
            description=issue_data.description,
            status=issue_data.status,
            type=issue_data.type,
            priority=issue_data.priority,
            project_id=issue_data.project_id,
            creator_id=creator.id,
            assignee_id=issue_data.assignee_id,
        )

        # Add tags if provided
        if issue_data.tag_ids:
            tags = self.tag_repo.get_by_ids(issue_data.tag_ids)
            issue.tags = tags

        return self.repo.create(issue)

    def update(self, issue_id: int, issue_data: IssueUpdate, user: User) -> Issue:
        """Update an issue"""
        issue = self.get_by_id(issue_id)

        # Check if user has access to project
        if not self.project_service.check_access(issue.project_id, user.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to this project",
            )

        # Update fields
        if issue_data.title:
            issue.title = issue_data.title
        if issue_data.description is not None:
            issue.description = issue_data.description
        if issue_data.status:
            issue.status = issue_data.status
        if issue_data.type:
            issue.type = issue_data.type
        if issue_data.priority:
            issue.priority = issue_data.priority
        if issue_data.assignee_id is not None:
            issue.assignee_id = issue_data.assignee_id

        # Update tags if provided
        if issue_data.tag_ids is not None:
            tags = self.tag_repo.get_by_ids(issue_data.tag_ids)
            issue.tags = tags

        return self.repo.update(issue)

    def delete(self, issue_id: int, user: User) -> None:
        """Delete an issue"""
        issue = self.get_by_id(issue_id)

        # Check if user is creator or has access to project
        if issue.creator_id != user.id and not self.project_service.check_access(issue.project_id, user.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to delete this issue",
            )

        self.repo.delete(issue)
