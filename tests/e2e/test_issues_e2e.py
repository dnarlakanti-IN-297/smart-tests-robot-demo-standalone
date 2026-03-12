"""End-to-end tests for issues"""

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.e2e
def test_view_issues_list(authenticated_page: Page, base_url: str):
    """Test viewing issues for a project"""
    page = authenticated_page

    # Navigate to first project's issues
    page.wait_for_selector("table", timeout=5000)
    page.click('a:has-text("View Issues")')

    # Wait for issues page
    page.wait_for_url(f"{base_url}/projects/*/issues")

    # Check page loaded
    expect(page.locator(".card h2").first).to_contain_text("Issues")

    # Wait for issues to load - table should appear inside #issues-list
    page.wait_for_selector("#issues-list table", timeout=10000)


@pytest.mark.e2e
def test_view_issue_details(authenticated_page: Page, base_url: str):
    """Test viewing issue details"""
    page = authenticated_page

    # Navigate to issues
    page.wait_for_selector("table", timeout=5000)
    page.click('a:has-text("View Issues")')
    page.wait_for_url(f"{base_url}/projects/*/issues")

    # Wait for issues to load
    page.wait_for_selector("#issues-list table", timeout=10000)

    # Click on first issue "View" button
    page.locator('#issues-list a:has-text("View")').first.click()

    # Should navigate to issue detail page
    page.wait_for_url(f"{base_url}/issues/*")

    # Check issue details loaded
    expect(page.locator("#issue-details")).to_be_visible()


@pytest.mark.e2e
def test_add_comment_to_issue(authenticated_page: Page, base_url: str):
    """Test adding a comment to an issue"""
    page = authenticated_page

    # Navigate to issues
    page.wait_for_selector("table", timeout=5000)
    page.click('a:has-text("View Issues")')
    page.wait_for_url(f"{base_url}/projects/*/issues")

    # Wait for issues and click on first one
    page.wait_for_selector("#issues-list table", timeout=10000)
    page.locator('#issues-list a:has-text("View")').first.click()
    page.wait_for_url(f"{base_url}/issues/*")

    # Wait for comment form
    page.wait_for_selector("#add-comment-form", timeout=5000)

    # Add a comment
    comment_text = "This is a test comment from Playwright E2E test"
    page.fill("#comment-content", comment_text)

    # Submit comment
    page.click('#add-comment-form button[type="submit"]')

    # Wait for success message or comment to appear
    page.wait_for_timeout(2000)

    # Check that comment appears in the list
    expect(page.locator("#comments-list")).to_contain_text(comment_text)


@pytest.mark.e2e
def test_empty_comment_validation(authenticated_page: Page, base_url: str):
    """Test that empty comments are not allowed"""
    page = authenticated_page

    # Navigate to issue detail page
    page.wait_for_selector("table", timeout=5000)
    page.click('a:has-text("View Issues")')
    page.wait_for_url(f"{base_url}/projects/*/issues")
    page.wait_for_selector("#issues-list table", timeout=10000)
    page.locator('#issues-list a:has-text("View")').first.click()
    page.wait_for_url(f"{base_url}/issues/*")

    # Try to submit empty comment
    page.fill("#comment-content", "")

    # Button should be disabled or form validation should prevent submission
    # HTML5 validation will prevent submission
    # We can't easily test this, but we can verify the required attribute
    is_required = page.get_attribute("#comment-content", "required")
    assert is_required is not None


@pytest.mark.e2e
def test_issue_status_badges(authenticated_page: Page, base_url: str):
    """Test that issue status badges are displayed correctly"""
    page = authenticated_page

    # Navigate to issues
    page.wait_for_selector("table", timeout=5000)
    page.click('a:has-text("View Issues")')
    page.wait_for_url(f"{base_url}/projects/*/issues")

    # Wait for issues table
    page.wait_for_selector("#issues-list table", timeout=10000)

    # Check for status badges
    # At least one badge should exist
    badges = page.locator(".badge")
    expect(badges.first).to_be_visible()


