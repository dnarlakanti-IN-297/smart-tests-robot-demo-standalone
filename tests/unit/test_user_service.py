"""Unit tests for UserService"""

import pytest
from fastapi import HTTPException

from app.schemas.user import UserCreate, UserUpdate
from app.services.user_service import UserService


@pytest.mark.unit
class TestUserService:
    """Test cases for UserService"""

    def test_create_user(self, db_session):
        """Test creating a new user"""
        service = UserService(db_session)
        user_data = UserCreate(
            email="newuser@example.com",
            username="newuser",
            full_name="New User",
            password="password123",
        )

        user = service.create(user_data)

        assert user.id is not None
        assert user.email == "newuser@example.com"
        assert user.username == "newuser"
        assert user.full_name == "New User"
        assert user.hashed_password is not None
        assert user.is_active is True

    def test_create_user_duplicate_email(self, db_session, test_user):
        """Test creating user with duplicate email fails"""
        service = UserService(db_session)
        user_data = UserCreate(
            email=test_user.email,
            username="different",
            full_name="Different User",
            password="password123",
        )

        with pytest.raises(HTTPException) as exc_info:
            service.create(user_data)

        assert exc_info.value.status_code == 400
        assert "Email already registered" in str(exc_info.value.detail)

    def test_create_user_duplicate_username(self, db_session, test_user):
        """Test creating user with duplicate username fails"""
        service = UserService(db_session)
        user_data = UserCreate(
            email="different@example.com",
            username=test_user.username,
            full_name="Different User",
            password="password123",
        )

        with pytest.raises(HTTPException) as exc_info:
            service.create(user_data)

        assert exc_info.value.status_code == 400
        assert "Username already taken" in str(exc_info.value.detail)

    def test_get_user_by_id(self, db_session, test_user):
        """Test getting user by ID"""
        service = UserService(db_session)

        user = service.get_by_id(test_user.id)

        assert user.id == test_user.id
        assert user.email == test_user.email

    def test_get_user_by_id_not_found(self, db_session):
        """Test getting non-existent user raises exception"""
        service = UserService(db_session)

        with pytest.raises(HTTPException) as exc_info:
            service.get_by_id(99999)

        assert exc_info.value.status_code == 404

    def test_get_user_by_username(self, db_session, test_user):
        """Test getting user by username"""
        service = UserService(db_session)

        user = service.get_by_username(test_user.username)

        assert user is not None
        assert user.username == test_user.username

    def test_get_all_users(self, db_session, test_user, test_user2):
        """Test getting all users"""
        service = UserService(db_session)

        users = service.get_all()

        assert len(users) == 2
        assert test_user.id in [u.id for u in users]
        assert test_user2.id in [u.id for u in users]

    def test_update_user(self, db_session, test_user):
        """Test updating user"""
        service = UserService(db_session)
        update_data = UserUpdate(full_name="Updated Name")

        updated_user = service.update(test_user.id, update_data)

        assert updated_user.full_name == "Updated Name"
        assert updated_user.email == test_user.email

    def test_update_user_email(self, db_session, test_user):
        """Test updating user email"""
        service = UserService(db_session)
        update_data = UserUpdate(email="newemail@example.com")

        updated_user = service.update(test_user.id, update_data)

        assert updated_user.email == "newemail@example.com"

    def test_update_user_duplicate_email(self, db_session, test_user, test_user2):
        """Test updating user with duplicate email fails"""
        service = UserService(db_session)
        update_data = UserUpdate(email=test_user2.email)

        with pytest.raises(HTTPException) as exc_info:
            service.update(test_user.id, update_data)

        assert exc_info.value.status_code == 400
        assert "Email already registered" in str(exc_info.value.detail)

    def test_delete_user(self, db_session, test_user):
        """Test deleting user"""
        service = UserService(db_session)

        service.delete(test_user.id)

        with pytest.raises(HTTPException):
            service.get_by_id(test_user.id)
