"""Integration tests for projects API"""

import pytest


@pytest.mark.integration
class TestProjectsAPI:
    """Test cases for project endpoints"""

    def test_create_project(self, client, auth_headers):
        """Test creating a project"""
        response = client.post(
            "/api/projects",
            json={
                "name": "New Project",
                "key": "NP",
                "description": "A new project",
            },
            headers=auth_headers,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "New Project"
        assert data["key"] == "NP"
        assert data["description"] == "A new project"

    def test_create_project_without_auth(self, client):
        """Test creating project without authentication fails"""
        response = client.post(
            "/api/projects",
            json={"name": "New Project", "key": "NP"},
        )

        assert response.status_code == 401

    def test_create_project_duplicate_key(self, client, auth_headers, test_project):
        """Test creating project with duplicate key fails"""
        response = client.post(
            "/api/projects",
            json={
                "name": "Another Project",
                "key": test_project.key,
                "description": "Duplicate key",
            },
            headers=auth_headers,
        )

        assert response.status_code == 400
        assert "Project key already exists" in response.json()["detail"]

    def test_create_project_invalid_key(self, client, auth_headers):
        """Test creating project with invalid key fails"""
        response = client.post(
            "/api/projects",
            json={
                "name": "New Project",
                "key": "invalid-key",  # lowercase not allowed
                "description": "Invalid key",
            },
            headers=auth_headers,
        )

        assert response.status_code == 422

    def test_get_user_projects(self, client, auth_headers, test_project):
        """Test getting user's projects"""
        response = client.get("/api/projects", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert any(p["id"] == test_project.id for p in data)

    def test_get_project_by_id(self, client, auth_headers, test_project):
        """Test getting project by ID"""
        response = client.get(f"/api/projects/{test_project.id}", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_project.id
        assert data["name"] == test_project.name

    def test_get_project_without_access(self, client, test_project, test_user2):
        """Test getting project without access fails"""
        # Login as user2
        login_response = client.post(
            "/api/auth/login",
            json={"username": test_user2.username, "password": "password123"},
        )
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = client.get(f"/api/projects/{test_project.id}", headers=headers)

        assert response.status_code == 403

    def test_update_project(self, client, auth_headers, test_project):
        """Test updating project"""
        response = client.put(
            f"/api/projects/{test_project.id}",
            json={"name": "Updated Name", "description": "Updated description"},
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"
        assert data["description"] == "Updated description"

    def test_update_project_without_permission(self, client, test_project, test_user2):
        """Test updating project without permission fails"""
        # Login as user2
        login_response = client.post(
            "/api/auth/login",
            json={"username": test_user2.username, "password": "password123"},
        )
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = client.put(
            f"/api/projects/{test_project.id}",
            json={"name": "Hacked Name"},
            headers=headers,
        )

        assert response.status_code == 403

    def test_delete_project(self, client, auth_headers, test_project):
        """Test deleting project"""
        response = client.delete(f"/api/projects/{test_project.id}", headers=auth_headers)

        assert response.status_code == 204

        # Verify project is deleted
        response = client.get(f"/api/projects/{test_project.id}", headers=auth_headers)
        assert response.status_code == 404

    def test_add_project_member(self, client, auth_headers, test_project, test_user2):
        """Test adding member to project"""
        response = client.post(
            f"/api/projects/{test_project.id}/members",
            json={"user_id": test_user2.id, "role": "member"},
            headers=auth_headers,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["user_id"] == test_user2.id
        assert data["project_id"] == test_project.id

    def test_remove_project_member(self, client, auth_headers, test_project, test_user2):
        """Test removing member from project"""
        # First add member
        client.post(
            f"/api/projects/{test_project.id}/members",
            json={"user_id": test_user2.id, "role": "member"},
            headers=auth_headers,
        )

        # Then remove
        response = client.delete(
            f"/api/projects/{test_project.id}/members/{test_user2.id}",
            headers=auth_headers,
        )

        assert response.status_code == 204

    def test_get_project_not_found(self, client, auth_headers):
        """Test getting non-existent project"""
        response = client.get("/api/projects/99999", headers=auth_headers)

        assert response.status_code == 404
