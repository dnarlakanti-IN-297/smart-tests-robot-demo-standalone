"""Integration tests for tags API"""

import pytest


@pytest.mark.integration
class TestTagsAPI:
    """Test cases for tag endpoints"""

    def test_create_tag(self, client, auth_headers):
        """Test creating a tag"""
        response = client.post(
            "/api/tags",
            json={"name": "new-tag", "color": "#FF5733"},
            headers=auth_headers,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "new-tag"
        assert data["color"] == "#FF5733"

    def test_create_tag_without_auth(self, client):
        """Test creating tag without authentication fails"""
        response = client.post(
            "/api/tags",
            json={"name": "unauthorized-tag", "color": "#FF0000"},
        )

        assert response.status_code == 401

    def test_create_tag_duplicate_name(self, client, auth_headers, test_tag):
        """Test creating tag with duplicate name fails"""
        response = client.post(
            "/api/tags",
            json={"name": test_tag.name, "color": "#FF0000"},
            headers=auth_headers,
        )

        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]

    def test_create_tag_invalid_color(self, client, auth_headers):
        """Test creating tag with invalid color fails"""
        response = client.post(
            "/api/tags",
            json={"name": "invalid-color", "color": "not-a-color"},
            headers=auth_headers,
        )

        assert response.status_code == 422

    def test_create_tag_default_color(self, client, auth_headers):
        """Test creating tag with default color"""
        response = client.post(
            "/api/tags",
            json={"name": "default-color-tag"},
            headers=auth_headers,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["color"] == "#6B7280"  # Default color

    def test_get_all_tags(self, client, auth_headers, test_tag):
        """Test getting all tags"""
        response = client.get("/api/tags", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert any(tag["id"] == test_tag.id for tag in data)

    def test_get_tags_without_auth(self, client):
        """Test getting tags without authentication fails"""
        response = client.get("/api/tags")

        assert response.status_code == 401

    def test_delete_tag(self, client, auth_headers, test_tag):
        """Test deleting a tag"""
        response = client.delete(f"/api/tags/{test_tag.id}", headers=auth_headers)

        assert response.status_code == 204

        # Verify tag is deleted
        response = client.get("/api/tags", headers=auth_headers)
        data = response.json()
        assert not any(tag["id"] == test_tag.id for tag in data)

    def test_delete_tag_not_found(self, client, auth_headers):
        """Test deleting non-existent tag"""
        response = client.delete("/api/tags/99999", headers=auth_headers)

        assert response.status_code == 404

    def test_delete_tag_without_auth(self, client, test_tag):
        """Test deleting tag without authentication fails"""
        response = client.delete(f"/api/tags/{test_tag.id}")

        assert response.status_code == 401
