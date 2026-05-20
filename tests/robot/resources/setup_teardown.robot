*** Settings ***
Documentation     Suite setup and teardown keywords
Library           RequestsLibrary
Library           OperatingSystem
Resource          api_keywords.robot
Resource          variables.robot

*** Keywords ***
Suite Setup For API Tests
    [Documentation]    Setup for API test suites
    Create API Session
    Log    API session created successfully

Suite Teardown For API Tests
    [Documentation]    Teardown for API test suites
    Delete API Session
    Log    API session deleted successfully

Test Setup For Authenticated Tests
    [Documentation]    Setup for tests requiring authentication
    # Each test will handle its own user creation/login as needed
    No Operation

Test Teardown For Authenticated Tests
    [Documentation]    Teardown for authenticated tests
    # Cleanup is handled by database resets between test runs
    No Operation

Check Application Health
    [Documentation]    Verify application is running and healthy
    ${response}=    GET On Session    api    /health    expected_status=200
    Log    Application health check passed
    [Return]    ${response}
