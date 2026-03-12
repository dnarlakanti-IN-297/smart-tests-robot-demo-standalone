"""End-to-end tests for projects"""

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.e2e
def test_view_projects_list(authenticated_page: Page, base_url: str):
    """Test viewing projects list"""
    page = authenticated_page

    # Should be on projects page
    expect(page).to_have_url(f"{base_url}/projects")

    # Check page title
    expect(page.locator(".card h2").first).to_contain_text("My Projects")

    # Wait for projects to load
    page.wait_for_selector("table", timeout=5000)

    # Check that projects table exists
    expect(page.locator("table")).to_be_visible()

    # Check table headers (use first to avoid ambiguity)
    expect(page.locator("th").first).to_be_visible()
    expect(page.get_by_role("columnheader", name="Key")).to_be_visible()
    expect(page.get_by_role("columnheader", name="Name")).to_be_visible()
    expect(page.get_by_role("columnheader", name="Description")).to_be_visible()


@pytest.mark.e2e
def test_create_new_project(authenticated_page: Page, base_url: str):
    """Test creating a new project"""
    page = authenticated_page

    # Click create project button
    page.click('button:has-text("Create Project")')

    # Wait for modal to appear
    expect(page.locator("#create-project-modal")).to_be_visible()

    # Fill in project details
    page.fill('#create-project-modal input[id="name"]', "Test E2E Project")
    page.fill('#create-project-modal input[id="key"]', "E2E")
    page.fill('#create-project-modal textarea[id="description"]', "End-to-end test project")

    # Submit form
    page.click('#create-project-form button[type="submit"]')

    # Wait for modal to close
    page.wait_for_timeout(1000)

    # Check that project appears in list
    expect(page.locator("table")).to_contain_text("E2E")
    expect(page.locator("table")).to_contain_text("Test E2E Project")


@pytest.mark.e2e
def test_create_project_with_duplicate_key(authenticated_page: Page, base_url: str):
    """Test creating project with duplicate key shows error"""
    page = authenticated_page

    # Click create project button
    page.click('button:has-text("Create Project")')

    # Wait for modal
    expect(page.locator("#create-project-modal")).to_be_visible()

    # Fill in with existing project key
    page.fill('#create-project-modal input[id="name"]', "Duplicate Project")
    page.fill('#create-project-modal input[id="key"]', "IT")  # Existing key
    page.fill('#create-project-modal textarea[id="description"]', "This should fail")

    # Submit form
    page.click('#create-project-form button[type="submit"]')

    # Check for error message
    expect(page.locator("#modal-error")).to_contain_text("already exists")


@pytest.mark.e2e
def test_navigate_to_project_issues(authenticated_page: Page, base_url: str):
    """Test navigating to project issues page"""
    page = authenticated_page

    # Wait for projects to load
    page.wait_for_selector("table", timeout=5000)

    # Click "View Issues" on first project
    page.click('a:has-text("View Issues")')

    # Should navigate to issues page
    page.wait_for_url(f"{base_url}/projects/*/issues")

    # Check issues page loaded
    expect(page.locator("h2")).to_contain_text("Issues")


@pytest.mark.e2e
def test_cancel_project_creation(authenticated_page: Page, base_url: str):
    """Test canceling project creation"""
    page = authenticated_page

    # Open create project modal
    page.click('button:has-text("Create Project")')

    # Wait for modal
    expect(page.locator("#create-project-modal")).to_be_visible()

    # Fill in some data
    page.fill('#create-project-modal input[id="name"]', "Canceled Project")

    # Click cancel
    page.click('button:has-text("Cancel")')

    # Modal should close
    expect(page.locator("#create-project-modal")).to_be_hidden()

    # Form should be reset (check if name field is empty when reopened)
    page.click('button:has-text("Create Project")')
    name_value = page.input_value('#create-project-modal input[id="name"]')
    assert name_value == ""
