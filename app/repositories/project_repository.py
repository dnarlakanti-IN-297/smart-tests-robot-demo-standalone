"""Project repository"""

from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.project import Project, ProjectMember


class ProjectRepository:
    """Repository for Project model"""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, project_id: int) -> Optional[Project]:
        """Get project by ID"""
        return self.db.query(Project).filter(Project.id == project_id).first()

    def get_by_key(self, key: str) -> Optional[Project]:
        """Get project by key"""
        return self.db.query(Project).filter(Project.key == key).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Project]:
        """Get all projects with pagination"""
        return self.db.query(Project).offset(skip).limit(limit).all()

    def get_user_projects(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Project]:
        """Get projects where user is a member"""
        return (
            self.db.query(Project)
            .join(ProjectMember)
            .filter(ProjectMember.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, project: Project) -> Project:
        """Create a new project"""
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def update(self, project: Project) -> Project:
        """Update an existing project"""
        self.db.commit()
        self.db.refresh(project)
        return project

    def delete(self, project: Project) -> None:
        """Delete a project"""
        self.db.delete(project)
        self.db.commit()

    def get_member(self, project_id: int, user_id: int) -> Optional[ProjectMember]:
        """Get project member"""
        return (
            self.db.query(ProjectMember)
            .filter(ProjectMember.project_id == project_id, ProjectMember.user_id == user_id)
            .first()
        )

    def add_member(self, member: ProjectMember) -> ProjectMember:
        """Add a member to project"""
        self.db.add(member)
        self.db.commit()
        self.db.refresh(member)
        return member

    def remove_member(self, member: ProjectMember) -> None:
        """Remove a member from project"""
        self.db.delete(member)
        self.db.commit()

    def is_member(self, project_id: int, user_id: int) -> bool:
        """Check if user is a member of project"""
        return self.get_member(project_id, user_id) is not None
