"""Issue routes"""

from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_active_user
from app.database import get_db
from app.models.user import User
from app.schemas.issue import Issue, IssueCreate, IssueList, IssueUpdate
from app.services.issue_service import IssueService

router = APIRouter()


@router.get("", response_model=List[IssueList])
def get_issues(
    project_id: Optional[int] = Query(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get issues, optionally filtered by project"""
    issue_service = IssueService(db)

    if project_id:
        return issue_service.get_by_project(project_id, skip, limit)

    return issue_service.get_all(skip, limit)


@router.post("", response_model=Issue, status_code=201)
def create_issue(
    issue_data: IssueCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Create a new issue"""
    issue_service = IssueService(db)
    return issue_service.create(issue_data, current_user)


@router.get("/me", response_model=List[IssueList])
def get_my_issues(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get issues assigned to current user"""
    issue_service = IssueService(db)
    return issue_service.get_by_user(current_user.id, skip, limit)


@router.get("/{issue_id}", response_model=Issue)
def get_issue(
    issue_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get issue by ID"""
    issue_service = IssueService(db)
    return issue_service.get_by_id(issue_id)


@router.put("/{issue_id}", response_model=Issue)
def update_issue(
    issue_id: int,
    issue_data: IssueUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Update issue"""
    issue_service = IssueService(db)
    return issue_service.update(issue_id, issue_data, current_user)


@router.delete("/{issue_id}", status_code=204)
def delete_issue(
    issue_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Delete issue"""
    issue_service = IssueService(db)
    issue_service.delete(issue_id, current_user)
