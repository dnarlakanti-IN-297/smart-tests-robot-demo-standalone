"""Unit tests for AuthService"""

import pytest
from fastapi import HTTPException

from app.schemas.user import UserLogin
from app.services.auth_service import AuthService


@pytest.mark.unit
class TestAuthService:
    """Test cases for AuthService"""

    def test_login_success(self, db_session, test_user):
        """Test successful login"""
        service = AuthService(db_session)
        credentials = UserLogin(username=test_user.username, password="password123")

        token = service.login(credentials)

        assert token.access_token is not None
        assert token.token_type == "bearer"

    def test_login_invalid_username(self, db_session):
        """Test login with invalid username fails"""
        service = AuthService(db_session)
        credentials = UserLogin(username="nonexistent", password="password123")

        with pytest.raises(HTTPException) as exc_info:
            service.login(credentials)

        assert exc_info.value.status_code == 401
        assert "Incorrect username or password" in str(exc_info.value.detail)

    def test_login_invalid_password(self, db_session, test_user):
        """Test login with invalid password fails"""
        service = AuthService(db_session)
        credentials = UserLogin(username=test_user.username, password="wrongpassword")

        with pytest.raises(HTTPException) as exc_info:
            service.login(credentials)

        assert exc_info.value.status_code == 401
        assert "Incorrect username or password" in str(exc_info.value.detail)

    def test_login_inactive_user(self, db_session, test_user):
        """Test login with inactive user fails"""
        # Mark user as inactive
        test_user.is_active = False
        db_session.commit()

        service = AuthService(db_session)
        credentials = UserLogin(username=test_user.username, password="password123")

        with pytest.raises(HTTPException) as exc_info:
            service.login(credentials)

        assert exc_info.value.status_code == 400
        assert "Inactive user" in str(exc_info.value.detail)
