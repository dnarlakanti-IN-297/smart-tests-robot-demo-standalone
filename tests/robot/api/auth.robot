*** Settings ***
Documentation     Authentication API Tests
...               Tests for user registration, login, and token validation
Library           RequestsLibrary
Library           Collections
Resource          ../resources/api_keywords.robot
Resource          ../resources/variables.robot
Resource          ../resources/setup_teardown.robot

Suite Setup       Suite Setup For API Tests
Suite Teardown    Suite Teardown For API Tests

*** Test Cases ***
Register New User Successfully
    [Documentation]    Test successful user registration with valid data
    [Tags]    auth    register    smoke
    ${email}=    Set Variable    newuser@example.com
    ${username}=    Set Variable    newuser
    ${response}=    Register User    ${email}    ${username}    New User    password123

    Response Status Should Be    ${response}    201
    Response Should Contain Key    ${response}    id
    Response Should Contain Key    ${response}    email
    Response Should Contain Key    ${response}    username
    Response Should Not Contain Key    ${response}    hashed_password
    Response Field Should Equal    ${response}    email    ${email}
    Response Field Should Equal    ${response}    username    ${username}

Register With Duplicate Email Should Fail
    [Documentation]    Test that registration fails when email already exists
    [Tags]    auth    register    validation
    # First registration
    ${email}=    Set Variable    duplicate@example.com
    ${response1}=    Register User    ${email}    user1    User One    password123
    Response Status Should Be    ${response1}    201

    # Second registration with same email, different username
    ${response2}=    Register User    ${email}    user2    User Two    password123
    Response Status Should Be    ${response2}    400
    Should Contain    ${response2.json()['detail']}    email

Register With Duplicate Username Should Fail
    [Documentation]    Test that registration fails when username already exists
    [Tags]    auth    register    validation
    # First registration
    ${username}=    Set Variable    duplicateuser
    ${response1}=    Register User    user1@example.com    ${username}    User One    password123
    Response Status Should Be    ${response1}    201

    # Second registration with same username, different email
    ${response2}=    Register User    user2@example.com    ${username}    User Two    password123
    Response Status Should Be    ${response2}    400
    Should Contain    ${response2.json()['detail']}    username

Register With Invalid Email Should Fail
    [Documentation]    Test that registration fails with invalid email format
    [Tags]    auth    register    validation
    ${response}=    Register User    notanemail    testuser    Test User    password123
    Response Status Should Be    ${response}    422

Register With Short Password Should Fail
    [Documentation]    Test that registration fails with password too short
    [Tags]    auth    register    validation
    ${response}=    Register User    test@example.com    testuser    Test User    123
    Response Status Should Be    ${response}    422

Login With Valid Credentials
    [Documentation]    Test successful login with correct username and password
    [Tags]    auth    login    smoke
    # Register user first
    ${username}=    Set Variable    loginuser
    ${password}=    Set Variable    password123
    Register User    login@example.com    ${username}    Login User    ${password}

    # Login
    ${response}=    Login User    ${username}    ${password}
    Response Status Should Be    ${response}    200
    Response Should Contain Key    ${response}    access_token
    Response Should Contain Key    ${response}    token_type
    Response Field Should Equal    ${response}    token_type    bearer

Login With Invalid Username Should Fail
    [Documentation]    Test that login fails with non-existent username
    [Tags]    auth    login    validation
    ${response}=    Login User    nonexistentuser    password123
    Response Status Should Be    ${response}    401

Login With Invalid Password Should Fail
    [Documentation]    Test that login fails with incorrect password
    [Tags]    auth    login    validation
    # Register user first
    ${username}=    Set Variable    wrongpassuser
    Register User    wrongpass@example.com    ${username}    Wrong Pass User    correctpass123

    # Login with wrong password
    ${response}=    Login User    ${username}    wrongpassword
    Response Status Should Be    ${response}    401

Access Protected Endpoint Without Token
    [Documentation]    Test that protected endpoints require authentication
    [Tags]    auth    authorization
    ${response}=    GET On Session    api    /api/users/me    expected_status=401

Access Protected Endpoint With Valid Token
    [Documentation]    Test accessing protected endpoint with valid JWT token
    [Tags]    auth    authorization    smoke
    # Register and login
    ${username}=    Set Variable    tokenuser
    ${password}=    Set Variable    password123
    Register User    token@example.com    ${username}    Token User    ${password}
    ${token}=    Get Auth Token    ${username}    ${password}

    # Access protected endpoint
    ${response}=    Get Current User    ${token}
    Response Status Should Be    ${response}    200
    Response Should Contain Key    ${response}    username
    Response Should Contain Key    ${response}    email
    Response Field Should Equal    ${response}    username    ${username}

Access Protected Endpoint With Invalid Token
    [Documentation]    Test that invalid tokens are rejected
    [Tags]    auth    authorization
    ${headers}=    Create Dictionary    Authorization=Bearer invalidtoken123
    ${response}=    GET On Session    api    /api/users/me
    ...    headers=${headers}
    ...    expected_status=401

*** Keywords ***
# No custom keywords needed for this test suite
