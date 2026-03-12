# End-to-End Testing with Playwright

This project includes comprehensive E2E tests using Playwright to test the complete application flow in real browsers.

## Setup

### Initial Setup (One Time)

```bash
# Install Playwright and dependencies
make install-dev

# Install Playwright browsers
./venv/bin/playwright install chromium
```

## Running E2E Tests

### Quick Commands

```bash
# Run E2E tests (headed mode - see the browser)
make test-e2e

# Run E2E tests (headless mode - faster, for CI)
make test-e2e-headless

# Run all tests including E2E
make test-all
```

### Advanced Usage

```bash
# Run specific E2E test file
pytest tests/e2e/test_auth_e2e.py -v --headed

# Run specific test
pytest tests/e2e/test_auth_e2e.py::test_login_success -v --headed

# Run with specific browser
pytest tests/e2e/ --browser firefox --headed

# Run with slow motion (500ms between actions)
pytest tests/e2e/ --slowmo 500 --headed

# Generate test artifacts (videos, screenshots) on failure
pytest tests/e2e/ --video on --screenshot on
```

## Test Coverage

### Authentication Tests (`test_auth_e2e.py`)

- ✅ Home page loads correctly
- ✅ Successful login flow
- ✅ Invalid credentials handling
- ✅ Logout functionality
- ✅ User registration
- ✅ Protected routes require authentication

### Project Tests (`test_projects_e2e.py`)

- ✅ View projects list
- ✅ Create new project
- ✅ Duplicate project key validation
- ✅ Navigate to project issues
- ✅ Cancel project creation

### Issue Tests (`test_issues_e2e.py`)

- ✅ View issues list
- ✅ View issue details
- ✅ Add comments to issues
- ✅ Empty comment validation
- ✅ Issue status badges display
- ✅ View comments on issue
- ✅ View no comments message
- ✅ Comment appears after adding
- ✅ Comment metadata displayed (author, timestamp)
- ✅ Multiple comments displayed
- ✅ Create new issue button navigation
- ✅ Create new issue with form
- ✅ Cancel issue creation
- ✅ Edit issue button visible
- ✅ Edit issue modal opens
- ✅ Edit issue form populated with current data
- ✅ Update issue status (e.g., close issue)
- ✅ Cancel issue edit

## Test Structure

```
tests/e2e/
├── __init__.py
├── conftest.py              # Shared fixtures (authenticated_page)
├── test_auth_e2e.py         # Authentication flow tests (6 tests)
├── test_projects_e2e.py     # Project management tests (5 tests)
└── test_issues_e2e.py       # Issue tracking & comments tests (18 tests)
```

## Fixtures

### `base_url`
Provides the base URL for the application (http://localhost:8000).

### `authenticated_page`
Returns a Playwright page object that's already logged in as admin.
Automatically logs out after the test completes.

**Usage:**
```python
def test_something(authenticated_page: Page, base_url: str):
    page = authenticated_page
    # Page is already logged in and on /projects
    page.click('button:has-text("Create Project")')
```

## Writing New E2E Tests

### Basic Structure

```python
import pytest
from playwright.sync_api import Page, expect

@pytest.mark.e2e
def test_my_feature(authenticated_page: Page, base_url: str):
    """Test description"""
    page = authenticated_page

    # Navigate
    page.goto(f"{base_url}/my-page")

    # Interact
    page.click('button:has-text("Click Me")')
    page.fill('input[name="field"]', "value")

    # Assert
    expect(page.locator("#result")).to_contain_text("Expected")
```

### Best Practices

1. **Use descriptive test names** - `test_user_can_create_project_with_valid_data`

2. **Use semantic locators** - Prefer text content and roles over CSS selectors:
   ```python
   # Good
   page.click('button:has-text("Submit")')
   page.get_by_role("button", name="Submit").click()

   # Avoid
   page.click("#submit-btn")
   ```

3. **Add explicit waits** - Wait for elements to be ready:
   ```python
   page.wait_for_selector("table", timeout=5000)
   expect(page.locator("table")).to_be_visible()
   ```

4. **Use the `authenticated_page` fixture** - Don't repeat login logic:
   ```python
   # Good
   def test_something(authenticated_page: Page):
       page = authenticated_page
       # Already logged in

   # Avoid - unless testing login itself
   def test_something(page: Page):
       page.goto("/login")
       page.fill('input[name="username"]', "admin")
       # ...
   ```

5. **Mark E2E tests** - Always add the `@pytest.mark.e2e` decorator:
   ```python
   @pytest.mark.e2e
   def test_my_feature(page: Page):
       ...
   ```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: E2E Tests

on: [push, pull_request]

jobs:
  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements-dev.txt
          playwright install --with-deps chromium

      - name: Start application
        run: |
          make db-init
          make migrate
          make seed
          make run &
          sleep 5

      - name: Run E2E tests
        run: make test-e2e-headless

      - name: Upload test artifacts
        if: failure()
        uses: actions/upload-artifact@v2
        with:
          name: playwright-artifacts
          path: test-results/
```

## Debugging E2E Tests

### Run in Headed Mode
See what's happening in the browser:
```bash
pytest tests/e2e/ --headed
```

### Slow Motion
Add delays between actions:
```bash
pytest tests/e2e/ --headed --slowmo 1000
```

### Debug Mode
Use Playwright Inspector:
```bash
PWDEBUG=1 pytest tests/e2e/test_auth_e2e.py::test_login_success
```

### Screenshots and Videos
Capture on failure:
```bash
pytest tests/e2e/ --screenshot only-on-failure --video retain-on-failure
```

### Browser Console Logs
Add to your test:
```python
page.on("console", lambda msg: print(f"CONSOLE: {msg.text}"))
```

## Troubleshooting

### Port Already in Use
Make sure the application is running on port 8000:
```bash
lsof -ti:8000  # Check what's using port 8000
```

### Tests Timeout
Increase timeout in conftest.py or individual tests:
```python
page.wait_for_selector("table", timeout=10000)  # 10 seconds
```

### Element Not Found
Check if element is in a frame or shadow DOM:
```python
# For iframes
frame = page.frame_locator("iframe")
frame.locator("button").click()
```

### Flaky Tests
Add explicit waits:
```python
# Wait for network idle
page.wait_for_load_state("networkidle")

# Wait for specific condition
page.wait_for_function("() => document.querySelectorAll('table tr').length > 0")
```

## Resources

- [Playwright Documentation](https://playwright.dev/python/)
- [Playwright Python API](https://playwright.dev/python/docs/api/class-playwright)
- [pytest-playwright Plugin](https://github.com/microsoft/playwright-pytest)
- [Best Practices](https://playwright.dev/python/docs/best-practices)

## Test Metrics

Current E2E test coverage:
- **29 E2E tests** across 3 test files
- **Coverage areas**: Authentication (6 tests), Projects (5 tests), Issues & Comments (18 tests)
- **Average execution time**: ~70 seconds (all E2E tests)
- **Browsers supported**: Chromium, Firefox, WebKit
