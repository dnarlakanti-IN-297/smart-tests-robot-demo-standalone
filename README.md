# Issue Tracker

![Tests](https://github.com/xgalanxhi/issues-tracker-app/actions/workflows/tests.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

A modern issue tracking application built with FastAPI, SQLAlchemy, and Python. Features project management, issue tracking with statuses and priorities, comments, tags, and JWT authentication.

## Features

- ✅ **User Authentication** - JWT token-based authentication
- ✅ **Project Management** - Create and manage projects with member roles
- ✅ **Issue Tracking** - Track issues with statuses, types, and priorities
- ✅ **Comments** - Add comments and discussions to issues
- ✅ **Tags/Labels** - Organize issues with tags
- ✅ **Assignments** - Assign issues to team members
- ✅ **RESTful API** - Comprehensive REST API with OpenAPI documentation
- ✅ **Web Interface** - HTML templates for browser-based access
- ✅ **Comprehensive Tests** - Unit and integration tests with pytest

## Tech Stack

- **Framework**: FastAPI 0.109.0
- **Database**: SQLite (easily swappable to PostgreSQL)
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic
- **Authentication**: JWT with python-jose
- **Testing**: pytest with httpx
- **Templates**: Jinja2
- **Code Quality**: black, isort, flake8, mypy

## Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

## Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
cd issue-tracker-app

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows

# Install dependencies
make install-dev
```

### 2. Initialize Database

```bash
# Create environment file
cp .env.example .env

# Initialize database and seed with sample data
make db-init
make migrate
make seed
```

### 3. Run the Application

```bash
# Start development server
make run
```

The application will be available at:
- Web Interface: http://localhost:8000
- API Documentation: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## Makefile Commands

The project includes a comprehensive Makefile for easy development:

### Setup & Installation
- `make install` - Install production dependencies
- `make install-dev` - Install development dependencies
- `make db-init` - Initialize database
- `make migrate` - Run database migrations
- `make seed` - Seed database with sample data

### Development
- `make run` - Run development server (auto-restarts on changes)
- `make format` - Format code with black and isort
- `make lint` - Run linting checks (flake8, mypy, black, isort)

### Testing
- `make test` - Run all tests
- `make test-unit` - Run unit tests only
- `make test-integration` - Run integration tests only
- `make test-cov` - Run tests with coverage report

### Docker
- `make docker-build` - Build Docker image
- `make docker-up` - Start Docker containers
- `make docker-down` - Stop Docker containers

### Cleanup
- `make clean` - Remove generated files and cache

## Project Structure

```
issue-tracker-app/
├── app/
│   ├── auth/              # Authentication utilities
│   ├── db/                # Database initialization and seeding
│   ├── models/            # SQLAlchemy models
│   ├── repositories/      # Data access layer
│   ├── routes/            # API endpoints
│   ├── schemas/           # Pydantic schemas
│   ├── services/          # Business logic
│   ├── static/            # CSS, JS files
│   ├── templates/         # Jinja2 HTML templates
│   ├── config.py          # Configuration
│   ├── database.py        # Database setup
│   └── main.py            # FastAPI application
├── tests/
│   ├── unit/              # Unit tests
│   ├── integration/       # Integration tests
│   └── conftest.py        # Pytest fixtures
├── alembic/               # Database migrations
├── Makefile               # Development commands
├── requirements.txt       # Production dependencies
├── requirements-dev.txt   # Development dependencies
├── pyproject.toml         # Project configuration
├── Dockerfile             # Docker configuration
└── docker-compose.yml     # Docker Compose setup
```

## Test Accounts

After seeding the database, you can use these test accounts:

| Username | Password    | Role  |
|----------|-------------|-------|
| admin    | admin123    | Admin |
| john     | password123 | User  |
| jane     | password123 | User  |

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and get JWT token
- `POST /api/auth/token` - OAuth2 compatible token endpoint

### Users
- `GET /api/users/me` - Get current user
- `GET /api/users` - List all users
- `GET /api/users/{id}` - Get user by ID
- `PUT /api/users/{id}` - Update user
- `DELETE /api/users/{id}` - Delete user

### Projects
- `GET /api/projects` - List user's projects
- `POST /api/projects` - Create a new project
- `GET /api/projects/{id}` - Get project details
- `PUT /api/projects/{id}` - Update project
- `DELETE /api/projects/{id}` - Delete project
- `POST /api/projects/{id}/members` - Add member to project
- `DELETE /api/projects/{id}/members/{user_id}` - Remove member

### Issues
- `GET /api/issues` - List issues (with optional project filter)
- `POST /api/issues` - Create a new issue
- `GET /api/issues/me` - Get issues assigned to current user
- `GET /api/issues/{id}` - Get issue details
- `PUT /api/issues/{id}` - Update issue
- `DELETE /api/issues/{id}` - Delete issue

### Comments
- `GET /api/comments?issue_id={id}` - Get comments for an issue
- `POST /api/comments` - Create a new comment
- `PUT /api/comments/{id}` - Update comment
- `DELETE /api/comments/{id}` - Delete comment

### Tags
- `GET /api/tags` - List all tags
- `POST /api/tags` - Create a new tag
- `DELETE /api/tags/{id}` - Delete tag

## Running Tests

```bash
# Run all tests (unit + integration, excludes E2E)
make test

# Run with coverage report
make test-cov

# Run only unit tests
make test-unit

# Run only integration tests
make test-integration

# Run E2E tests with Playwright (headless)
make test-e2e-headless

# Run E2E tests with Playwright (headed - see browser)
make test-e2e

# Run all tests including E2E
make test-all

# Run tests with verbose output
pytest -v

# Run specific test file
pytest tests/unit/test_user_service.py

# Run specific test
pytest tests/unit/test_user_service.py::TestUserService::test_create_user

# Run tests with markers
pytest -m unit          # Run only unit tests
pytest -m integration   # Run only integration tests
pytest -m e2e           # Run only E2E tests
```

### E2E Testing with Playwright

The project includes comprehensive end-to-end tests using Playwright that test the full application flow in a real browser:

**Setup (one-time):**
```bash
# Install Playwright browsers
./venv/bin/playwright install chromium
```

**Running E2E tests:**
```bash
# Headless mode (faster, for CI)
make test-e2e-headless

# Headed mode (see the browser)
make test-e2e

# Run specific E2E test
pytest tests/e2e/test_auth_e2e.py -v --headed
```

**E2E Test Coverage:**
- ✅ User authentication (login, logout, registration)
- ✅ Project management (view, create, navigate)
- ✅ Issue tracking (view, create, details)
- ✅ Comments (add, view)
- ✅ Protected routes and permissions

## Docker Deployment

```bash
# Build and start containers
make docker-build
make docker-up

# View logs
docker-compose logs -f

# Stop containers
make docker-down
```

## Development Workflow

1. **Create a feature branch**
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Make your changes**
   - Write code following the project structure
   - Add tests for new functionality
   - Update documentation if needed

3. **Format and lint your code**
   ```bash
   make format
   make lint
   ```

4. **Run tests**
   ```bash
   make test
   ```

5. **Commit and push**
   ```bash
   git add .
   git commit -m "Add my feature"
   git push origin feature/my-feature
   ```

## Database Migrations

When you modify database models:

```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Review the generated migration in alembic/versions/

# Apply migrations
make migrate

# or
alembic upgrade head

# Rollback last migration
alembic downgrade -1
```

## Environment Variables

Create a `.env` file in the project root (copy from `.env.example`):

```env
# Application
APP_NAME="Issue Tracker"
DEBUG=True
SECRET_KEY=your-secret-key-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=sqlite:///./issue_tracker.db

# JWT
JWT_SECRET_KEY=your-jwt-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Server
HOST=0.0.0.0
PORT=8000
```

## Architecture

### Layered Architecture

The application follows a clean layered architecture:

1. **Routes** (`routes/`) - Handle HTTP requests and responses
2. **Services** (`services/`) - Business logic and orchestration
3. **Repositories** (`repositories/`) - Database access layer
4. **Models** (`models/`) - SQLAlchemy ORM models
5. **Schemas** (`schemas/`) - Pydantic validation and serialization

### Domain Models

- **User** - Application users with roles (admin/user)
- **Project** - Workspaces for organizing issues
- **ProjectMember** - User membership in projects with roles
- **Issue** - Trackable items with status, type, and priority
- **Comment** - Discussions on issues
- **Tag** - Labels for organizing issues

### Authentication Flow

1. User registers with email/username/password
2. Password is hashed with bcrypt
3. User logs in with credentials
4. Server returns JWT token
5. Client includes token in Authorization header
6. Protected endpoints validate token and extract user info

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Ensure all tests pass and code is formatted
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues, questions, or contributions, please open an issue on the GitHub repository.
