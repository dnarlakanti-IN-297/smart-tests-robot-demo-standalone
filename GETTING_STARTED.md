# Getting Started with Issue Tracker

Quick guide to get the Issue Tracker application up and running in minutes.

## Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Git (optional)

## Quick Start (5 minutes)

### 1. Setup Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows
```

### 2. Install Dependencies

```bash
# Install all dependencies
make install-dev

# Or without make
pip install -r requirements-dev.txt
```

### 3. Setup Database

```bash
# One command to setup everything
make db-init && make migrate && make seed

# Or without make
python -m app.db.init_db
alembic upgrade head
python -m app.db.seed_data
```

### 4. Run the Application

```bash
# Start the server
make run

# Or without make
python run.py
```

**That's it!** The application is now running at:
- Web: http://localhost:8000
- API Docs: http://localhost:8000/api/docs

## Test Accounts

Login with these pre-seeded accounts:

| Username | Password    | Role  | Description          |
|----------|-------------|-------|----------------------|
| admin    | admin123    | Admin | Full access          |
| john     | password123 | User  | Regular user         |
| jane     | password123 | User  | Regular user         |

## First Steps

### Using the Web Interface

1. Open http://localhost:8000
2. Click "Login" and use one of the test accounts
3. Navigate to "Projects" to see existing projects
4. Create a new project or explore existing ones
5. Click "View Issues" to see issues in a project
6. Create new issues, add comments, and manage your work!

### Using the API

1. Open http://localhost:8000/api/docs
2. Try the `/api/auth/login` endpoint with test credentials
3. Copy the returned `access_token`
4. Click "Authorize" button at the top
5. Enter `Bearer <your-token>` (replace `<your-token>` with the actual token)
6. Now you can try all the API endpoints!

### Example API Workflow

```bash
# 1. Login and get token
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Response: {"access_token":"eyJ...","token_type":"bearer"}

# 2. Use token to get projects (replace TOKEN with your actual token)
curl http://localhost:8000/api/projects \
  -H "Authorization: Bearer TOKEN"

# 3. Create a new issue
curl -X POST http://localhost:8000/api/issues \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My first issue",
    "description": "This is a test issue",
    "project_id": 1,
    "status": "open",
    "type": "bug",
    "priority": "high"
  }'
```

## Running Tests

```bash
# Run all tests
make test

# Run with coverage
make test-cov

# View coverage report
open htmlcov/index.html  # macOS
# or
start htmlcov/index.html  # Windows
```

## Using Docker

```bash
# Build and start with Docker Compose
make docker-build
make docker-up

# Application runs at http://localhost:8000

# Stop containers
make docker-down
```

## Common Tasks

### Create a New User

```bash
# Via API
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "username": "newuser",
    "full_name": "New User",
    "password": "password123"
  }'
```

### Create a New Project

1. Login to web interface
2. Go to "Projects"
3. Click "Create Project"
4. Fill in name, key (2-10 uppercase letters), and description
5. Click "Create"

### Create an Issue

1. Go to a project's issues page
2. Click "Create Issue" (or use API)
3. Fill in the details
4. Optionally assign to a user and add tags
5. Click "Create"

### Add Comments

1. Open an issue detail page
2. Scroll to the comments section
3. Type your comment
4. Click "Add Comment"

## Development Tips

### Format Code Before Committing

```bash
make format  # Runs black and isort
```

### Check Code Quality

```bash
make lint  # Runs flake8 and mypy
```

### Database Migrations

```bash
# After modifying models, create a migration
alembic revision --autogenerate -m "Description of changes"

# Review the generated file in alembic/versions/

# Apply the migration
make migrate
```

### Reset Database

```bash
# Delete database and recreate
rm issue_tracker.db
make db-init
make migrate
make seed
```

## Troubleshooting

### Port Already in Use

If port 8000 is already in use, edit `.env` file:
```env
PORT=8001
```

### Database Errors

Delete the database and recreate:
```bash
rm issue_tracker.db test.db
make db-init
make migrate
make seed
```

### Import Errors

Make sure you've activated the virtual environment:
```bash
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows
```

### Tests Failing

Ensure test database is clean:
```bash
rm test.db
pytest
```

## Next Steps

- Read the [README.md](README.md) for full documentation
- Explore the [API Documentation](http://localhost:8000/api/docs)
- Check [CLAUDE.md](CLAUDE.md) for development guidelines
- Review the code structure in `app/` directory
- Look at test examples in `tests/` directory

## Need Help?

- Check the logs in the terminal where the server is running
- Open an issue on GitHub
- Review the FastAPI documentation: https://fastapi.tiangolo.com
- Review SQLAlchemy documentation: https://docs.sqlalchemy.org

## Quick Reference

```bash
# Makefile Commands
make help              # Show all commands
make install-dev       # Install dependencies
make run              # Start server
make test             # Run tests
make test-cov         # Run tests with coverage
make format           # Format code
make lint             # Check code quality
make clean            # Clean generated files
make docker-up        # Start with Docker
make db-init          # Initialize database
make migrate          # Run migrations
make seed             # Seed sample data
```

Happy tracking! 🚀
