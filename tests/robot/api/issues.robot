*** Settings ***
Documentation     Issue API Tests
...               Tests for issue CRUD operations, assignment, and filtering
Library           RequestsLibrary
Library           Collections
Resource          ../resources/api_keywords.robot
Resource          ../resources/variables.robot
Resource          ../resources/setup_teardown.robot

Suite Setup       Suite Setup For API Tests
Suite Teardown    Suite Teardown For API Tests

*** Test Cases ***
Create Issue Successfully
    [Documentation]    Test creating a new issue with valid data
    [Tags]    issues    create    smoke
    # Setup: Register user and create project
    Register User    issueuser@example.com    issueuser    Issue User    password123
    ${token}=    Get Auth Token    issueuser    password123
    ${proj_response}=    Create Project    Issue Project    ISSPROJ    ${TEST_PROJECT_DESC}    ${token}
    ${project_id}=    Get From Dictionary    ${proj_response.json()}    id

    # Create issue
    ${response}=    Create Issue    ${TEST_ISSUE_TITLE}    ${project_id}    ${token}
    ...    description=${TEST_ISSUE_DESC}

    Response Status Should Be    ${response}    201
    Response Should Contain Key    ${response}    id
    Response Field Should Equal    ${response}    title    ${TEST_ISSUE_TITLE}
    Response Field Should Equal    ${response}    project_id    ${project_id}
    Response Field Should Equal    ${response}    status    ${STATUS_OPEN}

Create Issue With Short Title Should Fail
    [Documentation]    Test that issue title must be at least 20 characters
    [Tags]    issues    create    validation
    Register User    issueshort@example.com    issueshort    Issue Short    password123
    ${token}=    Get Auth Token    issueshort    password123
    ${proj_response}=    Create Project    Short Issue Proj    SHORTISS    ${TEST_PROJECT_DESC}    ${token}
    ${project_id}=    Get From Dictionary    ${proj_response.json()}    id

    ${response}=    Create Issue    Short title    ${project_id}    ${token}
    Response Status Should Be    ${response}    422

Create Issue Without Project Access Should Fail
    [Documentation]    Test that users cannot create issues in projects they don't have access to
    [Tags]    issues    create    authorization
    # User 1 creates project
    Register User    issueowner@example.com    issueowner    Issue Owner    password123
    ${token1}=    Get Auth Token    issueowner    password123
    ${proj_response}=    Create Project    Private Project    PRIVISS    ${TEST_PROJECT_DESC}    ${token1}
    ${project_id}=    Get From Dictionary    ${proj_response.json()}    id

    # User 2 tries to create issue
    Register User    issueoutside@example.com    issueoutside    Issue Outside    password123
    ${token2}=    Get Auth Token    issueoutside    password123
    ${response}=    Create Issue    ${TEST_ISSUE_TITLE}    ${project_id}    ${token2}
    Response Status Should Be    ${response}    403

Get Issue By Id
    [Documentation]    Test retrieving an issue by ID
    [Tags]    issues    read    smoke
    Register User    issueget@example.com    issueget    Issue Get    password123
    ${token}=    Get Auth Token    issueget    password123
    ${proj_response}=    Create Project    Get Issue Proj    GETISS    ${TEST_PROJECT_DESC}    ${token}
    ${project_id}=    Get From Dictionary    ${proj_response.json()}    id

    # Create issue
    ${create_response}=    Create Issue    ${TEST_ISSUE_TITLE}    ${project_id}    ${token}
    ${issue_id}=    Get From Dictionary    ${create_response.json()}    id

    # Get issue
    ${response}=    Get Issue By Id    ${issue_id}    ${token}
    Response Status Should Be    ${response}    200
    Response Field Should Equal    ${response}    id    ${issue_id}

Get Issue By Id Not Found
    [Documentation]    Test that getting non-existent issue returns 404
    [Tags]    issues    read    validation
    Register User    issuenotfound@example.com    issuenotfound    Issue Not Found    password123
    ${token}=    Get Auth Token    issuenotfound    password123

    ${response}=    Get Issue By Id    99999    ${token}
    Response Status Should Be    ${response}    404

