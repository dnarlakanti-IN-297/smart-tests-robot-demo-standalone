"""Authentication routes"""

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.token import Token
from app.schemas.user import User, UserCreate, UserLogin
from app.services.auth_service import AuthService
from app.services.user_service import UserService

router = APIRouter()


@router.post("/register", response_model=User, status_code=201)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    user_service = UserService(db)
    return user_service.create(user_data)


@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Login and get access token"""
    auth_service = AuthService(db)
    return auth_service.login(credentials)


@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """OAuth2 compatible token login (for OpenAPI docs)"""
    auth_service = AuthService(db)
    credentials = UserLogin(username=form_data.username, password=form_data.password)
    return auth_service.login(credentials)
