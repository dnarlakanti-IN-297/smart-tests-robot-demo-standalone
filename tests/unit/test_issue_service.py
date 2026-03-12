"""Unit tests for IssueService"""

import pytest
from fastapi import HTTPException

from app.models.issue import IssuePriority, IssueStatus, IssueType
from app.schemas.issue import IssueCreate, IssueUpdate
from app.services.issue_service import IssueService


@pytest.mark.unit
class TestIssueService:
    """Test cases for IssueService"""

    def test_create_issue(self, db_session, test_project, test_user):
        """Test creating a new issue"""
        service = IssueService(db_session)
        issue_data = IssueCreate(
            title="New Issue",
            description="Issue description",
            status=IssueStatus.OPEN.value,
            type=IssueType.BUG.value,
            priority=IssuePriority.HIGH.value,
            project_id=test_project.id,
        )

        issue = service.create(issue_data, test_user)

        assert issue.id is not None
        assert issue.title == "New Issue"
        assert issue.description == "Issue description"
        assert issue.status == IssueStatus.OPEN.value
        assert issue.creator_id == test_user.id

    def test_create_issue_no_access(self, db_session, test_project, test_user2):
        """Test creating issue without project access fails"""
        service = IssueService(db_session)
        issue_data = IssueCreate(
            title="Unauthorized Issue",
            project_id=test_project.id,
        )

        with pytest.raises(HTTPException) as exc_info:
            service.create(issue_data, test_user2)

        assert exc_info.value.status_code == 403

    def test_get_issue_by_id(self, db_session, test_issue):
        """Test getting issue by ID"""
        service = IssueService(db_session)

        issue = service.get_by_id(test_issue.id)

        assert issue.id == test_issue.id
        assert issue.title == test_issue.title

    def test_get_issue_by_id_not_found(self, db_session):
        """Test getting non-existent issue raises exception"""
        service = IssueService(db_session)

        with pytest.raises(HTTPException) as exc_info:
            service.get_by_id(99999)

        assert exc_info.value.status_code == 404

    def test_get_all_issues(self, db_session, test_issue):
        """Test getting all issues"""
        service = IssueService(db_session)

        issues = service.get_all()

        assert len(issues) >= 1
        assert test_issue.id in [i.id for i in issues]

    def test_get_issues_by_project(self, db_session, test_project, test_issue):
        """Test getting issues by project"""
        service = IssueService(db_session)

        issues = service.get_by_project(test_project.id)

        assert len(issues) >= 1
        assert all(i.project_id == test_project.id for i in issues)

    def test_get_issues_by_user(self, db_session, test_user, test_issue):
        """Test getting issues assigned to user"""
        service = IssueService(db_session)

        issues = service.get_by_user(test_user.id)

        assert len(issues) >= 1
        assert all(i.assignee_id == test_user.id for i in issues)

    def test_update_issue(self, db_session, test_issue, test_user):
        """Test updating issue"""
        service = IssueService(db_session)
        update_data = IssueUpdate(
            title="Updated Title",
            status=IssueStatus.IN_PROGRESS.value,
        )

        updated_issue = service.update(test_issue.id, update_data, test_user)

        assert updated_issue.title == "Updated Title"
        assert updated_issue.status == IssueStatus.IN_PROGRESS.value

    def test_update_issue_no_access(self, db_session, test_issue, test_user2):
        """Test updating issue without access fails"""
        service = IssueService(db_session)
        update_data = IssueUpdate(title="Hacked Title")

        with pytest.raises(HTTPException) as exc_info:
            service.update(test_issue.id, update_data, test_user2)

        assert exc_info.value.status_code == 403

    def test_delete_issue_as_creator(self, db_session, test_issue, test_user):
        """Test deleting issue as creator"""
        service = IssueService(db_session)

        service.delete(test_issue.id, test_user)

        with pytest.raises(HTTPException):
            service.get_by_id(test_issue.id)

    def test_delete_issue_no_permission(self, db_session, test_issue, test_user2):
        """Test deleting issue without permission fails"""
        service = IssueService(db_session)

        with pytest.raises(HTTPException) as exc_info:
            service.delete(test_issue.id, test_user2)

        assert exc_info.value.status_code == 403

    def test_create_issue_with_tags(self, db_session, test_project, test_user, test_tag):
        """Test creating issue with tags"""
        service = IssueService(db_session)
        issue_data = IssueCreate(
            title="Tagged Issue",
            project_id=test_project.id,
            tag_ids=[test_tag.id],
        )

        issue = service.create(issue_data, test_user)

        assert len(issue.tags) == 1
        assert issue.tags[0].id == test_tag.id
