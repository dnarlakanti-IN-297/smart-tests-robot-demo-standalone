"""Authentication service"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.auth.jwt import create_access_token
from app.auth.password import verify_password
from app.repositories.user_repository import UserRepository
from app.schemas.token import Token
from app.schemas.user import UserLogin


class AuthService:
    """Service for authentication operations"""

    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def login(self, credentials: UserLogin) -> Token:
        """Authenticate user and return JWT token"""
        user = self.user_repo.get_by_username(credentials.username)

        if not user or not verify_password(credentials.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user",
            )

        # Create access token
        access_token = create_access_token(data={"sub": user.username, "user_id": user.id})

        return Token(access_token=access_token, token_type="bearer")