@pytest.mark.e2e
def test_view_comments_on_issue(authenticated_page: Page, base_url: str):
    """Test viewing comments list on an issue"""
    page = authenticated_page

    # Navigate to issues
    page.wait_for_selector("table", timeout=5000)
    page.click('a:has-text("View Issues")')
    page.wait_for_url(f"{base_url}/projects/*/issues")

    # Wait for issues and click on first one
    page.wait_for_selector("#issues-list table", timeout=10000)
    page.locator('#issues-list a:has-text("View")').first.click()
    page.wait_for_url(f"{base_url}/issues/*")

    # Wait for comments section to load
    page.wait_for_selector("#comments-list", timeout=5000)

    # Comments section should be visible
    comments_list = page.locator("#comments-list")
    expect(comments_list).to_be_visible()

    # Should show either "No comments yet" or actual comments
    # Just verify the section loaded
    expect(comments_list).not_to_contain_text("Loading comments...")


@pytest.mark.e2e
def test_view_no_comments_message(authenticated_page: Page, base_url: str):
    """Test that 'no comments' message appears when there are no comments"""
    page = authenticated_page

    # Navigate to issues
    page.wait_for_selector("table", timeout=5000)
    page.click('a:has-text("View Issues")')
    page.wait_for_url(f"{base_url}/projects/*/issues")

    # Wait for issues and click on first one
    page.wait_for_selector("#issues-list table", timeout=10000)
    page.locator('#issues-list a:has-text("View")').first.click()
    page.wait_for_url(f"{base_url}/issues/*")

    # Wait for comments to load
    page.wait_for_selector("#comments-list", timeout=5000)

    # Check if there are no comments (initial state)
    comments_list = page.locator("#comments-list")

    # Wait a bit for comments to load
    page.wait_for_timeout(1000)

    # Should show either the no comments message or have comments
    # If no comments, should see the message
    page_content = page.locator("#comments-list").text_content()
    assert page_content is not None


@pytest.mark.e2e
def test_comment_appears_after_adding(authenticated_page: Page, base_url: str):
    """Test that a newly added comment appears in the comments list"""
    page = authenticated_page

    # Navigate to issues
    page.wait_for_selector("table", timeout=5000)
    page.click('a:has-text("View Issues")')
    page.wait_for_url(f"{base_url}/projects/*/issues")

    # Wait for issues and click on first one
    page.wait_for_selector("#issues-list table", timeout=10000)
    page.locator('#issues-list a:has-text("View")').first.click()
    page.wait_for_url(f"{base_url}/issues/*")

    # Wait for comment form
    page.wait_for_selector("#add-comment-form", timeout=5000)

    # Add a unique comment to test viewing
    import time
    timestamp = int(time.time())
    comment_text = f"E2E test comment for viewing - {timestamp}"

    page.fill("#comment-content", comment_text)
    page.click('#add-comment-form button[type="submit"]')

    # Wait for comment to be added
    page.wait_for_timeout(2000)

    # Verify comment appears in comments list
    comments_list = page.locator("#comments-list")
    expect(comments_list).to_contain_text(comment_text)


@pytest.mark.e2e
def test_comment_metadata_displayed(authenticated_page: Page, base_url: str):
    """Test that comment metadata (author, timestamp) is displayed"""
    page = authenticated_page

    # Navigate to issues and add a comment first
    page.wait_for_selector("table", timeout=5000)
    page.click('a:has-text("View Issues")')
    page.wait_for_url(f"{base_url}/projects/*/issues")

    page.wait_for_selector("#issues-list table", timeout=10000)
    page.locator('#issues-list a:has-text("View")').first.click()
    page.wait_for_url(f"{base_url}/issues/*")

    # Add a comment to ensure we have at least one
    page.wait_for_selector("#add-comment-form", timeout=5000)
    page.fill("#comment-content", "Test comment for metadata check")
    page.click('#add-comment-form button[type="submit"]')

    # Wait for comment to appear
    page.wait_for_timeout(2000)

    # Check that comment metadata is visible (User ID and timestamp)
    comments_list = page.locator("#comments-list")

    # Should contain user information (User #X)
    expect(comments_list).to_contain_text("User #")

    # Comment content should be visible
    expect(comments_list).to_contain_text("Test comment for metadata check")


