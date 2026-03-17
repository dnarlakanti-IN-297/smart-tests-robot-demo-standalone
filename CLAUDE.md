# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Python issue-tracker application built with FastAPI, SQLAlchemy, and pytest. Manages issues, projects, users, and comments with JWT authentication and role-based access control.

**Tech Stack:**
- Python 3.11+
- FastAPI 0.109.0 (web framework)
- SQLAlchemy 2.0 (ORM)
- SQLite (database, easily swappable to PostgreSQL)
- Alembic (database migrations)
- Jinja2 (HTML templates)
- JWT with python-jose (authentication)
- pytest with httpx (testing)

## Build and Development Commands

**Note:** This project includes a comprehensive Makefile for easy development. Run `make help` to see all available commands.

### Environment Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

### Running the application
```bash
# Quick start with Makefile (recommended)
make run

# Or run directly
python run.py

# Or with uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Application starts on:
- Web Interface: http://localhost:8000
- API Documentation: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

### Testing
```bash
# Using Makefile (recommended)
make test                # Run all tests
make test-unit          # Run unit tests only
make test-integration   # Run integration tests only
make test-cov           # Run with coverage report

# Using pytest directly
pytest                   # Run all tests
pytest -v               # Run with verbose output
pytest --cov=app --cov-report=html --cov-report=term  # With coverage

# Run specific test file
pytest tests/unit/test_user_service.py

# Run specific test class
pytest tests/unit/test_user_service.py::TestUserService

# Run specific test method
pytest tests/unit/test_user_service.py::TestUserService::test_create_user

# Run tests matching pattern
pytest -k "user"

# Run tests with markers
pytest -m unit          # Run unit tests only
pytest -m integration   # Run integration tests only

# Show print statements
pytest -s

# Stop on first failure
pytest -x

# Run last failed tests
pytest --lf

# Show test durations
pytest --durations=10
```

### Code Quality
```bash
# Format code with black
black .

# Sort imports with isort
isort .

# Lint with flake8
flake8 app/ tests/

# Type checking with mypy
mypy app/

# Run all quality checks
black . && isort . && flake8 app/ tests/ && mypy app/
```

### Database Management
```bash
# Using Makefile (recommended)
make db-init            # Initialize database tables
make migrate            # Run Alembic migrations
make seed               # Seed database with sample data

