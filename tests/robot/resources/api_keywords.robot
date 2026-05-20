*** Settings ***
Documentation     Reusable keywords for API testing
Library           RequestsLibrary
Library           Collections
Library           String
Resource          variables.robot

*** Keywords ***
Create API Session
    [Documentation]    Create a session for API requests
    Create Session    api    ${BASE_URL}    verify=True

Delete API Session
    [Documentation]    Delete the API session
    Delete All Sessions

# ============================================================================
# Authentication Keywords
# ============================================================================

Register User
    [Arguments]    ${email}    ${username}    ${fullname}    ${password}
    [Documentation]    Register a new user
    ${user_data}=    Create Dictionary
    ...    email=${email}
    ...    username=${username}
    ...    full_name=${fullname}
    ...    password=${password}
    ${response}=    POST On Session    api    /api/auth/register
    ...    json=${user_data}
    ...    expected_status=any
    [Return]    ${response}

Login User
    [Arguments]    ${username}    ${password}
    [Documentation]    Login and return the response
    ${credentials}=    Create Dictionary
    ...    username=${username}
    ...    password=${password}
    ${response}=    POST On Session    api    /api/auth/login
    ...    json=${credentials}
    ...    expected_status=any
    [Return]    ${response}

Get Auth Token
    [Arguments]    ${username}    ${password}
    [Documentation]    Login and extract the access token
    ${response}=    Login User    ${username}    ${password}
    ${token}=    Get From Dictionary    ${response.json()}    access_token
    [Return]    ${token}

Create Auth Headers
    [Arguments]    ${token}
    [Documentation]    Create authorization headers with Bearer token
    ${headers}=    Create Dictionary
    ...    Authorization=Bearer ${token}
    ...    Content-Type=application/json
    [Return]    ${headers}

# ============================================================================
# User Management Keywords
# ============================================================================

Get Current User
    [Arguments]    ${token}
    [Documentation]    Get current user details using token
    ${headers}=    Create Auth Headers    ${token}
    ${response}=    GET On Session    api    /api/users/me
    ...    headers=${headers}
    ...    expected_status=any
    [Return]    ${response}

Get User By Id
    [Arguments]    ${user_id}    ${token}
    [Documentation]    Get user by ID
    ${headers}=    Create Auth Headers    ${token}
    ${response}=    GET On Session    api    /api/users/${user_id}
    ...    headers=${headers}
    ...    expected_status=any
    [Return]    ${response}

# ============================================================================
# Project Keywords
# ============================================================================

Create Project
    [Arguments]    ${name}    ${key}    ${description}    ${token}
    [Documentation]    Create a new project
    ${headers}=    Create Auth Headers    ${token}
    ${project_data}=    Create Dictionary
    ...    name=${name}
    ...    key=${key}
    ...    description=${description}
    ${response}=    POST On Session    api    /api/projects
    ...    json=${project_data}
    ...    headers=${headers}
    ...    expected_status=any
    [Return]    ${response}

Get Project By Id
    [Arguments]    ${project_id}    ${token}
    [Documentation]    Get project by ID
    ${headers}=    Create Auth Headers    ${token}
    ${response}=    GET On Session    api    /api/projects/${project_id}
    ...    headers=${headers}
    ...    expected_status=any
    [Return]    ${response}

Get All Projects
    [Arguments]    ${token}
    [Documentation]    Get all projects for current user
    ${headers}=    Create Auth Headers    ${token}
    ${response}=    GET On Session    api    /api/projects
    ...    headers=${headers}
    ...    expected_status=any
    [Return]    ${response}

Update Project
    [Arguments]    ${project_id}    ${token}    ${name}=${EMPTY}    ${description}=${EMPTY}
    [Documentation]    Update project details
    ${headers}=    Create Auth Headers    ${token}
    ${update_data}=    Create Dictionary
    Run Keyword If    '${name}' != '${EMPTY}'    Set To Dictionary    ${update_data}    name=${name}
    Run Keyword If    '${description}' != '${EMPTY}'    Set To Dictionary    ${update_data}    description=${description}
    ${response}=    PUT On Session    api    /api/projects/${project_id}
    ...    json=${update_data}
    ...    headers=${headers}
    ...    expected_status=any
    [Return]    ${response}

Delete Project
    [Arguments]    ${project_id}    ${token}
    [Documentation]    Delete a project
    ${headers}=    Create Auth Headers    ${token}
    ${response}=    DELETE On Session    api    /api/projects/${project_id}
    ...    headers=${headers}
    ...    expected_status=any
    [Return]    ${response}

# ============================================================================
# Issue Keywords
# ============================================================================

Create Issue
    [Arguments]    ${title}    ${project_id}    ${token}    ${description}=${EMPTY}    ${status}=${STATUS_OPEN}    ${type}=${TYPE_TASK}    ${priority}=${PRIORITY_MEDIUM}    ${assignee_id}=${NONE}
    [Documentation]    Create a new issue
    ${headers}=    Create Auth Headers    ${token}
    ${issue_data}=    Create Dictionary
    ...    title=${title}
    ...    project_id=${project_id}
    ...    status=${status}
    ...    type=${type}
    ...    priority=${priority}
    Run Keyword If    '${description}' != '${EMPTY}'    Set To Dictionary    ${issue_data}    description=${description}
    Run Keyword If    ${assignee_id} != ${NONE}    Set To Dictionary    ${issue_data}    assignee_id=${assignee_id}
    ${response}=    POST On Session    api    /api/issues
    ...    json=${issue_data}
    ...    headers=${headers}
    ...    expected_status=any
    [Return]    ${response}

