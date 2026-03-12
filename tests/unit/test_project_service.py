"""Unit tests for ProjectService"""

import pytest
from fastapi import HTTPException

from app.schemas.project import ProjectCreate, ProjectMemberCreate, ProjectUpdate
from app.services.project_service import ProjectService


@pytest.mark.unit
class TestProjectService:
    """Test cases for ProjectService"""

    def test_create_project(self, db_session, test_user):
        """Test creating a new project"""
        service = ProjectService(db_session)
        project_data = ProjectCreate(
            name="New Project",
            key="NP",
            description="A new project",
        )

        project = service.create(project_data, test_user)

        assert project.id is not None
        assert project.name == "New Project"
        assert project.key == "NP"
        assert project.description == "A new project"

    def test_create_project_duplicate_key(self, db_session, test_user, test_project):
        """Test creating project with duplicate key fails"""
        service = ProjectService(db_session)
        project_data = ProjectCreate(
            name="Another Project",
            key=test_project.key,
            description="Duplicate key",
        )

        with pytest.raises(HTTPException) as exc_info:
            service.create(project_data, test_user)

        assert exc_info.value.status_code == 400
        assert "Project key already exists" in str(exc_info.value.detail)

    def test_get_project_by_id(self, db_session, test_project):
        """Test getting project by ID"""
        service = ProjectService(db_session)

        project = service.get_by_id(test_project.id)

        assert project.id == test_project.id
        assert project.name == test_project.name

    def test_get_project_by_id_not_found(self, db_session):
        """Test getting non-existent project raises exception"""
        service = ProjectService(db_session)

        with pytest.raises(HTTPException) as exc_info:
            service.get_by_id(99999)

        assert exc_info.value.status_code == 404

    def test_get_all_projects(self, db_session, test_project):
        """Test getting all projects"""
        service = ProjectService(db_session)

        projects = service.get_all()

        assert len(projects) >= 1
        assert test_project.id in [p.id for p in projects]

    def test_get_user_projects(self, db_session, test_user, test_project):
        """Test getting projects for a user"""
        service = ProjectService(db_session)

        projects = service.get_user_projects(test_user.id)

        assert len(projects) >= 1
        assert test_project.id in [p.id for p in projects]

    def test_update_project(self, db_session, test_project, test_user):
        """Test updating project"""
        service = ProjectService(db_session)
        update_data = ProjectUpdate(name="Updated Name", description="Updated desc")

        updated_project = service.update(test_project.id, update_data, test_user)

        assert updated_project.name == "Updated Name"
        assert updated_project.description == "Updated desc"

    def test_update_project_unauthorized(self, db_session, test_project, test_user2):
        """Test updating project without permission fails"""
        service = ProjectService(db_session)
        update_data = ProjectUpdate(name="Hacked Name")

        with pytest.raises(HTTPException) as exc_info:
            service.update(test_project.id, update_data, test_user2)

        assert exc_info.value.status_code == 403

    def test_delete_project(self, db_session, test_project, test_user):
        """Test deleting project"""
        service = ProjectService(db_session)

        service.delete(test_project.id, test_user)

        with pytest.raises(HTTPException):
            service.get_by_id(test_project.id)

    def test_delete_project_unauthorized(self, db_session, test_project, test_user2):
        """Test deleting project without permission fails"""
        service = ProjectService(db_session)

        with pytest.raises(HTTPException) as exc_info:
            service.delete(test_project.id, test_user2)

        assert exc_info.value.status_code == 403

    def test_add_member(self, db_session, test_project, test_user, test_user2):
        """Test adding member to project"""
        service = ProjectService(db_session)
        member_data = ProjectMemberCreate(user_id=test_user2.id, role="member")

        member = service.add_member(test_project.id, member_data, test_user)

        assert member.user_id == test_user2.id
        assert member.project_id == test_project.id

    def test_add_member_already_exists(self, db_session, test_project, test_user):
        """Test adding existing member fails"""
        service = ProjectService(db_session)
        member_data = ProjectMemberCreate(user_id=test_user.id, role="member")

        with pytest.raises(HTTPException) as exc_info:
            service.add_member(test_project.id, member_data, test_user)

        assert exc_info.value.status_code == 400

    def test_remove_member(self, db_session, test_project, test_user, test_user2):
        """Test removing member from project"""
        service = ProjectService(db_session)

        # First add member
        member_data = ProjectMemberCreate(user_id=test_user2.id, role="member")
        service.add_member(test_project.id, member_data, test_user)

        # Then remove
        service.remove_member(test_project.id, test_user2.id, test_user)

        assert not service.check_access(test_project.id, test_user2.id)

    def test_check_access(self, db_session, test_project, test_user):
        """Test checking user access to project"""
        service = ProjectService(db_session)

        has_access = service.check_access(test_project.id, test_user.id)

        assert has_access is True

    def test_check_access_no_permission(self, db_session, test_project, test_user2):
        """Test checking access for non-member"""
        service = ProjectService(db_session)

        has_access = service.check_access(test_project.id, test_user2.id)

        assert has_access is False
