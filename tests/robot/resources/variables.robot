*** Settings ***
Documentation     Common variables for Robot Framework tests

*** Variables ***
# Application URLs
${BASE_URL}              http://localhost:8000
${API_BASE}              ${BASE_URL}/api
${HEALTH_ENDPOINT}       ${BASE_URL}/health

# API Endpoints
${AUTH_REGISTER}         ${API_BASE}/auth/register
${AUTH_LOGIN}            ${API_BASE}/auth/login
${USERS_ME}              ${API_BASE}/users/me
${PROJECTS_ENDPOINT}     ${API_BASE}/projects
${ISSUES_ENDPOINT}       ${API_BASE}/issues
${COMMENTS_ENDPOINT}     ${API_BASE}/comments
${TAGS_ENDPOINT}         ${API_BASE}/tags

# Test Users - Default
${TEST_USER_EMAIL}       testuser@example.com
${TEST_USER_USERNAME}    testuser
${TEST_USER_PASSWORD}    password123
${TEST_USER_FULLNAME}    Test User

# Test Users - Admin
${ADMIN_EMAIL}           admin@example.com
${ADMIN_USERNAME}        admin
${ADMIN_PASSWORD}        admin123
${ADMIN_FULLNAME}        Admin User

# Test Users - Secondary
${USER2_EMAIL}           user2@example.com
${USER2_USERNAME}        user2
${USER2_PASSWORD}        password123
${USER2_FULLNAME}        User Two

# Test Project
${TEST_PROJECT_NAME}     Test Project
${TEST_PROJECT_KEY}      TEST
${TEST_PROJECT_DESC}     This is a test project for automated testing purposes

# Test Issue
${TEST_ISSUE_TITLE}      This is a test issue title with sufficient length
${TEST_ISSUE_DESC}       This is a detailed description for the test issue

# Test Comment
${TEST_COMMENT_CONTENT}  This is a test comment with sufficient length for validation

# HTTP Headers
${CONTENT_TYPE_JSON}     application/json
${ACCEPT_JSON}           application/json

# Timeouts
${TIMEOUT}               10s
${SHORT_TIMEOUT}         5s
${LONG_TIMEOUT}          30s

# Issue Status
${STATUS_OPEN}           open
${STATUS_IN_PROGRESS}    in_progress
${STATUS_RESOLVED}       resolved
${STATUS_CLOSED}         closed

# Issue Type
${TYPE_BUG}              bug
${TYPE_FEATURE}          feature
${TYPE_TASK}             task

# Issue Priority
${PRIORITY_LOW}          low
${PRIORITY_MEDIUM}       medium
${PRIORITY_HIGH}         high
${PRIORITY_CRITICAL}     critical

# User Roles
${ROLE_USER}             USER
${ROLE_ADMIN}            ADMIN

# Tag Colors (hex color codes)
${COLOR_RED}             ${{'\#ff0000'}}
${COLOR_GREEN}           ${{'\#00ff00'}}
${COLOR_BLUE}            ${{'\#3498db'}}