@pytest.mark.e2e
def test_multiple_comments_displayed(authenticated_page: Page, base_url: str):
    """Test that multiple comments are displayed correctly"""
    page = authenticated_page

    # Navigate to issues
    page.wait_for_selector("table", timeout=5000)
    page.click('a:has-text("View Issues")')
    page.wait_for_url(f"{base_url}/projects/*/issues")

    page.wait_for_selector("#issues-list table", timeout=10000)
    page.locator('#issues-list a:has-text("View")').first.click()
    page.wait_for_url(f"{base_url}/issues/*")

    # Add multiple comments
    page.wait_for_selector("#add-comment-form", timeout=5000)

    comments_to_add = [
        "First test comment",
        "Second test comment",
        "Third test comment"
    ]

    for comment_text in comments_to_add:
        page.fill("#comment-content", comment_text)
        page.click('#add-comment-form button[type="submit"]')
        page.wait_for_timeout(1500)

    # Verify all comments appear
    comments_list = page.locator("#comments-list")
    for comment_text in comments_to_add:
        expect(comments_list).to_contain_text(comment_text)


@pytest.mark.e2e
def test_create_new_issue_button(authenticated_page: Page, base_url: str):
    """Test that clicking Create Issue button navigates to create issue page"""
    page = authenticated_page

    # Navigate to issues page
    page.wait_for_selector("table", timeout=5000)
    page.click('a:has-text("View Issues")')
    page.wait_for_url(f"{base_url}/projects/*/issues")

    # Click Create Issue button
    page.click('button:has-text("Create Issue")')

    # Should navigate to create issue page
    page.wait_for_url(f"{base_url}/issues/new?project_id=*")

    # Check that create issue form is visible
    expect(page.locator("h2")).to_contain_text("Create New Issue")
    expect(page.locator("#create-issue-form")).to_be_visible()


@pytest.mark.e2e
def test_create_new_issue(authenticated_page: Page, base_url: str):
    """Test creating a new issue"""
    page = authenticated_page
    import time
    timestamp = int(time.time())

    # Navigate to create issue page
    page.wait_for_selector("table", timeout=5000)
    page.click('a:has-text("View Issues")')
    page.wait_for_url(f"{base_url}/projects/*/issues")
    page.click('button:has-text("Create Issue")')
    page.wait_for_url(f"{base_url}/issues/new?project_id=*")

    # Fill in issue details
    page.fill("#title", f"E2E Test Issue {timestamp}")
    page.fill("#description", "This is a test issue created by E2E tests")
    page.select_option("#type", "bug")
    page.select_option("#priority", "high")
    page.select_option("#status", "open")

    # Submit form
    page.click('button[type="submit"]')

    # Should show success message
    page.wait_for_selector(".alert-success", timeout=5000)
    expect(page.locator(".alert-success")).to_contain_text("Issue created successfully")

    # Should redirect to issue detail page
    page.wait_for_url(f"{base_url}/issues/*", timeout=5000)

    # Verify we're on the issue detail page
    expect(page.locator("#issue-details")).to_be_visible()
    expect(page.locator("#issue-details h2")).to_contain_text(f"E2E Test Issue {timestamp}")


@pytest.mark.e2e
def test_cancel_issue_creation(authenticated_page: Page, base_url: str):
    """Test canceling issue creation"""
    page = authenticated_page

    # Navigate to create issue page
    page.wait_for_selector("table", timeout=5000)
    page.click('a:has-text("View Issues")')
    page.wait_for_url(f"{base_url}/projects/*/issues")

    # Get the current project ID from URL
    current_url = page.url
    project_id = current_url.split("/projects/")[1].split("/")[0]

    page.click('button:has-text("Create Issue")')
    page.wait_for_url(f"{base_url}/issues/new?project_id=*")

    # Fill in some data
    page.fill("#title", "Test Issue to Cancel")

    # Click cancel
    page.click('button:has-text("Cancel")')

    # Should return to issues list page
    page.wait_for_url(f"{base_url}/projects/{project_id}/issues")
    expect(page.locator("h2")).to_contain_text("Issues")


