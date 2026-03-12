"""User routes"""

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_active_user
from app.database import get_db
from app.models.user import User as UserModel
from app.schemas.user import User, UserUpdate
from app.services.user_service import UserService

router = APIRouter()


@router.get("/me", response_model=User)
def get_current_user(current_user: UserModel = Depends(get_current_active_user)):
    """Get current user"""
    return current_user


@router.get("", response_model=List[User])
def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user),
):
    """Get all users"""
    user_service = UserService(db)
    return user_service.get_all(skip, limit)


@router.get("/{user_id}", response_model=User)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user),
):
    """Get user by ID"""
    user_service = UserService(db)
    return user_service.get_by_id(user_id)


@router.put("/{user_id}", response_model=User)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user),
):
    """Update user"""
    user_service = UserService(db)
    return user_service.update(user_id, user_data)


@router.delete("/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user),
):
    """Delete user"""
    user_service = UserService(db)
    user_service.delete(user_id)
