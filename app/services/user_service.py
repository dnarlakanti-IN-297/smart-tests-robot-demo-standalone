"""User service"""

from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.auth.password import get_password_hash
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    """Service for user operations"""

    def __init__(self, db: Session):
        self.db = db
        self.repo = UserRepository(db)

    def get_by_id(self, user_id: int) -> User:
        """Get user by ID"""
        user = self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        return self.repo.get_by_username(username)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users"""
        return self.repo.get_all(skip, limit)

    def create(self, user_data: UserCreate) -> User:
        """Create a new user"""
        # Check if email already exists
        if self.repo.get_by_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        # Check if username already exists
        if self.repo.get_by_username(user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken",
            )

        # Create user with hashed password
        user = User(
            email=user_data.email,
            username=user_data.username,
            full_name=user_data.full_name,
            hashed_password=get_password_hash(user_data.password),
        )

        return self.repo.create(user)

    def update(self, user_id: int, user_data: UserUpdate) -> User:
        """Update a user"""
        user = self.get_by_id(user_id)

        # Update email if provided and different
        if user_data.email and user_data.email != user.email:
            existing_user = self.repo.get_by_email(user_data.email)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered",
                )
            user.email = user_data.email

        # Update other fields
        if user_data.full_name:
            user.full_name = user_data.full_name

        if user_data.password:
            user.hashed_password = get_password_hash(user_data.password)

        return self.repo.update(user)

    def delete(self, user_id: int) -> None:
        """Delete a user"""
        user = self.get_by_id(user_id)
        self.repo.delete(user)
