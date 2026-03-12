"""Issue repository"""

from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.issue import Issue


class IssueRepository:
    """Repository for Issue model"""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, issue_id: int) -> Optional[Issue]:
        """Get issue by ID"""
        return self.db.query(Issue).filter(Issue.id == issue_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Issue]:
        """Get all issues with pagination"""
        return self.db.query(Issue).offset(skip).limit(limit).all()

    def get_by_project(self, project_id: int, skip: int = 0, limit: int = 100) -> List[Issue]:
        """Get issues by project"""
        return (
            self.db.query(Issue)
            .filter(Issue.project_id == project_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_creator(self, creator_id: int, skip: int = 0, limit: int = 100) -> List[Issue]:
        """Get issues by creator"""
        return (
            self.db.query(Issue)
            .filter(Issue.creator_id == creator_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_assignee(self, assignee_id: int, skip: int = 0, limit: int = 100) -> List[Issue]:
        """Get issues by assignee"""
        return (
            self.db.query(Issue)
            .filter(Issue.assignee_id == assignee_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[Issue]:
        """Get issues by status"""
        return self.db.query(Issue).filter(Issue.status == status).offset(skip).limit(limit).all()

    def create(self, issue: Issue) -> Issue:
        """Create a new issue"""
        self.db.add(issue)
        self.db.commit()
        self.db.refresh(issue)
        return issue

    def update(self, issue: Issue) -> Issue:
        """Update an existing issue"""
        self.db.commit()
        self.db.refresh(issue)
        return issue

    def delete(self, issue: Issue) -> None:
        """Delete an issue"""
        self.db.delete(issue)
        self.db.commit()
