"""Project routes"""

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_active_user
from app.database import get_db
from app.models.user import User
from app.schemas.project import Project, ProjectCreate, ProjectMember, ProjectMemberCreate, ProjectUpdate
from app.services.project_service import ProjectService

router = APIRouter()


@router.get("", response_model=List[Project])
def get_projects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get all projects for current user"""
    project_service = ProjectService(db)
    return project_service.get_user_projects(current_user.id, skip, limit)


@router.post("", response_model=Project, status_code=201)
def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Create a new project"""
    project_service = ProjectService(db)
    return project_service.create(project_data, current_user)


@router.get("/{project_id}", response_model=Project)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get project by ID"""
    project_service = ProjectService(db)
    project = project_service.get_by_id(project_id)

    # Check access
    if not project_service.check_access(project_id, current_user.id):
        from fastapi import HTTPException, status

        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    return project


@router.put("/{project_id}", response_model=Project)
def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Update project"""
    project_service = ProjectService(db)
    return project_service.update(project_id, project_data, current_user)


@router.delete("/{project_id}", status_code=204)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Delete project"""
    project_service = ProjectService(db)
    project_service.delete(project_id, current_user)


@router.post("/{project_id}/members", response_model=ProjectMember, status_code=201)
def add_project_member(
    project_id: int,
    member_data: ProjectMemberCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Add a member to project"""
    project_service = ProjectService(db)
    return project_service.add_member(project_id, member_data, current_user)


@router.delete("/{project_id}/members/{user_id}", status_code=204)
def remove_project_member(
    project_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Remove a member from project"""
    project_service = ProjectService(db)
    project_service.remove_member(project_id, user_id, current_user)