Get All Issues
    [Documentation]    Test retrieving all issues user has access to
    [Tags]    issues    read
    Register User    issueall@example.com    issueall    Issue All    password123
    ${token}=    Get Auth Token    issueall    password123
    ${proj_response}=    Create Project    All Issues Proj    ALLISS    ${TEST_PROJECT_DESC}    ${token}
    ${project_id}=    Get From Dictionary    ${proj_response.json()}    id

    # Create multiple issues
    Create Issue    First issue with sufficient length for validation    ${project_id}    ${token}
    Create Issue    Second issue with sufficient length for validation    ${project_id}    ${token}

    # Get all issues
    ${response}=    Get All Issues    ${token}
    Response Status Should Be    ${response}    200
    ${issues}=    Set Variable    ${response.json()}
    ${count}=    Get Length    ${issues}
    Should Be True    ${count} >= 2

Update Issue Title Successfully
    [Documentation]    Test updating issue title
    [Tags]    issues    update
    Register User    issueupdate@example.com    issueupdate    Issue Update    password123
    ${token}=    Get Auth Token    issueupdate    password123
    ${proj_response}=    Create Project    Update Issue Proj    UPDISS    ${TEST_PROJECT_DESC}    ${token}
    ${project_id}=    Get From Dictionary    ${proj_response.json()}    id

    # Create issue
    ${create_response}=    Create Issue    Original issue title with sufficient length    ${project_id}    ${token}
    ${issue_id}=    Get From Dictionary    ${create_response.json()}    id

    # Update issue
    ${response}=    Update Issue    ${issue_id}    ${token}    title=Updated issue title with sufficient length for validation
    Response Status Should Be    ${response}    200
    Response Field Should Equal    ${response}    title    Updated issue title with sufficient length for validation

Update Issue Status Successfully
    [Documentation]    Test updating issue status through workflow
    [Tags]    issues    update    workflow
    Register User    issuestatus@example.com    issuestatus    Issue Status    password123
    ${token}=    Get Auth Token    issuestatus    password123
    ${proj_response}=    Create Project    Status Issue Proj    STATISS    ${TEST_PROJECT_DESC}    ${token}
    ${project_id}=    Get From Dictionary    ${proj_response.json()}    id

    # Create issue
    ${create_response}=    Create Issue    ${TEST_ISSUE_TITLE}    ${project_id}    ${token}
    ${issue_id}=    Get From Dictionary    ${create_response.json()}    id

    # Update status: open -> in_progress
    ${response1}=    Update Issue    ${issue_id}    ${token}    status=${STATUS_IN_PROGRESS}
    Response Status Should Be    ${response1}    200
    Response Field Should Equal    ${response1}    status    ${STATUS_IN_PROGRESS}

    # Update status: in_progress -> resolved
    ${response2}=    Update Issue    ${issue_id}    ${token}    status=${STATUS_RESOLVED}
    Response Status Should Be    ${response2}    200
    Response Field Should Equal    ${response2}    status    ${STATUS_RESOLVED}

Update Issue Without Access Should Fail
    [Documentation]    Test that only authorized users can update issues
    [Tags]    issues    update    authorization
    # User 1 creates issue
    Register User    issueowner2@example.com    issueowner2    Issue Owner2    password123
    ${token1}=    Get Auth Token    issueowner2    password123
    ${proj_response}=    Create Project    Owner Issue Proj    OWNISS    ${TEST_PROJECT_DESC}    ${token1}
    ${project_id}=    Get From Dictionary    ${proj_response.json()}    id
    ${create_response}=    Create Issue    ${TEST_ISSUE_TITLE}    ${project_id}    ${token1}
    ${issue_id}=    Get From Dictionary    ${create_response.json()}    id

    # User 2 tries to update
    Register User    issuehacker@example.com    issuehacker    Issue Hacker    password123
    ${token2}=    Get Auth Token    issuehacker    password123
    ${response}=    Update Issue    ${issue_id}    ${token2}    title=Hacked issue title with sufficient length
    Response Status Should Be    ${response}    403

