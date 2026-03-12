"""Integration tests for issues API"""

import pytest


@pytest.mark.integration
class TestIssuesAPI:
    """Test cases for issue endpoints"""

    def test_create_issue(self, client, auth_headers, test_project):
        """Test creating an issue"""
        response = client.post(
            "/api/issues",
            json={
                "title": "New Bug",
                "description": "Found a bug",
                "status": "open",
                "type": "bug",
                "priority": "high",
                "project_id": test_project.id,
            },
            headers=auth_headers,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "New Bug"
        assert data["description"] == "Found a bug"
        assert data["status"] == "open"
        assert data["type"] == "bug"
        assert data["priority"] == "high"

    def test_create_issue_without_auth(self, client, test_project):
        """Test creating issue without authentication fails"""
        response = client.post(
            "/api/issues",
            json={
                "title": "New Issue",
                "project_id": test_project.id,
            },
        )

        assert response.status_code == 401

    def test_create_issue_without_access(self, client, test_project, test_user2):
        """Test creating issue without project access fails"""
        # Login as user2
        login_response = client.post(
            "/api/auth/login",
            json={"username": test_user2.username, "password": "password123"},
        )
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = client.post(
            "/api/issues",
            json={
                "title": "Unauthorized Issue",
                "project_id": test_project.id,
            },
            headers=headers,
        )

        assert response.status_code == 403

    def test_get_all_issues(self, client, auth_headers, test_issue):
        """Test getting all issues"""
        response = client.get("/api/issues", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_get_issues_by_project(self, client, auth_headers, test_project, test_issue):
        """Test getting issues filtered by project"""
        response = client.get(
            f"/api/issues?project_id={test_project.id}",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert all(issue["project_id"] == test_project.id for issue in data)

    def test_get_my_issues(self, client, auth_headers, test_issue):
        """Test getting issues assigned to current user"""
        response = client.get("/api/issues/me", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_issue_by_id(self, client, auth_headers, test_issue):
        """Test getting issue by ID"""
        response = client.get(f"/api/issues/{test_issue.id}", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_issue.id
        assert data["title"] == test_issue.title
        assert data["description"] == test_issue.description

    def test_get_issue_not_found(self, client, auth_headers):
        """Test getting non-existent issue"""
        response = client.get("/api/issues/99999", headers=auth_headers)

        assert response.status_code == 404

    def test_update_issue(self, client, auth_headers, test_issue):
        """Test updating issue"""
        response = client.put(
            f"/api/issues/{test_issue.id}",
            json={
                "title": "Updated Title",
                "status": "in_progress",
                "priority": "critical",
            },
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["status"] == "in_progress"
        assert data["priority"] == "critical"

    def test_update_issue_status(self, client, auth_headers, test_issue):
        """Test updating issue status"""
        response = client.put(
            f"/api/issues/{test_issue.id}",
            json={"status": "resolved"},
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "resolved"

    def test_update_issue_without_access(self, client, test_issue, test_user2):
        """Test updating issue without access fails"""
        # Login as user2
        login_response = client.post(
            "/api/auth/login",
            json={"username": test_user2.username, "password": "password123"},
        )
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = client.put(
            f"/api/issues/{test_issue.id}",
            json={"title": "Hacked Title"},
            headers=headers,
        )

        assert response.status_code == 403

    def test_delete_issue(self, client, auth_headers, test_issue):
        """Test deleting issue"""
        response = client.delete(f"/api/issues/{test_issue.id}", headers=auth_headers)

        assert response.status_code == 204

        # Verify issue is deleted
        response = client.get(f"/api/issues/{test_issue.id}", headers=auth_headers)
        assert response.status_code == 404

    def test_delete_issue_without_permission(self, client, test_issue, test_user2):
        """Test deleting issue without permission fails"""
        # Login as user2
        login_response = client.post(
            "/api/auth/login",
            json={"username": test_user2.username, "password": "password123"},
        )
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = client.delete(f"/api/issues/{test_issue.id}", headers=headers)

        assert response.status_code == 403

    def test_create_issue_with_assignment(self, client, auth_headers, test_project, test_user):
        """Test creating issue with assignee"""
        response = client.post(
            "/api/issues",
            json={
                "title": "Assigned Issue",
                "project_id": test_project.id,
                "assignee_id": test_user.id,
            },
            headers=auth_headers,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["assignee_id"] == test_user.id

    def test_create_issue_with_tags(self, client, auth_headers, test_project, test_tag):
        """Test creating issue with tags"""
        response = client.post(
            "/api/issues",
            json={
                "title": "Tagged Issue",
                "project_id": test_project.id,
                "tag_ids": [test_tag.id],
            },
            headers=auth_headers,
        )

        assert response.status_code == 201