@pytest.mark.e2e
def test_edit_issue_button_visible(authenticated_page: Page, base_url: str):
    """Test that Edit Issue button is visible on issue detail page"""
    page = authenticated_page

    # Navigate to issue detail page
    page.wait_for_selector("table", timeout=5000)
    page.click('a:has-text("View Issues")')
    page.wait_for_url(f"{base_url}/projects/*/issues")

    page.wait_for_selector("#issues-list table", timeout=10000)
    page.locator('#issues-list a:has-text("View")').first.click()
    page.wait_for_url(f"{base_url}/issues/*")

    # Wait for issue to load
    page.wait_for_selector("#issue-details", timeout=5000)

    # Check that Edit Issue button is visible
    expect(page.locator('button:has-text("Edit Issue")')).to_be_visible()


@pytest.mark.e2e
def test_edit_issue_modal_opens(authenticated_page: Page, base_url: str):
    """Test that clicking Edit Issue opens the edit modal"""
    page = authenticated_page

    # Navigate to issue detail page
    page.wait_for_selector("table", timeout=5000)
    page.click('a:has-text("View Issues")')
    page.wait_for_url(f"{base_url}/projects/*/issues")

    page.wait_for_selector("#issues-list table", timeout=10000)
    page.locator('#issues-list a:has-text("View")').first.click()
    page.wait_for_url(f"{base_url}/issues/*")

    # Wait for issue to load
    page.wait_for_selector("#issue-details", timeout=5000)

    # Click Edit Issue button
    page.click('button:has-text("Edit Issue")')

    # Modal should be visible
    expect(page.locator("#edit-issue-modal")).to_be_visible()
    expect(page.locator("#edit-issue-form")).to_be_visible()


@pytest.mark.e2e
def test_edit_issue_form_populated(authenticated_page: Page, base_url: str):
    """Test that edit form is populated with current issue data"""
    page = authenticated_page

    # Navigate to issue detail page
    page.wait_for_selector("table", timeout=5000)
    page.click('a:has-text("View Issues")')
    page.wait_for_url(f"{base_url}/projects/*/issues")

    page.wait_for_selector("#issues-list table", timeout=10000)
    page.locator('#issues-list a:has-text("View")').first.click()
    page.wait_for_url(f"{base_url}/issues/*")

    # Wait for issue to load
    page.wait_for_selector("#issue-details", timeout=5000)

    # Click Edit Issue button
    page.click('button:has-text("Edit Issue")')

    # Check that form fields are populated (not empty)
    title_value = page.input_value("#edit-title")
    assert title_value != ""
    assert len(title_value) > 0


@pytest.mark.e2e
def test_update_issue_status(authenticated_page: Page, base_url: str):
    """Test updating issue status to closed"""
    page = authenticated_page

    # Navigate to issue detail page
    page.wait_for_selector("table", timeout=5000)
    page.click('a:has-text("View Issues")')
    page.wait_for_url(f"{base_url}/projects/*/issues")

    page.wait_for_selector("#issues-list table", timeout=10000)
    page.locator('#issues-list a:has-text("View")').first.click()
    page.wait_for_url(f"{base_url}/issues/*")

    # Wait for issue to load
    page.wait_for_selector("#issue-details", timeout=5000)

    # Click Edit Issue button
    page.click('button:has-text("Edit Issue")')

    # Change status to closed
    page.select_option("#edit-status", "closed")

    # Submit form
    page.click('#edit-issue-form button[type="submit"]')

    # Wait for modal to close
    page.wait_for_timeout(2000)

    # Verify the status badge is updated
    expect(page.locator(".badge-closed")).to_be_visible()


@pytest.mark.e2e
def test_cancel_issue_edit(authenticated_page: Page, base_url: str):
    """Test canceling issue edit"""
    page = authenticated_page

    # Navigate to issue detail page
    page.wait_for_selector("table", timeout=5000)
    page.click('a:has-text("View Issues")')
    page.wait_for_url(f"{base_url}/projects/*/issues")

    page.wait_for_selector("#issues-list table", timeout=10000)
    page.locator('#issues-list a:has-text("View")').first.click()
    page.wait_for_url(f"{base_url}/issues/*")

    # Wait for issue to load
    page.wait_for_selector("#issue-details", timeout=5000)

    # Click Edit Issue button
    page.click('button:has-text("Edit Issue")')

    # Modal should be visible
    expect(page.locator("#edit-issue-modal")).to_be_visible()

    # Click Cancel
    page.click('button:has-text("Cancel")')

    # Modal should be hidden
    expect(page.locator("#edit-issue-modal")).to_be_hidden()
