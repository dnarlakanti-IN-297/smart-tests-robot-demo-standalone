"""Playwright test configuration"""

import os
import time

import pytest
from playwright.sync_api import Page


@pytest.fixture(autouse=True)
def ci_demo_delay():
    """Add artificial delay for CI demo visibility"""
    if os.getenv('CI') or os.getenv('GITHUB_ACTIONS'):
        # Add 3 second delay per E2E test (longer than unit/integration)
        time.sleep(3)
    yield


@pytest.fixture(scope="session")
def base_url():
    """Base URL for the application"""
    return "http://localhost:8000"


@pytest.fixture
def authenticated_page(page: Page, base_url: str):
    """Page with authenticated user"""
    # Navigate to login page
    page.goto(f"{base_url}/login")

    # Fill in credentials
    page.fill('input[name="username"]', "admin")
    page.fill('input[name="password"]', "admin123")

    # Click login button
    page.click('button[type="submit"]')

    # Wait for redirect to projects page
    page.wait_for_url(f"{base_url}/projects", timeout=5000)

    yield page

    # Cleanup - logout
    page.evaluate("localStorage.clear()")
