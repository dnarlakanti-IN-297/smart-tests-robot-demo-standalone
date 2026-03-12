"""Integration tests for authentication API"""

import pytest


@pytest.mark.integration
class TestAuthAPI:
    """Test cases for authentication endpoints"""

    def test_register_user(self, client):
        """Test user registration"""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "newuser@example.com",
                "username": "newuser",
                "full_name": "New User",
                "password": "password123",
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert data["username"] == "newuser"
        assert "hashed_password" not in data

    def test_register_duplicate_email(self, client, test_user):
        """Test registering with duplicate email fails"""
        response = client.post(
            "/api/auth/register",
            json={
                "email": test_user.email,
                "username": "different",
                "full_name": "Different User",
                "password": "password123",
            },
        )

        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]

    def test_register_duplicate_username(self, client, test_user):
        """Test registering with duplicate username fails"""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "different@example.com",
                "username": test_user.username,
                "full_name": "Different User",
                "password": "password123",
            },
        )

        assert response.status_code == 400
        assert "Username already taken" in response.json()["detail"]

    def test_register_invalid_email(self, client):
        """Test registering with invalid email fails"""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "invalid-email",
                "username": "newuser",
                "full_name": "New User",
                "password": "password123",
            },
        )

        assert response.status_code == 422

    def test_register_short_password(self, client):
        """Test registering with short password fails"""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "newuser@example.com",
                "username": "newuser",
                "full_name": "New User",
                "password": "123",
            },
        )

        assert response.status_code == 422

    def test_login_success(self, client, test_user):
        """Test successful login"""
        response = client.post(
            "/api/auth/login",
            json={"username": test_user.username, "password": "password123"},
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_invalid_username(self, client):
        """Test login with invalid username"""
        response = client.post(
            "/api/auth/login",
            json={"username": "nonexistent", "password": "password123"},
        )

        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]

    def test_login_invalid_password(self, client, test_user):
        """Test login with invalid password"""
        response = client.post(
            "/api/auth/login",
            json={"username": test_user.username, "password": "wrongpassword"},
        )

        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]

    def test_access_protected_endpoint_without_token(self, client):
        """Test accessing protected endpoint without token"""
        response = client.get("/api/users/me")

        assert response.status_code == 401

    def test_access_protected_endpoint_with_token(self, client, auth_headers):
        """Test accessing protected endpoint with valid token"""
        response = client.get("/api/users/me", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert "username" in data
        assert "email" in data

    def test_access_with_invalid_token(self, client):
        """Test accessing with invalid token"""
        response = client.get(
            "/api/users/me",
            headers={"Authorization": "Bearer invalid_token"},
        )

        assert response.status_code == 401