# Using commands directly
python -m app.db.init_db                                    # Initialize database
alembic upgrade head                                         # Run migrations
alembic revision --autogenerate -m "description of changes" # Create new migration
python -m app.db.seed_data                                   # Seed sample data
```

## Architecture

### Layered Architecture
Standard Python web application with clear separation of concerns:

1. **Routes/Controllers** (`routes/` or `api/`) - Handle HTTP requests, input validation, response formatting
2. **Services** (`services/`) - Business logic layer, orchestrates operations
3. **Models** (`models/`) - Database models/entities (Issue, User, Project, Comment, etc.)
4. **Repositories/DAOs** (`repositories/` or `db/`) - Database access layer, query logic
5. **Schemas** (`schemas/`) - Pydantic/Marshmallow schemas for serialization and validation
6. **Auth** (`auth/`) - Authentication and authorization logic
7. **Middleware** (`middleware/`) - Request/response processing
8. **Utils** (`utils/`) - Helper functions and utilities
9. **Config** (`config.py`) - Application configuration

### Domain Model Relationships
- **User** (1) → (Many) **Issue** (as creator)
- **User** (1) → (Many) **Comment**
- **Project** (1) → (Many) **Issue**
- **Issue** (1) → (Many) **Comment**
- **User** (Many) ↔ (Many) **Project** (project members)
- **Issue** (Many) ↔ (1) **User** (assigned user, optional)

### Security Configuration
- **Public access**: `/health`, `/docs` (API docs)
- **Authenticated**: `/api/issues/**`, `/api/projects/**`, `/api/comments/**`
- **Admin only**: `/api/admin/**`, `/api/users/**`
- Authentication via JWT tokens or session-based
- Role-based access control (RBAC): USER, PROJECT_OWNER, ADMIN
- CSRF protection for form-based applications

### Test users
Seed data includes:
- Admin: `admin` / `admin123` (role: ADMIN, email: admin@example.com)
- User 1: `john` / `password123` (role: USER, email: john@example.com)
- User 2: `jane` / `password123` (role: USER, email: jane@example.com)

## Key Implementation Patterns

### Service Layer
Services contain business logic and coordinate between routes and repositories. Services should:
- Validate business rules
- Handle transactions
- Raise domain-specific exceptions
- Return domain objects or DTOs

### Repository Layer
Repositories abstract database access. Use SQLAlchemy or Django ORM for database operations.
- Keep queries in repositories, not in services
- Use eager loading to avoid N+1 queries
- Return model instances or None

### Schema/Serialization Layer
Use Pydantic (FastAPI) or Marshmallow (Flask) for data validation and serialization:
- Request schemas for input validation
- Response schemas for output serialization
- Separate create/update schemas when fields differ

### Issue Management
1. User creates issue with title, description, project
2. Issue assigned status (OPEN, IN_PROGRESS, RESOLVED, CLOSED)
3. Issue can be assigned to user
4. Users can comment on issues
5. Project owners and admins can delete issues
6. Issue creator can edit their own issues

### Authentication Flow
1. User registers with email/password
2. Password hashed with bcrypt/argon2
3. Login returns JWT token or creates session
4. Protected routes validate token/session
5. User permissions checked for operations

### Entity Best Practices
- Use type hints for all function parameters and returns
- Use dataclasses or Pydantic models for data structures
- Database models use SQLAlchemy declarative base or Django ORM
- Include `created_at` and `updated_at` timestamps
- Use UUIDs for primary keys (optional but recommended)
- Implement `__repr__` for debugging

## Testing Strategy

Tests organized using pytest:
- **Unit tests**: Service layer (mocked repositories), utility functions
- **Integration tests**: API endpoints with test database
- **Repository tests**: Database operations with test database
- **Fixture-based**: Use pytest fixtures for common setup

### Test Organization
```
tests/
├── conftest.py              # Shared fixtures
├── unit/
│   ├── test_issue_service.py
│   ├── test_user_service.py
│   └── test_validators.py
├── integration/
│   ├── test_issue_api.py
│   ├── test_auth_api.py
│   └── test_project_api.py
└── fixtures/
    └── sample_data.py       # Test data fixtures
```

### Common pytest Fixtures
```python
@pytest.fixture
def client():
    """Test client for making requests"""

@pytest.fixture
def db_session():
    """Database session for tests"""

@pytest.fixture
def test_user():
    """Create test user"""

@pytest.fixture
def test_issue():
    """Create test issue"""

@pytest.fixture
def authenticated_client(client, test_user):
    """Client with authentication"""
```

### pytest Markers
Mark tests for selective execution:
```python
@pytest.mark.unit          # Unit tests
@pytest.mark.integration   # Integration tests
@pytest.mark.slow          # Slow-running tests
@pytest.mark.smoke         # Smoke tests
@pytest.mark.parametrize   # Parameterized tests
```

### Mocking
Use `unittest.mock` or `pytest-mock` for mocking:
```python
from unittest.mock import Mock, patch

def test_service_with_mock(mocker):
    mock_repo = mocker.patch('app.services.issue_service.IssueRepository')
    # Test with mocked dependency
```

### Test Database
- Use separate test database configuration
- Reset database between tests using fixtures
- Use transactions that rollback after each test
- Consider using pytest-postgresql or similar for isolated test databases

## Common Development Scenarios

### Adding a new feature
1. Create database model in `models/` (with SQLAlchemy/Django ORM)
2. Create migration if using Alembic/Django migrations
3. Create repository/DAO for database operations
4. Create service with business logic
5. Create request/response schemas
6. Create route/controller with endpoints
7. Write tests at each layer (unit → integration)
8. Update seed data if needed

### Adding a new API endpoint
1. Define request/response schemas
2. Implement service method if new logic needed
3. Add route handler in appropriate routes file
4. Add authentication/authorization checks
5. Write integration test for endpoint
6. Update API documentation

### Modifying permissions
Edit authentication middleware or decorators. Common patterns:
- `@require_auth` - Requires valid authentication
- `@require_role(Role.ADMIN)` - Requires specific role
- `@require_permission('issue:delete')` - Requires permission
- Check resource ownership in service layer

### Debugging
```bash
# Run with debugger
pytest --pdb  # Drop into debugger on failure

# Use breakpoint()
# Add breakpoint() in code and run pytest -s

# Verbose logging
pytest -v -s --log-cli-level=DEBUG

# Print SQL queries (SQLAlchemy)
# Set echo=True in engine creation or use logging configuration
```

### Running specific test suites
```bash
# All unit tests
pytest tests/unit/

# All integration tests
pytest tests/integration/

# Tests for specific feature
pytest tests/ -k "issue"

# Tests with specific marker
pytest -m integration

# Exclude slow tests
pytest -m "not slow"

# Run with coverage for specific module
pytest --cov=app.services.issue_service tests/unit/test_issue_service.py
```

## Configuration Management

### Environment Variables
```bash
# .env file (not committed to git)
DATABASE_URL=postgresql://user:pass@localhost/issuetracker
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Load with python-dotenv
from dotenv import load_dotenv
load_dotenv()
```

### Configuration Classes
```python
# config.py
class Config:
    DEBUG = False
    TESTING = False
    DATABASE_URL = os.getenv('DATABASE_URL')

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    DATABASE_URL = 'sqlite:///:memory:'

class ProductionConfig(Config):
    # Production settings
    pass
```

## Dependencies

### Core Dependencies
- Web framework: Flask/FastAPI/Django
- ORM: SQLAlchemy or Django ORM
- Database driver: psycopg2/asyncpg (PostgreSQL) or sqlite3
- Authentication: PyJWT, passlib, bcrypt
- Validation: Pydantic or Marshmallow

### Development Dependencies
- pytest: Testing framework
- pytest-cov: Coverage reporting
- pytest-mock: Mocking support
- black: Code formatting
- isort: Import sorting
- flake8: Linting
- mypy: Type checking
- faker: Generate test data
- factory-boy: Test fixtures

## CI/CD Integration

### GitHub Actions Example
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      - name: Run tests
        run: pytest --cov=app --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

### Pre-commit Hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
```

## Best Practices

### Code Style
- Follow PEP 8 style guide
- Use type hints for function signatures
- Maximum line length: 88 characters (Black default)
- Use descriptive variable names
- Write docstrings for public functions and classes

### Error Handling
```python
# Define custom exceptions
class IssueTrackerException(Exception):
    pass

class IssueNotFoundException(IssueTrackerException):
    pass

class UnauthorizedException(IssueTrackerException):
    pass

# Handle in routes
try:
    issue = issue_service.get_issue(issue_id)
except IssueNotFoundException:
    return {"error": "Issue not found"}, 404
```

### Async Support (if using FastAPI)
```python
# Use async/await for I/O operations
async def get_issue(issue_id: int) -> Issue:
    return await issue_repository.find_by_id(issue_id)
```

### Logging
```python
import logging

logger = logging.getLogger(__name__)

logger.info("Creating new issue")
logger.error("Failed to create issue", exc_info=True)
```

---

# Adoption Journey Implementation Guide Standards

This repo also contains an adoption journey implementation guide (`ISP_SMART_TESTS_DEMO.adoc`). The standards below apply when producing or revising the implementation guide.

## Guide Format

- **AsciiDoc only.** All implementation guides must be `.adoc` files. The PS docsite (Antora) requires AsciiDoc.
- **Standard header metadata.** Every guide starts with AsciiDoc attributes for journey metadata, followed by the PS docsite attribution block:

```asciidoc
= [Guide Title]
:product-area: [FM / Smart Tests / SDLC Metrics / CI Insights / Release Orchestration / Onboarding]
:edition-required: [Edition 1 / Edition 2 / Edition 3 / standalone FM / TBD]
:journey-slug: [kebab-case slug, e.g., fm/ui-path or smart-tests/python-pytest]
:toc: left
:toclevels: 3

[cols="1,2"]
|===
|**Author(s)**
|**Details**

|[Your Name] ([username])
|Team: PS

Date: [YYYY-MM-DD]

|**Required Check(s)**
|**Status**

|PS Official
|Pending

|ENG Approval
|Pending

|===
```

The "Success Point(s)" row is omitted for implementation guides; it only applies to ISP delivery scripts.

## Required Sections (in order)

1. **Overview**: What the customer achieves, what they have when done, who the guide is for.
2. **Prerequisites**: Concrete, verifiable checklist. Categories: product, technical, access, parameterized values table.
3. **Step-by-Step Implementation**: Numbered steps, one action per step, copy-pasteable code blocks, expected output after key steps.
4. **Verification**: At least one verification step per major capability with expected results.
5. **Troubleshooting**: Known issues and resolutions. If none yet, include the section with a placeholder note.

## Style Rules (Non-Negotiable)

1. **No emojis in prose.** Not in headings, checkpoints, knowledge check markers, or document formatting. Use text labels instead (e.g., "Success:" not "checkmark emoji"). Emojis inside code blocks or expected tool/application output are acceptable (they are part of the application, not the document).
2. **No em dashes.** Use commas, semicolons, colons, periods, or parentheses.
3. **Active voice, second person, present tense.** "Run the following command" not "The following command should be run."
4. **Code blocks specify language.** Always use `[source,bash]`, `[source,go]`, `[source,python]`, `[source,yaml]`, etc.
5. **No internal references.** No Slack channels, no internal-only URLs. Guides are customer-facing.
6. **No unverified licensing or pricing claims.** If edition requirement is uncertain, use `:edition-required: TBD` and flag it.

## Code Quality Rules

- **Every command and code snippet must be tested** against this repo's demo application and confirmed working.
- **Expected output must match actual output.** Do not show output from a different branch or version than the one the reader is following.
- **No placeholder content.** No `TODO`, `TBD`, `[screenshot here]`, `https://your-instance.example.com`, or similar. Every value must be real or a documented parameterized placeholder using the format `<YOUR_VALUE>`.
- **All referenced files must exist** in this repository. Do not reference files that haven't been created.
- **Parameterized values** (values that vary per customer) use a consistent `<YOUR_VALUE>` format and are documented in the Prerequisites section.

## Implementation Guide Definition of Done

Before declaring the guide ready for review, every item must be true:

### Format and Metadata
- [ ] Written in AsciiDoc (`.adoc`)
- [ ] All header metadata attributes present and filled in
- [ ] Edition/licensing confirmed (not assumed or copied from another guide)

### Content Completeness
- [ ] Overview explains what the customer achieves
- [ ] All prerequisites listed, concrete, and verifiable
- [ ] Every step numbered, one action per step
- [ ] Verification section with expected results
- [ ] Troubleshooting section exists

### Code Quality
- [ ] Every command executed against this repo's demo application
- [ ] Every command produces the documented result
- [ ] All referenced files exist in this repository
- [ ] No placeholder content (TODO, TBD, screenshot placeholders, example.com URLs)
- [ ] Expected output matches actual output from the branch the reader follows
- [ ] Parameterized values use consistent format and documented in Prerequisites

### Style Compliance
- [ ] No emojis in prose (emojis in code blocks and tool output are acceptable)
- [ ] No em dashes
- [ ] Active voice, second person, present tense
- [ ] Code blocks specify language
- [ ] No Slack channels or internal-only references
- [ ] No unverified licensing or pricing claims

### Integration
- [ ] Demo application builds and runs successfully
- [ ] Guide can be followed start-to-finish on a clean setup
- [ ] Author has followed the guide end-to-end at least once

## ISP Downstream Use

This guide's content may be used to create an ISP (Integrated Success Plan) delivery script for instructor-led customer sessions. Well-structured guides with clear steps, knowledge checks, and verification points translate directly into delivery scripts. Keep this in mind when organizing content into logical modules.

## Review Process

When the guide is ready, notify Rene Cabral with the file path. Rene reviews against these standards and updates the journey spec and dashboard status in the adoption-journeys repo.