Get Issue By Id
    [Arguments]    ${issue_id}    ${token}
    [Documentation]    Get issue by ID
    ${headers}=    Create Auth Headers    ${token}
    ${response}=    GET On Session    api    /api/issues/${issue_id}
    ...    headers=${headers}
    ...    expected_status=any
    [Return]    ${response}

Get All Issues
    [Arguments]    ${token}
    [Documentation]    Get all issues
    ${headers}=    Create Auth Headers    ${token}
    ${response}=    GET On Session    api    /api/issues
    ...    headers=${headers}
    ...    expected_status=any
    [Return]    ${response}

Update Issue
    [Arguments]    ${issue_id}    ${token}    ${title}=${EMPTY}    ${status}=${EMPTY}    ${description}=${EMPTY}
    [Documentation]    Update issue details
    ${headers}=    Create Auth Headers    ${token}
    ${update_data}=    Create Dictionary
    Run Keyword If    '${title}' != '${EMPTY}'    Set To Dictionary    ${update_data}    title=${title}
    Run Keyword If    '${status}' != '${EMPTY}'    Set To Dictionary    ${update_data}    status=${status}
    Run Keyword If    '${description}' != '${EMPTY}'    Set To Dictionary    ${update_data}    description=${description}
    ${response}=    PUT On Session    api    /api/issues/${issue_id}
    ...    json=${update_data}
    ...    headers=${headers}
    ...    expected_status=any
    [Return]    ${response}

Delete Issue
    [Arguments]    ${issue_id}    ${token}
    [Documentation]    Delete an issue
    ${headers}=    Create Auth Headers    ${token}
    ${response}=    DELETE On Session    api    /api/issues/${issue_id}
    ...    headers=${headers}
    ...    expected_status=any
    [Return]    ${response}

# ============================================================================
# Comment Keywords
# ============================================================================

Create Comment
    [Arguments]    ${issue_id}    ${content}    ${token}
    [Documentation]    Create a comment on an issue
    ${headers}=    Create Auth Headers    ${token}
    ${comment_data}=    Create Dictionary
    ...    content=${content}
    ...    issue_id=${issue_id}
    ${response}=    POST On Session    api    /api/comments
    ...    json=${comment_data}
    ...    headers=${headers}
    ...    expected_status=any
    [Return]    ${response}

Get Comments For Issue
    [Arguments]    ${issue_id}    ${token}
    [Documentation]    Get all comments for an issue
    ${headers}=    Create Auth Headers    ${token}
    ${response}=    GET On Session    api    /api/issues/${issue_id}/comments
    ...    headers=${headers}
    ...    expected_status=any
    [Return]    ${response}

Update Comment
    [Arguments]    ${comment_id}    ${content}    ${token}
    [Documentation]    Update a comment
    ${headers}=    Create Auth Headers    ${token}
    ${comment_data}=    Create Dictionary    content=${content}
    ${response}=    PUT On Session    api    /api/comments/${comment_id}
    ...    json=${comment_data}
    ...    headers=${headers}
    ...    expected_status=any
    [Return]    ${response}

Delete Comment
    [Arguments]    ${comment_id}    ${token}
    [Documentation]    Delete a comment
    ${headers}=    Create Auth Headers    ${token}
    ${response}=    DELETE On Session    api    /api/comments/${comment_id}
    ...    headers=${headers}
    ...    expected_status=any
    [Return]    ${response}

# ============================================================================
# Tag Keywords
# ============================================================================

Create Tag
    [Arguments]    ${name}    ${token}    ${color}=\#3498db
    [Documentation]    Create a new tag
    ${headers}=    Create Auth Headers    ${token}
    ${tag_data}=    Create Dictionary
    ...    name=${name}
    ...    color=${color}
    ${response}=    POST On Session    api    /api/tags
    ...    json=${tag_data}
    ...    headers=${headers}
    ...    expected_status=any
    [Return]    ${response}

Get All Tags
    [Arguments]    ${token}
    [Documentation]    Get all tags
    ${headers}=    Create Auth Headers    ${token}
    ${response}=    GET On Session    api    /api/tags
    ...    headers=${headers}
    ...    expected_status=any
    [Return]    ${response}

Delete Tag
    [Arguments]    ${tag_id}    ${token}
    [Documentation]    Delete a tag
    ${headers}=    Create Auth Headers    ${token}
    ${response}=    DELETE On Session    api    /api/tags/${tag_id}
    ...    headers=${headers}
    ...    expected_status=any
    [Return]    ${response}

# ============================================================================
# Validation Keywords
# ============================================================================

Response Status Should Be
    [Arguments]    ${response}    ${expected_status}
    [Documentation]    Verify response status code
    Should Be Equal As Numbers    ${response.status_code}    ${expected_status}

Response Should Contain Key
    [Arguments]    ${response}    ${key}
    [Documentation]    Verify response JSON contains a key
    ${json}=    Set Variable    ${response.json()}
    Dictionary Should Contain Key    ${json}    ${key}

Response Should Not Contain Key
    [Arguments]    ${response}    ${key}
    [Documentation]    Verify response JSON does not contain a key
    ${json}=    Set Variable    ${response.json()}
    Dictionary Should Not Contain Key    ${json}    ${key}

Response Field Should Equal
    [Arguments]    ${response}    ${field}    ${expected_value}
    [Documentation]    Verify response field equals expected value
    ${json}=    Set Variable    ${response.json()}
    ${actual_value}=    Get From Dictionary    ${json}    ${field}
    Should Be Equal As Strings    ${actual_value}    ${expected_value}
