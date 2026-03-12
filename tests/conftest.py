"""Shared pytest fixtures"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.auth.password import get_password_hash
from app.database import Base, get_db
from app.main import app
from app.models.issue import Issue, IssuePriority, IssueStatus, IssueType
from app.models.project import Project, ProjectMember, ProjectRole
from app.models.tag import Tag
from app.models.user import User, UserRole

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with test database"""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db_session):
    """Create a test user"""
    user = User(
        email="test@example.com",
        username="testuser",
        full_name="Test User",
        hashed_password=get_password_hash("password123"),
        role=UserRole.USER.value,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_admin(db_session):
    """Create a test admin user"""
    admin = User(
        email="admin@example.com",
        username="admin",
        full_name="Admin User",
        hashed_password=get_password_hash("admin123"),
        role=UserRole.ADMIN.value,
    )
    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)
    return admin


@pytest.fixture
def test_user2(db_session):
    """Create a second test user"""
    user = User(
        email="user2@example.com",
        username="user2",
        full_name="User Two",
        hashed_password=get_password_hash("password123"),
        role=UserRole.USER.value,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_project(db_session, test_user):
    """Create a test project"""
    project = Project(
        name="Test Project",
        key="TEST",
        description="A test project",
    )
    db_session.add(project)
    db_session.commit()
    db_session.refresh(project)

    # Add user as owner
    member = ProjectMember(
        project_id=project.id,
        user_id=test_user.id,
        role=ProjectRole.OWNER.value,
    )
    db_session.add(member)
    db_session.commit()

    return project


@pytest.fixture
def test_issue(db_session, test_project, test_user):
    """Create a test issue"""
    issue = Issue(
        title="Test Issue",
        description="A test issue description",
        status=IssueStatus.OPEN.value,
        type=IssueType.BUG.value,
        priority=IssuePriority.HIGH.value,
        project_id=test_project.id,
        creator_id=test_user.id,
        assignee_id=test_user.id,
    )
    db_session.add(issue)
    db_session.commit()
    db_session.refresh(issue)
    return issue


@pytest.fixture
def test_tag(db_session):
    """Create a test tag"""
    tag = Tag(name="test-tag", color="#FF0000")
    db_session.add(tag)
    db_session.commit()
    db_session.refresh(tag)
    return tag


@pytest.fixture
def auth_headers(client, test_user):
    """Get authentication headers for test user"""
    response = client.post(
        "/api/auth/login",
        json={"username": test_user.username, "password": "password123"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_auth_headers(client, test_admin):
    """Get authentication headers for admin user"""
    response = client.post(
        "/api/auth/login",
        json={"username": test_admin.username, "password": "admin123"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