Delete Issue Successfully
    [Documentation]    Test deleting an issue as creator
    [Tags]    issues    delete
    Register User    issuedelete@example.com    issuedelete    Issue Delete    password123
    ${token}=    Get Auth Token    issuedelete    password123
    ${proj_response}=    Create Project    Delete Issue Proj    DELISS    ${TEST_PROJECT_DESC}    ${token}
    ${project_id}=    Get From Dictionary    ${proj_response.json()}    id

    # Create issue
    ${create_response}=    Create Issue    ${TEST_ISSUE_TITLE}    ${project_id}    ${token}
    ${issue_id}=    Get From Dictionary    ${create_response.json()}    id

    # Delete issue
    ${response}=    Delete Issue    ${issue_id}    ${token}
    Response Status Should Be    ${response}    204

    # Verify deleted
    ${get_response}=    Get Issue By Id    ${issue_id}    ${token}
    Response Status Should Be    ${get_response}    404

Delete Issue Without Permission Should Fail
    [Documentation]    Test that only authorized users can delete issues
    [Tags]    issues    delete    authorization
    # User 1 creates issue
    Register User    issuedel1@example.com    issuedel1    Issue Del1    password123
    ${token1}=    Get Auth Token    issuedel1    password123
    ${proj_response}=    Create Project    Del Issue Proj2    DELISS2    ${TEST_PROJECT_DESC}    ${token1}
    ${project_id}=    Get From Dictionary    ${proj_response.json()}    id
    ${create_response}=    Create Issue    ${TEST_ISSUE_TITLE}    ${project_id}    ${token1}
    ${issue_id}=    Get From Dictionary    ${create_response.json()}    id

    # User 2 tries to delete
    Register User    issuedel2@example.com    issuedel2    Issue Del2    password123
    ${token2}=    Get Auth Token    issuedel2    password123
    ${response}=    Delete Issue    ${issue_id}    ${token2}
    Response Status Should Be    ${response}    403

Create Issue With Different Types
    [Documentation]    Test creating issues with different type values
    [Tags]    issues    create    types
    Register User    issuetype@example.com    issuetype    Issue Type    password123
    ${token}=    Get Auth Token    issuetype    password123
    ${proj_response}=    Create Project    Type Issue Proj    TYPEISS    ${TEST_PROJECT_DESC}    ${token}
    ${project_id}=    Get From Dictionary    ${proj_response.json()}    id

    # Create bug
    ${bug_response}=    Create Issue    Bug issue with sufficient length for validation    ${project_id}    ${token}    type=${TYPE_BUG}
    Response Status Should Be    ${bug_response}    201
    Response Field Should Equal    ${bug_response}    type    ${TYPE_BUG}

    # Create feature
    ${feature_response}=    Create Issue    Feature issue with sufficient length for validation    ${project_id}    ${token}    type=${TYPE_FEATURE}
    Response Status Should Be    ${feature_response}    201
    Response Field Should Equal    ${feature_response}    type    ${TYPE_FEATURE}

Create Issue With Different Priorities
    [Documentation]    Test creating issues with different priority values
    [Tags]    issues    create    priorities
    Register User    issueprio@example.com    issueprio    Issue Prio    password123
    ${token}=    Get Auth Token    issueprio    password123
    ${proj_response}=    Create Project    Prio Issue Proj    PRIOISS    ${TEST_PROJECT_DESC}    ${token}
    ${project_id}=    Get From Dictionary    ${proj_response.json()}    id

    # Create high priority issue
    ${high_response}=    Create Issue    High priority issue with sufficient length    ${project_id}    ${token}    priority=${PRIORITY_HIGH}
    Response Status Should Be    ${high_response}    201
    Response Field Should Equal    ${high_response}    priority    ${PRIORITY_HIGH}

    # Create low priority issue
    ${low_response}=    Create Issue    Low priority issue with sufficient length    ${project_id}    ${token}    priority=${PRIORITY_LOW}
    Response Status Should Be    ${low_response}    201
    Response Field Should Equal    ${low_response}    priority    ${PRIORITY_LOW}

*** Keywords ***
# No custom keywords needed for this test suite
