# Technical Reference Documentation

**Issue Tracker Application**
Version: 1.0.0
Last Updated: 2025-01-XX
Python: 3.11+
Framework: FastAPI

---

## Table of Contents

1. [Application Specifications](#1-application-specifications)
2. [Database Schema and Models](#2-database-schema-and-models)
3. [API Endpoints](#3-api-endpoints)
4. [Testing Architecture](#4-testing-architecture)
5. [GitHub Actions and CI/CD](#5-github-actions-and-cicd)
6. [Smart Tests Integration](#6-smart-tests-integration)
7. [Local Development Setup](#7-local-development-setup)
8. [Docker Deployment](#8-docker-deployment)
9. [Code Quality and Standards](#9-code-quality-and-standards)
10. [Project Structure](#10-project-structure)

---

## 1. Application Specifications

### 1.1 Technology Stack

#### Core Framework
- **FastAPI**: `>=0.115.0` - Modern, high-performance web framework
- **Uvicorn**: `>=0.30.0` - ASGI server with standard features
- **Python**: `>=3.11` - Required minimum version

#### Database Layer
- **SQLAlchemy**: `>=2.0.36` - ORM with 2.0 architecture
- **Alembic**: `>=1.14.0` - Database migration tool
- **Database**: SQLite (default), PostgreSQL-ready

#### Authentication & Security
- **python-jose[cryptography]**: `>=3.3.0` - JWT token handling
- **bcrypt**: `>=5.0.0` - Password hashing
- **python-dotenv**: `>=1.0.1` - Environment variable management

#### Validation & Serialization
- **Pydantic**: `>=2.10.0` - Data validation using Python type hints
- **pydantic-settings**: `>=2.7.0` - Settings management
- **email-validator**: `>=2.2.0` - Email validation

#### Template Engine
- **Jinja2**: `>=3.1.4` - HTML templating for web interface

#### Additional Libraries
- **python-multipart**: `>=0.0.17` - File upload handling
- **python-dateutil**: `>=2.9.0` - Date manipulation utilities

### 1.2 Development Dependencies

#### Testing Framework
- **pytest**: `>=8.3.0` - Testing framework
- **pytest-asyncio**: `>=0.24.0` - Async test support
- **pytest-cov**: `>=6.0.0` - Coverage reporting
- **pytest-mock**: `>=3.14.0` - Mocking utilities
- **httpx**: `>=0.28.0` - HTTP client for testing APIs

#### End-to-End Testing
- **playwright**: `>=1.40.0` - Browser automation
- **pytest-playwright**: `>=0.4.0` - Playwright pytest integration

#### Code Quality Tools
- **black**: `>=24.10.0` - Code formatting (line length: 88)
- **isort**: `>=5.13.2` - Import sorting
- **flake8**: `>=7.1.0` - Linting and style checking
- **mypy**: `>=1.13.0` - Static type checking

#### Test Data
- **faker**: `>=33.0.0` - Fake data generation

### 1.3 Application Configuration

Configuration is managed through Pydantic Settings (`app/config.py`):

```python
class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Issue Tracker"
    DEBUG: bool = True
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ALLOWED_HOSTS: str = "localhost,127.0.0.1"

    # Database
    DATABASE_URL: str = "sqlite:///./issue_tracker.db"

    # JWT
    JWT_SECRET_KEY: str = "dev-jwt-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
```

**Configuration Loading:**
- Environment variables from `.env` file
- Case-sensitive variable names
- Type validation via Pydantic

### 1.4 Application Entry Points

#### Main Application (`app/main.py`)
```python
app = FastAPI(
    title=settings.APP_NAME,
    description="Issue Tracker API",
    version="1.0.0",
    docs_url="/api/docs",           # OpenAPI Swagger UI
    redoc_url="/api/redoc",          # ReDoc documentation
    openapi_url="/api/openapi.json", # OpenAPI JSON schema
)
```

#### Run Script (`run.py`)
```python
uvicorn.run(
    "app.main:app",
    host=settings.HOST,      # Default: 0.0.0.0
    port=settings.PORT,      # Default: 8000
    reload=settings.DEBUG,   # Auto-reload on code changes
)
```

**Public Endpoints:**
- `/health` - Health check endpoint
- `/api/docs` - Interactive API documentation (Swagger UI)
- `/api/redoc` - Alternative API documentation (ReDoc)

### 1.5 Static Files

- **Directory**: `app/static/`
- **Mount Path**: `/static`
- **Contents**: CSS, JavaScript, images for web interface

---

## 2. Database Schema and Models

### 2.1 Database Configuration

**Engine Setup** (`app/database.py`):
```python
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
    echo=settings.DEBUG,  # Log SQL queries in debug mode
)
```

**Session Management:**
- `SessionLocal` - Session factory
- `Base` - Declarative base for all models
- `get_db()` - Dependency injection for database sessions

### 2.2 Data Models

#### User Model (`app/models/user.py`)

**Table**: `users`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | Integer | Primary Key, Index | Unique identifier |
| `email` | String | Unique, Index, Not Null | User email address |
| `username` | String | Unique, Index, Not Null | Login username |
| `full_name` | String | Not Null | Display name |
| `hashed_password` | String | Not Null | bcrypt hashed password |
| `role` | String | Not Null, Default: "user" | User role (admin/user) |
| `is_active` | Boolean | Not Null, Default: True | Account status |
| `created_at` | DateTime | Not Null | Creation timestamp |
| `updated_at` | DateTime | Not Null | Last update timestamp |

**Relationships:**
- `created_issues` → Issues created by user
- `assigned_issues` → Issues assigned to user
- `comments` → User's comments (cascade delete)
- `project_memberships` → Project memberships (cascade delete)

**Enum: UserRole**
- `ADMIN` = "admin"
- `USER` = "user"

#### Project Model (`app/models/project.py`)

**Table**: `projects`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | Integer | Primary Key, Index | Unique identifier |
| `name` | String | Not Null, Index | Project name |
| `key` | String | Unique, Not Null, Index | Short project key (e.g., "PROJ") |
| `description` | Text | Nullable | Project description |
| `created_at` | DateTime | Not Null | Creation timestamp |
| `updated_at` | DateTime | Not Null | Last update timestamp |

**Relationships:**
- `issues` → Issues in project (cascade delete)
- `members` → Project members (cascade delete)

**Enum: ProjectRole**
- `OWNER` = "owner"
- `MEMBER` = "member"

#### ProjectMember Association Model

**Table**: `project_members`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | Integer | Primary Key, Index | Unique identifier |
| `project_id` | Integer | Foreign Key, Not Null | References projects.id (cascade delete) |
| `user_id` | Integer | Foreign Key, Not Null | References users.id (cascade delete) |
| `role` | String | Not Null, Default: "member" | Member role in project |
| `joined_at` | DateTime | Not Null | Membership start timestamp |

**Relationships:**
- `project` → Associated project
- `user` → Associated user

#### Issue Model (`app/models/issue.py`)

**Table**: `issues`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | Integer | Primary Key, Index | Unique identifier |
| `title` | String | Not Null, Index | Issue title |
| `description` | Text | Nullable | Detailed description |
| `status` | String | Not Null, Index, Default: "open" | Current status |
| `type` | String | Not Null, Index, Default: "task" | Issue type |
| `priority` | String | Not Null, Index, Default: "medium" | Priority level |
| `project_id` | Integer | Foreign Key, Not Null, Index | References projects.id (cascade delete) |
| `creator_id` | Integer | Foreign Key, Not Null, Index | References users.id (cascade delete) |
| `assignee_id` | Integer | Foreign Key, Nullable, Index | References users.id (set null) |
| `created_at` | DateTime | Not Null | Creation timestamp |
| `updated_at` | DateTime | Not Null | Last update timestamp |

**Relationships:**
- `project` → Parent project
- `creator` → User who created issue
- `assignee` → Assigned user (optional)
- `comments` → Issue comments (cascade delete)
- `tags` → Associated tags (many-to-many via `issue_tags`)

**Enums:**

**IssueStatus:**
- `OPEN` = "open"
- `IN_PROGRESS` = "in_progress"
- `RESOLVED` = "resolved"
- `CLOSED` = "closed"

**IssueType:**
- `BUG` = "bug"
- `FEATURE` = "feature"
- `TASK` = "task"
- `ENHANCEMENT` = "enhancement"

**IssuePriority:**
- `LOW` = "low"
- `MEDIUM` = "medium"
- `HIGH` = "high"
- `CRITICAL` = "critical"

#### Comment Model (`app/models/comment.py`)

**Table**: `comments`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | Integer | Primary Key, Index | Unique identifier |
| `content` | Text | Not Null | Comment text |
| `issue_id` | Integer | Foreign Key, Not Null, Index | References issues.id (cascade delete) |
| `author_id` | Integer | Foreign Key, Not Null, Index | References users.id (cascade delete) |
| `created_at` | DateTime | Not Null | Creation timestamp |
| `updated_at` | DateTime | Not Null | Last update timestamp |

**Relationships:**
- `issue` → Parent issue
- `author` → Comment author

#### Tag Model (`app/models/tag.py`)

**Table**: `tags`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | Integer | Primary Key, Index | Unique identifier |
| `name` | String | Unique, Not Null, Index | Tag name |
| `color` | String | Not Null, Default: "#6B7280" | Hex color code |
| `created_at` | DateTime | Not Null | Creation timestamp |

**Relationships:**
- `issues` → Associated issues (many-to-many via `issue_tags`)

#### IssueTag Association Table

**Table**: `issue_tags`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `issue_id` | Integer | Foreign Key, Primary Key | References issues.id (cascade delete) |
| `tag_id` | Integer | Foreign Key, Primary Key | References tags.id (cascade delete) |

### 2.3 Database Migrations

**Tool**: Alembic
**Configuration**: `alembic.ini`
**Migrations Directory**: `alembic/versions/`

**Commands:**
```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback last migration
alembic downgrade -1

# View migration history
alembic history
```

### 2.4 Database Initialization

**Init Database** (`app/db/init_db.py`):
- Creates all tables using `Base.metadata.create_all()`
- Run: `python -m app.db.init_db`

**Seed Data** (`app/db/seed_data.py`):
- Creates sample users (admin, john, jane)
- Creates sample projects, issues, comments, tags
- Run: `python -m app.db.seed_data`

**Test Accounts (after seeding):**
| Username | Password | Role | Email |
|----------|----------|------|-------|
| admin | admin123 | Admin | admin@example.com |
| john | password123 | User | john@example.com |
| jane | password123 | User | jane@example.com |

---

## 3. API Endpoints

### 3.1 API Router Structure

**Base Path**: `/api`

**Route Files** (`app/routes/`):
- `auth.py` - Authentication endpoints
- `users.py` - User management
- `projects.py` - Project operations
- `issues.py` - Issue tracking
- `comments.py` - Comments on issues
- `tags.py` - Tag management
- `web.py` - Web interface routes

### 3.2 Authentication Endpoints

**Base**: `/api/auth`

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/register` | Register new user | No |
| POST | `/login` | Login with username/password | No |
| POST | `/token` | OAuth2-compatible token endpoint | No |

**Request Example (Login):**
```json
{
  "username": "john",
  "password": "password123"
}
```

**Response Example:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3.3 User Endpoints

**Base**: `/api/users`

| Method | Endpoint | Description | Auth Required | Role |
|--------|----------|-------------|---------------|------|
| GET | `/me` | Get current user profile | Yes | Any |
| GET | `/` | List all users | Yes | Admin |
| GET | `/{id}` | Get user by ID | Yes | Admin |
| PUT | `/{id}` | Update user | Yes | Admin |
| DELETE | `/{id}` | Delete user | Yes | Admin |

### 3.4 Project Endpoints

**Base**: `/api/projects`

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/` | List user's projects | Yes |
| POST | `/` | Create new project | Yes |
| GET | `/{id}` | Get project details | Yes |
| PUT | `/{id}` | Update project | Yes (Owner) |
| DELETE | `/{id}` | Delete project | Yes (Owner) |
| POST | `/{id}/members` | Add member to project | Yes (Owner) |
| DELETE | `/{id}/members/{user_id}` | Remove member | Yes (Owner) |

**Request Example (Create Project):**
```json
{
  "name": "My Project",
  "key": "MYPROJ",
  "description": "Project description"
}
```

### 3.5 Issue Endpoints

**Base**: `/api/issues`

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/` | List issues (with filters) | Yes |
| POST | `/` | Create new issue | Yes |
| GET | `/me` | Get issues assigned to me | Yes |
| GET | `/{id}` | Get issue details | Yes |
| PUT | `/{id}` | Update issue | Yes |
| DELETE | `/{id}` | Delete issue | Yes (Creator/Owner/Admin) |

**Query Parameters (List Issues):**
- `project_id` - Filter by project
- `status` - Filter by status
- `assignee_id` - Filter by assignee
- `type` - Filter by type
- `priority` - Filter by priority

**Request Example (Create Issue):**
```json
{
  "title": "Fix login bug",
  "description": "Users cannot login with special characters",
  "project_id": 1,
  "type": "bug",
  "priority": "high",
  "status": "open",
  "assignee_id": 2
}
```

### 3.6 Comment Endpoints

**Base**: `/api/comments`

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/` | Get comments (requires `issue_id` param) | Yes |
| POST | `/` | Create comment | Yes |
| PUT | `/{id}` | Update comment | Yes (Author) |
| DELETE | `/{id}` | Delete comment | Yes (Author/Admin) |

**Request Example (Create Comment):**
```json
{
  "content": "I'm working on this issue now",
  "issue_id": 5
}
```

### 3.7 Tag Endpoints

**Base**: `/api/tags`

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/` | List all tags | Yes |
| POST | `/` | Create new tag | Yes |
| DELETE | `/{id}` | Delete tag | Yes (Admin) |

**Request Example (Create Tag):**
```json
{
  "name": "backend",
  "color": "#3498db"
}
```

### 3.8 Web Interface Endpoints

**Base**: `/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Home page / Dashboard |
| GET | `/login` | Login page |
| GET | `/register` | Registration page |
| GET | `/projects` | Projects list page |
| GET | `/projects/{id}` | Project detail page |
| GET | `/issues/{id}` | Issue detail page |

---

## 4. Testing Architecture

### 4.1 Test Organization

**Total Test Files**: 14
**Total Application Files**: 45

**Test Directory Structure:**
```
tests/
├── conftest.py              # Shared fixtures
├── unit/                    # Unit tests (6 files)
│   ├── test_user_service.py
│   ├── test_project_service.py
│   ├── test_issue_service.py
│   ├── test_auth_service.py
│   ├── test_comment_service.py
│   └── test_tag_service.py
├── integration/             # Integration tests (5 files)
│   ├── test_auth_api.py
│   ├── test_projects_api.py
│   ├── test_issues_api.py
│   ├── test_comments_api.py
│   └── test_tags_api.py
└── e2e/                     # End-to-end tests (3 files)
    ├── conftest.py          # E2E-specific fixtures
    ├── test_auth_e2e.py
    ├── test_projects_e2e.py
    └── test_issues_e2e.py
```

### 4.2 Pytest Configuration

**File**: `pyproject.toml`

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --strict-markers"
markers = [
    "unit: Unit tests",
    "integration: Integration tests",
    "e2e: End-to-end tests with Playwright",
    "slow: Slow running tests",
]
asyncio_mode = "auto"
```

**Test Markers:**
- `@pytest.mark.unit` - Marks unit tests
- `@pytest.mark.integration` - Marks integration tests
- `@pytest.mark.e2e` - Marks E2E tests
- `@pytest.mark.slow` - Marks slow-running tests

### 4.3 Shared Fixtures (`tests/conftest.py`)

#### Database Fixtures

**`db_session`** (function scope):
- Creates fresh test database for each test
- Uses SQLite in-memory database
- Automatically cleans up after test

**`client`** (function scope):
- FastAPI TestClient with test database
- Dependency injection override
- Automatic cleanup

#### User Fixtures

**`test_user`**:
- Email: test@example.com
- Username: testuser
- Password: password123
- Role: USER

**`test_admin`**:
- Email: admin@example.com
- Username: admin
- Password: admin123
- Role: ADMIN

**`test_user2`**:
- Secondary test user for multi-user scenarios

#### Domain Fixtures

**`test_project`**:
- Creates project with test_user as owner
- Name: "Test Project"
- Key: "TEST"

**`test_issue`**:
- Creates issue in test_project
- Creator and assignee: test_user
- Status: OPEN, Type: BUG, Priority: HIGH

**`test_tag`**:
- Creates tag for issue labeling
- Name: "test-tag", Color: "#FF0000"

#### Authentication Fixtures

**`auth_headers`**:
- JWT token for test_user
- Returns: `{"Authorization": "Bearer <token>"}`

**`admin_auth_headers`**:
- JWT token for test_admin
- Returns: `{"Authorization": "Bearer <token>"}`

#### CI Demo Fixture

**`ci_demo_delay`** (autouse):
- Adds 2-second delay per test in CI environment
- Only activates when `CI` or `GITHUB_ACTIONS` env var is set
- Purpose: Makes test execution visible in CI demo

### 4.4 E2E Test Configuration

**File**: `tests/e2e/conftest.py`

**Playwright Settings:**
- Browser: Chromium
- Base URL: http://localhost:8000
- Headless mode configurable
- Video recording: Retain on failure
- Screenshots: Only on failure

**CI Demo Delay:**
- 3-second delay per E2E test (longer than unit/integration)
- Purpose: E2E tests are more visually interesting in demos

### 4.5 Test Execution Commands

**Makefile Targets:**
```bash
make test                 # Run unit + integration tests
make test-unit           # Run only unit tests
make test-integration    # Run only integration tests
make test-e2e            # Run E2E tests (headed mode)
make test-e2e-headless   # Run E2E tests (headless)
make test-all            # Run all tests including E2E
make test-cov            # Run tests with coverage report
```

**Direct Pytest Commands:**
```bash
# Run all tests
pytest

# Run specific test suite
pytest tests/unit/
pytest tests/integration/
pytest tests/e2e/

# Run tests by marker
pytest -m unit
pytest -m integration
pytest -m e2e

# Run specific test file
pytest tests/unit/test_user_service.py

# Run specific test function
pytest tests/unit/test_user_service.py::TestUserService::test_create_user

# Run with coverage
pytest --cov=app --cov-report=html --cov-report=term

# Verbose output
pytest -v

# Show print statements
pytest -s

# Stop on first failure
pytest -x
```

### 4.6 Coverage Configuration

**File**: `pyproject.toml`

```toml
[tool.coverage.run]
source = ["app"]
omit = ["*/tests/*", "*/alembic/*"]

[tool.coverage.report]
precision = 2
show_missing = true
skip_covered = false
```

**Coverage Output:**
- HTML report: `htmlcov/index.html`
- Terminal report with missing lines
- XML report for Codecov integration

---

## 5. GitHub Actions and CI/CD

### 5.1 Workflows

**Location**: `.github/workflows/`

#### Workflow 1: Tests (`tests.yml`)

**Triggers:**
- Push to branches (when app/, tests/, requirements files change)
- Pull requests (same path filters)
- Manual trigger (workflow_dispatch)

**Jobs:**

**Job 1: Unit & Integration Tests**
- Runner: `ubuntu-latest`
- Python: `3.13`
- Java: `17` (for Smart Tests CLI)

**Steps:**
1. Checkout code (with full git history: `fetch-depth: 0`)
2. Set up Python 3.13 with pip cache
3. Set up Java 17 (Temurin distribution)
4. Install dependencies (requirements.txt, requirements-dev.txt, smart-tests-cli)
5. Verify Smart Tests connectivity
6. Record build with Smart Tests
7. Create test database
8. **Unit Tests:**
   - Record session for unit tests
   - Generate unit test list (`pytest --collect-only -qq`)
   - Create Smart Tests subset (target: 50%)
   - Run subset with pytest (`-o junit_family=legacy`)
   - Record results with Smart Tests
9. **Integration Tests:**
   - Record session for integration tests
   - Generate integration test list
   - Create Smart Tests subset (target: 50%)
   - Run subset with pytest
   - Record results with Smart Tests
10. Upload coverage to Codecov

**Features:**
- `continue-on-error: true` on unit tests (integration tests always run)
- `if: always()` on integration test steps
- JUnit XML output with legacy format
- Coverage with append mode for combined report

**Job 2: E2E Tests with Playwright**
- Runner: `ubuntu-latest`
- Python: `3.13`
- Java: `17`

**Steps:**
1. Checkout code
2. Set up Python and Java
3. Install dependencies + Playwright browsers (Chromium)
4. Verify Smart Tests connectivity
5. Record build with Smart Tests
6. Record session for E2E tests
7. Initialize database and seed data
8. Start application in background (wait for health check)
9. Generate E2E test list
10. Create Smart Tests subset (target: 50%)
11. Run E2E tests with video/screenshot capture
12. Record results with Smart Tests
13. Upload Playwright artifacts (videos, screenshots) on failure

#### Workflow 2: Apply Demo Patch (`apply-demo-patch.yml`)

**Trigger:** Manual only (workflow_dispatch)

**Inputs:**
- `action`: Choice (apply/revert)
- `patch_name`: Dropdown choice of 4 patches

**Branch Protection:**
- Only runs on branches starting with `patch-*`
- Prevents accidental changes to main branch

**Steps:**
1. Check branch name matches `patch-*` pattern
2. Checkout code
3. Configure Git (github-actions bot)
4. Verify patch file exists
5. Apply or revert patch
6. Commit changes with detailed message
7. Push to branch
8. Generate workflow summary

**Safety Features:**
- Branch name validation (must start with `patch-`)
- Commit co-authored by github-actions bot
- Detailed commit messages with workflow run URL
- Summary with expected CI behavior

### 5.2 Environment Variables

**Required Secret:**
- `PTSv2_TOKEN` - Token for PTSv2 (AI-based) engine
- `PTSv1_TOKEN` - Token for PTSv1 (ML-based) engine

**Automatic Variables:**
- `CI` - Set by GitHub Actions
- `GITHUB_ACTIONS` - Set by GitHub Actions
- `github.run_id` - Unique workflow run identifier
- `github.actor` - User who triggered workflow
- `github.ref_name` - Branch name

### 5.3 CI Test Execution Time

**Without delays**: ~35 seconds
**With CI demo delays**: 2-3 minutes

**Delay Implementation:**
- Unit/Integration tests: 2 seconds per test
- E2E tests: 3 seconds per test
- Only activates in CI (checks for `CI` or `GITHUB_ACTIONS` env vars)

---

## 6. Smart Tests Integration

### 6.1 Overview

**Tool**: CloudBees Smart Tests CLI 2.0
**Purpose**: AI-powered predictive test selection
**Mode**: Observation mode (runs all tests, predicts subset)

**⚠️ IMPORTANT PREREQUISITE:**

Your CloudBees organization or sub-organization **must have PTSv2 (Predictive Test Selection v2) enabled** for Smart Tests to perform predictive test selection. Without PTSv2 enabled, workflows will execute but Smart Tests will not generate test subset predictions.

**To verify or enable PTSv2:**
- Contact the CloudBees Smart Tests team via Slack: **#team-smart-tests-se**
- Provide your organization or sub-organization ID
- Request PTSv2 enablement if not already active

### 6.2 Installation

```bash
pip3 install --no-cache-dir smart-tests-cli~=2.0
```

### 6.3 Workflow Integration

#### Step 1: Record Build
```bash
smart-tests record build --build ${{ github.run_id }}
```
Creates a build record in Smart Tests platform.

#### Step 2: Record Session
```bash
smart-tests record session \
  --build ${{ github.run_id }} \
  --observation \
  --test-suite pytest-unit \
  > session-unit.txt
```
Creates a test session in observation mode.

**Test Suites:**
- `pytest-unit` - Unit tests
- `pytest-integration` - Integration tests
- `pytest-e2e` - End-to-end tests

#### Step 3: Generate Test List
```bash
pytest --collect-only -qq tests/unit/ > test_list_unit.txt
```
Collects all test node IDs (format: `file.py::TestClass::test_method`).

**Important:** Use `-qq` (double quiet) to get clean test IDs without extra output.

#### Step 4: Create Subset
```bash
cat test_list_unit.txt | \
  smart-tests subset pytest \
  --session @session-unit.txt \
  --target 50% \
  > smart-tests-subset-unit.txt
```
Smart Tests predicts which tests to run based on code changes.

**Target**: 50% of tests (adjustable)

#### Step 5: Run Tests
```bash
pytest -v \
  -o junit_family=legacy \
  --cov=app \
  --cov-report=xml \
  --junit-xml=test-results/unit.xml \
  @smart-tests-subset-unit.txt
```

**Important flags:**
- `-o junit_family=legacy` - Required for Smart Tests compatibility
- `@smart-tests-subset-unit.txt` - Read test paths from file

#### Step 6: Record Results
```bash
smart-tests record tests pytest \
  --session @session-unit.txt \
  "test-results/unit.xml"
```
Uploads test results to Smart Tests platform.

### 6.4 Smart Tests Features in This Project

**Test Coverage:**
- ✅ Unit tests (pytest-unit suite)
- ✅ Integration tests (pytest-integration suite)
- ✅ E2E tests (pytest-e2e suite)

**Integration Points:**
- All three test suites independently tracked
- Separate sessions for each suite
- Combined build record
- Coverage integration

**Observation Mode Benefits:**
- All tests run (no tests skipped)
- Predictions shown in UI for validation
- Accuracy metrics calculated
- Time savings estimated

**Configuration:**
- Target: 50% test subset
- JUnit format: Legacy
- Sessions recorded per test suite
- Build ID: GitHub run ID

### 6.5 Viewing Results

**CloudBees Platform:**
1. Navigate to Smart Tests → Predictive Test Selection
2. Go to Observation Mode
3. Find test session by GitHub run ID
4. View:
   - All tests that ran
   - Predicted subset
   - Accuracy metrics
   - Time savings
   - Failed vs passed tests

**Metrics to Analyze:**
- **Prediction Accuracy**: % of failures caught by predicted subset
- **Time Savings**: Difference between full run and predicted subset
- **Test Selection**: Which tests were predicted vs skipped

---

## 7. Local Development Setup

### 7.1 Prerequisites

- **Python**: 3.11 or higher
- **pip**: Python package manager
- **Git**: Version control
- **Virtual environment**: Recommended

### 7.2 Initial Setup

#### 1. Clone Repository
```bash
git clone <repository-url>
cd issue-tracker-app
```

#### 2. Create Virtual Environment
```bash
python -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

#### 3. Install Dependencies
```bash
# Production dependencies
pip install -r requirements.txt

# Development dependencies (includes testing, linting, etc.)
pip install -r requirements-dev.txt

# Or use Makefile
make install-dev
```

#### 4. Configure Environment
```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your settings (optional for local dev)
```

**Environment Variables:**
```env
APP_NAME="Issue Tracker"
DEBUG=True
SECRET_KEY=your-secret-key-change-this-in-production
DATABASE_URL=sqlite:///./issue_tracker.db
JWT_SECRET_KEY=your-jwt-secret-key-change-this
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
HOST=0.0.0.0
PORT=8000
```

#### 5. Initialize Database
```bash
# Create database tables
make db-init
# or
python -m app.db.init_db

# Run migrations
make migrate
# or
alembic upgrade head

# Seed with sample data
make seed
# or
python -m app.db.seed_data
```

#### 6. Run Application
```bash
# Using Makefile (recommended)
make run

# Or directly
python run.py

# Or with uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Application URLs:**
- Web Interface: http://localhost:8000
- API Documentation: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc
- Health Check: http://localhost:8000/health

### 7.3 Development Workflow

#### Running Tests
```bash
# All tests (unit + integration)
make test

# Specific test suites
make test-unit
make test-integration
make test-e2e           # With browser visible
make test-e2e-headless  # Headless mode

# With coverage
make test-cov
```

#### Code Quality
```bash
# Format code (black + isort)
make format

# Run linters
make lint

# Individual tools
black .
isort .
flake8 app/ tests/
mypy app/
```

#### Database Operations
```bash
# Create new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
make migrate

# Rollback migration
alembic downgrade -1

# View migration history
alembic history
```

#### Clean Up
```bash
make clean  # Remove cache files, coverage reports, etc.
```

### 7.4 Playwright Setup (for E2E tests)

```bash
# One-time browser installation
./venv/bin/playwright install chromium

# Or install all browsers
./venv/bin/playwright install
```

### 7.5 Project Files and Directories

**Configuration Files:**
- `.env` - Environment variables (not in git)
- `.env.example` - Template for environment variables
- `pyproject.toml` - Project configuration (pytest, black, isort, mypy)
- `alembic.ini` - Alembic migration configuration
- `Makefile` - Development commands
- `Dockerfile` - Docker image definition
- `docker-compose.yml` - Docker Compose services

**Main Directories:**
- `app/` - Application code (45 Python files)
- `tests/` - Test code (14 test files)
- `alembic/` - Database migrations
- `patches/` - Demo patches for CI
- `.github/workflows/` - CI/CD workflows

---

## 8. Docker Deployment

### 8.1 Docker Configuration

#### Dockerfile

**Base Image**: `python:3.11-slim`
**Working Directory**: `/app`

**Build Steps:**
1. Install system dependencies (gcc for compiling Python packages)
2. Copy and install Python requirements
3. Copy application code
4. Create directory for SQLite database
5. Expose port 8000

**Startup Command:**
```bash
alembic upgrade head && \
python -m app.db.seed_data && \
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 8.2 Docker Compose

**File**: `docker-compose.yml`
**Version**: 3.8

**Service: web**

**Configuration:**
- Build: Current directory (.)
- Ports: 8000:8000
- Volumes:
  - `./data:/app/data` - Persist database
  - `./app:/app/app` - Hot reload for development
- Environment:
  - DATABASE_URL: `sqlite:///./data/issue_tracker.db`
  - DEBUG: True
  - SECRET_KEY: dev-secret-key-change-in-production
  - JWT_SECRET_KEY: dev-jwt-secret-key-change-in-production

**Command:**
```bash
sh -c "alembic upgrade head &&
       python -m app.db.seed_data &&
       uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
```

### 8.3 Docker Commands

```bash
# Build image
make docker-build
# or
docker-compose build

# Start containers
make docker-up
# or
docker-compose up -d

# View logs
docker-compose logs -f

# Stop containers
make docker-down
# or
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

### 8.4 Production Considerations

**For production deployment:**

1. **Change secrets:**
   ```env
   SECRET_KEY=<generate-strong-secret>
   JWT_SECRET_KEY=<generate-strong-jwt-secret>
   DEBUG=False
   ```

2. **Use PostgreSQL:**
   ```env
   DATABASE_URL=postgresql://user:password@postgres:5432/issue_tracker
   ```

3. **Add PostgreSQL service to docker-compose.yml:**
   ```yaml
   services:
     postgres:
       image: postgres:15
       environment:
         POSTGRES_DB: issue_tracker
         POSTGRES_USER: user
         POSTGRES_PASSWORD: password
       volumes:
         - postgres_data:/var/lib/postgresql/data

   volumes:
     postgres_data:
   ```

4. **Use production ASGI server settings:**
   - Remove `--reload` flag
   - Add workers: `--workers 4`
   - Configure logging

5. **Add reverse proxy (nginx):**
   - SSL/TLS termination
   - Static file serving
   - Request rate limiting

---

## 9. Code Quality and Standards

### 9.1 Code Formatting

#### Black

**Configuration** (`pyproject.toml`):
```toml
[tool.black]
line-length = 88
target-version = ['py311']
include = '\.pyi?$'
exclude = '''
/(
    \.git
  | \.venv
  | venv
  | alembic
  | __pycache__
)/
'''
```

**Usage:**
```bash
black .              # Format all files
black app/           # Format app directory
black --check .      # Check without modifying
black --diff .       # Show diffs
```

#### isort

**Configuration** (`pyproject.toml`):
```toml
[tool.isort]
profile = "black"
line_length = 88
skip = [".venv", "venv", "alembic"]
```

**Usage:**
```bash
isort .              # Sort imports
isort --check-only . # Check without modifying
isort --diff .       # Show diffs
```

### 9.2 Linting

#### Flake8

**Usage:**
```bash
flake8 app/ tests/   # Lint application and tests
```

**Configuration:** Follows PEP 8 style guide

**Common Checks:**
- Line length (88 characters with Black)
- Unused imports
- Undefined names
- Indentation errors
- Trailing whitespace

#### Mypy

**Configuration** (`pyproject.toml`):
```toml
[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false
ignore_missing_imports = true
exclude = ["alembic", ".venv", "venv"]
```

**Usage:**
```bash
mypy app/            # Type check application
```

### 9.3 Development Standards

#### Code Style
- **PEP 8** compliance via Flake8
- **88 characters** line length (Black default)
- **Type hints** for function signatures
- **Docstrings** for public functions and classes

#### Import Organization
```python
# Standard library imports
import os
from datetime import datetime

# Third-party imports
from fastapi import FastAPI
from sqlalchemy import Column

# Local imports
from app.models import User
from app.services import UserService
```

#### Naming Conventions
- **Classes**: PascalCase (`UserService`, `ProjectModel`)
- **Functions/Methods**: snake_case (`get_user`, `create_project`)
- **Constants**: UPPER_SNAKE_CASE (`DATABASE_URL`, `JWT_ALGORITHM`)
- **Private**: Leading underscore (`_internal_method`)

#### Error Handling
```python
from fastapi import HTTPException, status

# Raise HTTP exceptions for API errors
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not found"
)
```

#### Dependency Injection
```python
from fastapi import Depends
from app.database import get_db

def get_user(
    user_id: int,
    db: Session = Depends(get_db)
) -> User:
    # Function implementation
    pass
```

### 9.4 Pre-commit Hooks (Optional)

**Install pre-commit:**
```bash
pip install pre-commit
```

**Create `.pre-commit-config.yaml`:**
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.10.0
    hooks:
      - id: black

  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 7.1.0
    hooks:
      - id: flake8
```

**Install hooks:**
```bash
pre-commit install
```

---

## 10. Project Structure

### 10.1 Directory Overview

```
issue-tracker-app/
├── .github/                    # GitHub Actions workflows
│   └── workflows/
│       ├── tests.yml          # CI testing workflow
│       └── apply-demo-patch.yml # Patch application workflow
│
├── alembic/                   # Database migrations
│   ├── versions/              # Migration files
│   ├── env.py                 # Alembic environment
│   └── script.py.mako         # Migration template
│
├── app/                       # Main application (45 files)
│   ├── __init__.py
│   ├── main.py               # FastAPI app entry point
│   ├── config.py             # Application settings
│   ├── database.py           # Database configuration
│   │
│   ├── auth/                 # Authentication
│   │   ├── password.py       # Password hashing
│   │   └── jwt.py            # JWT token handling
│   │
│   ├── db/                   # Database utilities
│   │   ├── init_db.py        # Database initialization
│   │   └── seed_data.py      # Sample data seeding
│   │
│   ├── models/               # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py           # User model
│   │   ├── project.py        # Project and ProjectMember
│   │   ├── issue.py          # Issue model with enums
│   │   ├── comment.py        # Comment model
│   │   └── tag.py            # Tag model
│   │
│   ├── repositories/         # Data access layer
│   │   ├── __init__.py
│   │   ├── user_repository.py
│   │   ├── project_repository.py
│   │   ├── issue_repository.py
│   │   ├── comment_repository.py
│   │   └── tag_repository.py
│   │
│   ├── routes/               # API endpoints
│   │   ├── __init__.py       # Router aggregation
│   │   ├── auth.py           # Authentication routes
│   │   ├── users.py          # User management
│   │   ├── projects.py       # Project operations
│   │   ├── issues.py         # Issue tracking
│   │   ├── comments.py       # Comment management
│   │   ├── tags.py           # Tag operations
│   │   └── web.py            # Web interface routes
│   │
│   ├── schemas/              # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py           # User validation schemas
│   │   ├── project.py        # Project schemas
│   │   ├── issue.py          # Issue schemas
│   │   ├── comment.py        # Comment schemas
│   │   └── tag.py            # Tag schemas
│   │
│   ├── services/             # Business logic
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   ├── project_service.py
│   │   ├── issue_service.py
│   │   ├── comment_service.py
│   │   ├── tag_service.py
│   │   └── auth_service.py
│   │
│   ├── static/               # Static files
│   │   ├── css/              # Stylesheets
│   │   └── js/               # JavaScript
│   │
│   └── templates/            # Jinja2 templates
│       ├── base.html         # Base template
│       ├── index.html        # Home page
│       ├── login.html        # Login page
│       └── ...               # Other pages
│
├── patches/                  # Demo patches for CI
│   ├── README.md             # Patch documentation
│   ├── CREATING_NEW_PATCHES.md # Patch creation guide
│   ├── AI_PATCH_GENERATION_PROMPT.txt # AI prompt template
│   ├── 01-require-project-description.patch
│   ├── 02-require-long-issue-titles.patch
│   ├── 03-require-long-comments.patch
│   └── 04-require-corporate-email.patch
│
├── tests/                    # Test suite (14 files)
│   ├── conftest.py           # Shared fixtures
│   │
│   ├── unit/                 # Unit tests
│   │   ├── test_user_service.py
│   │   ├── test_project_service.py
│   │   ├── test_issue_service.py
│   │   ├── test_auth_service.py
│   │   ├── test_comment_service.py
│   │   └── test_tag_service.py
│   │
│   ├── integration/          # Integration tests
│   │   ├── test_auth_api.py
│   │   ├── test_projects_api.py
│   │   ├── test_issues_api.py
│   │   ├── test_comments_api.py
│   │   └── test_tags_api.py
│   │
│   └── e2e/                  # End-to-end tests
│       ├── conftest.py       # Playwright fixtures
│       ├── test_auth_e2e.py
│       ├── test_projects_e2e.py
│       └── test_issues_e2e.py
│
├── .env.example              # Environment template
├── .gitignore                # Git ignore patterns
├── alembic.ini               # Alembic configuration
├── docker-compose.yml        # Docker Compose setup
├── Dockerfile                # Docker image definition
├── Makefile                  # Development commands
├── pyproject.toml            # Project configuration
├── README.md                 # Project overview
├── QUICKSTART.md             # Quick start guide
├── TECHNICAL_REFERENCE.md    # This file
├── requirements.txt          # Production dependencies
├── requirements-dev.txt      # Development dependencies
└── run.py                    # Application runner
```

### 10.2 Architecture Layers

**Layered Architecture (Clean Architecture):**

```
┌─────────────────────────────────────────┐
│  Routes (API Endpoints)                 │  ← HTTP request handling
│  - Input validation                     │
│  - Response formatting                  │
│  - Authentication checks                │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  Services (Business Logic)              │  ← Core application logic
│  - Business rules                       │
│  - Transaction management               │
│  - Domain operations                    │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  Repositories (Data Access)             │  ← Database operations
│  - Query logic                          │
│  - CRUD operations                      │
│  - Database abstraction                 │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  Models (Data Entities)                 │  ← SQLAlchemy ORM
│  - Database schema                      │
│  - Relationships                        │
│  - Data structure                       │
└─────────────────────────────────────────┘
```

**Cross-cutting Concerns:**
- **Schemas**: Data validation and serialization (Pydantic)
- **Auth**: Authentication and authorization
- **Config**: Application configuration
- **Database**: Session management

### 10.3 Key Files Explained

#### Configuration Files

**`pyproject.toml`**
- Project metadata
- Tool configurations (pytest, black, isort, mypy, coverage)
- Build system configuration

**`alembic.ini`**
- Alembic migration tool settings
- Database URL template
- Migration file locations

**`Makefile`**
- Development automation commands
- 20+ targets for common operations
- Environment setup, testing, Docker, etc.

**`.env.example`**
- Template for environment variables
- Documents all configuration options
- Safe to commit (no secrets)

#### Application Files

**`app/main.py`**
- FastAPI application instance
- Router inclusion
- Static files mounting
- OpenAPI configuration

**`app/config.py`**
- Centralized configuration
- Pydantic Settings for validation
- Environment variable loading

**`app/database.py`**
- SQLAlchemy engine setup
- Session factory
- Database dependency injection

**`run.py`**
- Application entry point
- Uvicorn server configuration
- Development mode settings

#### Test Files

**`tests/conftest.py`**
- Shared pytest fixtures
- Test database setup
- Authentication helpers
- Domain object factories

**`tests/e2e/conftest.py`**
- Playwright-specific fixtures
- Browser configuration
- E2E test setup

### 10.4 File Counts and Statistics

**Application Code:**
- Total Python files: 45
- Lines of code: ~5,000+ (estimated)

**Test Code:**
- Total test files: 14
- Unit tests: 6 files
- Integration tests: 5 files
- E2E tests: 3 files
- Test coverage: 140+ tests

**Configuration:**
- Workflows: 2
- Docker files: 2
- Config files: 5+

**Documentation:**
- README files: 6+
- Markdown docs: 8+

---

## Appendix A: Quick Reference

### A.1 Port Numbers

| Service | Port | URL |
|---------|------|-----|
| Application | 8000 | http://localhost:8000 |
| API Docs | 8000 | http://localhost:8000/api/docs |
| ReDoc | 8000 | http://localhost:8000/api/redoc |
| Health Check | 8000 | http://localhost:8000/health |

### A.2 Default Credentials

| User | Password | Role |
|------|----------|------|
| admin | admin123 | Admin |
| john | password123 | User |
| jane | password123 | User |

### A.3 Common Commands

```bash
# Setup
make install-dev
make db-init && make migrate && make seed

# Development
make run
make test
make format
make lint

# Docker
make docker-build
make docker-up
make docker-down

# Database
alembic upgrade head
alembic revision --autogenerate -m "Message"
python -m app.db.seed_data

# Testing
pytest
pytest -m unit
pytest -m integration
pytest -m e2e
pytest --cov=app
```

### A.4 Important URLs

- **Repository**: [GitHub Repository URL]
- **CI/CD**: GitHub Actions tab
- **Smart Tests**: https://cloudbees.io
- **Documentation**: http://localhost:8000/api/docs

### A.5 Folder Shortcuts

```bash
# Application
cd app/models      # Database models
cd app/routes      # API endpoints
cd app/services    # Business logic
cd app/schemas     # Validation schemas

# Tests
cd tests/unit          # Unit tests
cd tests/integration   # Integration tests
cd tests/e2e          # E2E tests

# CI/CD
cd .github/workflows   # GitHub Actions
cd patches            # Demo patches
```

---

## Appendix B: Troubleshooting

### B.1 Common Issues

**Issue: Database locked**
- **Cause**: Multiple processes accessing SQLite
- **Solution**: Use separate test database, restart application

**Issue: Port 8000 already in use**
- **Cause**: Another process using the port
- **Solution**: `lsof -i :8000` and kill process, or change PORT in .env

**Issue: ModuleNotFoundError**
- **Cause**: Missing dependencies
- **Solution**: `pip install -r requirements-dev.txt`

**Issue: Alembic migrations fail**
- **Cause**: Conflicting migration history
- **Solution**: `alembic downgrade base` then `alembic upgrade head`

**Issue: Tests fail with JWT errors**
- **Cause**: Wrong secret key
- **Solution**: Check JWT_SECRET_KEY in .env

**Issue: Playwright browser not found**
- **Cause**: Browsers not installed
- **Solution**: `playwright install chromium`

**Issue: Smart Tests not generating test subset predictions**
- **Cause**: PTSv2 (Predictive Test Selection v2) not enabled for your CloudBees organization
- **Solution**: Contact #team-smart-tests-se on Slack with your organization/sub-organization ID to request PTSv2 enablement
- **Note**: Workflows will run successfully but won't generate predictive subsets without PTSv2

**Issue: No test results visible in CloudBees Smart Tests dashboard**
- **Cause**: Multiple possible causes
  - PTSv2_TOKEN (or PTSv1_TOKEN) not configured correctly
  - PTSv2 not enabled
  - Network connectivity issues
  - Organization permissions
- **Solution**:
  - Verify `PTSv2_TOKEN` (or `PTSv1_TOKEN`) secret in GitHub repository settings
  - Check workflow logs for Smart Tests CLI errors
  - Verify PTSv2 is enabled for your organization
  - Contact #team-smart-tests-se for assistance

### B.2 Debug Commands

```bash
# Check Python version
python --version

# Verify virtual environment
which python

# List installed packages
pip list

# Test database connection
python -c "from app.database import engine; print(engine)"

# Check running processes
ps aux | grep uvicorn

# View application logs
# (if running with docker-compose)
docker-compose logs -f web
```

---

**End of Technical Reference Documentation**
