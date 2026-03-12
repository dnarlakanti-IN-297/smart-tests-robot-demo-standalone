"""Integration tests for comments API"""

import pytest


@pytest.mark.integration
class TestCommentsAPI:
    """Test cases for comment endpoints"""

    def test_create_comment(self, client, auth_headers, test_issue):
        """Test creating a comment"""
        response = client.post(
            "/api/comments",
            json={
                "content": "This is a test comment",
                "issue_id": test_issue.id,
            },
            headers=auth_headers,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["content"] == "This is a test comment"
        assert data["issue_id"] == test_issue.id

    def test_create_comment_without_auth(self, client, test_issue):
        """Test creating comment without authentication fails"""
        response = client.post(
            "/api/comments",
            json={
                "content": "Unauthorized comment",
                "issue_id": test_issue.id,
            },
        )

        assert response.status_code == 401

    def test_create_comment_for_nonexistent_issue(self, client, auth_headers):
        """Test creating comment for non-existent issue fails"""
        response = client.post(
            "/api/comments",
            json={
                "content": "Comment on nothing",
                "issue_id": 99999,
            },
            headers=auth_headers,
        )

        assert response.status_code == 404

    def test_get_comments_by_issue(self, client, auth_headers, test_issue):
        """Test getting comments for an issue"""
        # Create a comment first
        client.post(
            "/api/comments",
            json={
                "content": "Test comment",
                "issue_id": test_issue.id,
            },
            headers=auth_headers,
        )

        # Get comments
        response = client.get(
            f"/api/comments?issue_id={test_issue.id}",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert all(comment["issue_id"] == test_issue.id for comment in data)

    def test_update_comment(self, client, auth_headers, test_issue):
        """Test updating a comment"""
        # Create comment
        create_response = client.post(
            "/api/comments",
            json={
                "content": "Original content",
                "issue_id": test_issue.id,
            },
            headers=auth_headers,
        )
        comment_id = create_response.json()["id"]

        # Update comment
        response = client.put(
            f"/api/comments/{comment_id}",
            json={"content": "Updated content"},
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["content"] == "Updated content"

    def test_update_comment_by_non_author(self, client, test_issue, test_user, test_user2):
        """Test updating comment by non-author fails"""
        # Create comment as user1
        login_response = client.post(
            "/api/auth/login",
            json={"username": test_user.username, "password": "password123"},
        )
        token1 = login_response.json()["access_token"]
        headers1 = {"Authorization": f"Bearer {token1}"}

        create_response = client.post(
            "/api/comments",
            json={
                "content": "User1's comment",
                "issue_id": test_issue.id,
            },
            headers=headers1,
        )
        comment_id = create_response.json()["id"]

        # Try to update as user2
        login_response = client.post(
            "/api/auth/login",
            json={"username": test_user2.username, "password": "password123"},
        )
        token2 = login_response.json()["access_token"]
        headers2 = {"Authorization": f"Bearer {token2}"}

        response = client.put(
            f"/api/comments/{comment_id}",
            json={"content": "Hacked content"},
            headers=headers2,
        )

        assert response.status_code == 403

    def test_delete_comment(self, client, auth_headers, test_issue):
        """Test deleting a comment"""
        # Create comment
        create_response = client.post(
            "/api/comments",
            json={
                "content": "Comment to delete",
                "issue_id": test_issue.id,
            },
            headers=auth_headers,
        )
        comment_id = create_response.json()["id"]

        # Delete comment
        response = client.delete(
            f"/api/comments/{comment_id}",
            headers=auth_headers,
        )

        assert response.status_code == 204

    def test_delete_comment_by_non_author(self, client, test_issue, test_user, test_user2):
        """Test deleting comment by non-author fails"""
        # Create comment as user1
        login_response = client.post(
            "/api/auth/login",
            json={"username": test_user.username, "password": "password123"},
        )
        token1 = login_response.json()["access_token"]
        headers1 = {"Authorization": f"Bearer {token1}"}

        create_response = client.post(
            "/api/comments",
            json={
                "content": "User1's comment",
                "issue_id": test_issue.id,
            },
            headers=headers1,
        )
        comment_id = create_response.json()["id"]

        # Try to delete as user2
        login_response = client.post(
            "/api/auth/login",
            json={"username": test_user2.username, "password": "password123"},
        )
        token2 = login_response.json()["access_token"]
        headers2 = {"Authorization": f"Bearer {token2}"}

        response = client.delete(
            f"/api/comments/{comment_id}",
            headers=headers2,
        )

        assert response.status_code == 403
