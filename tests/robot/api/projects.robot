*** Settings ***
Documentation     Project API Tests
...               Tests for project CRUD operations, members, and permissions
Library           RequestsLibrary
Library           Collections
Resource          ../resources/api_keywords.robot
Resource          ../resources/variables.robot
Resource          ../resources/setup_teardown.robot

Suite Setup       Suite Setup For API Tests
Suite Teardown    Suite Teardown For API Tests

*** Test Cases ***
Create Project Successfully
    [Documentation]    Test creating a new project with valid data
    [Tags]    projects    create    smoke
    # Register and login user
    Register User    projectuser@example.com    projectuser    Project User    password123
    ${token}=    Get Auth Token    projectuser    password123

    # Create project
    ${response}=    Create Project    Test Project    TESTPROJ    ${TEST_PROJECT_DESC}    ${token}

    Response Status Should Be    ${response}    201
    Response Should Contain Key    ${response}    id
    Response Field Should Equal    ${response}    name    Test Project
    Response Field Should Equal    ${response}    key    TESTPROJ
    Response Field Should Equal    ${response}    description    ${TEST_PROJECT_DESC}

Create Project With Duplicate Key Should Fail
    [Documentation]    Test that project key must be unique
    [Tags]    projects    create    validation
    Register User    projdup@example.com    projdup    Proj Dup    password123
    ${token}=    Get Auth Token    projdup    password123

    # First project
    ${response1}=    Create Project    First Project    DUPKEY    ${TEST_PROJECT_DESC}    ${token}
    Response Status Should Be    ${response1}    201

    # Second project with same key
    ${response2}=    Create Project    Second Project    DUPKEY    ${TEST_PROJECT_DESC}    ${token}
    Response Status Should Be    ${response2}    400
    Should Contain    ${response2.json()['detail']}    key

Create Project With Short Description Should Fail
    [Documentation]    Test that project description must be at least 50 characters
    [Tags]    projects    create    validation
    Register User    projshort@example.com    projshort    Proj Short    password123
    ${token}=    Get Auth Token    projshort    password123

    ${response}=    Create Project    Short Desc Project    SHORTDESC    Too short    ${token}
    Response Status Should Be    ${response}    422

Get Project By Id
    [Documentation]    Test retrieving a project by ID
    [Tags]    projects    read    smoke
    Register User    projget@example.com    projget    Proj Get    password123
    ${token}=    Get Auth Token    projget    password123

    # Create project
    ${create_response}=    Create Project    Get Project    GETPROJ    ${TEST_PROJECT_DESC}    ${token}
    ${project_id}=    Get From Dictionary    ${create_response.json()}    id

    # Get project
    ${response}=    Get Project By Id    ${project_id}    ${token}
    Response Status Should Be    ${response}    200
    Response Field Should Equal    ${response}    id    ${project_id}
    Response Field Should Equal    ${response}    name    Get Project

Get Project By Id Not Found
    [Documentation]    Test that getting non-existent project returns 404
    [Tags]    projects    read    validation
    Register User    projnotfound@example.com    projnotfound    Proj Not Found    password123
    ${token}=    Get Auth Token    projnotfound    password123

    ${response}=    Get Project By Id    99999    ${token}
    Response Status Should Be    ${response}    404

Get All Projects For User
    [Documentation]    Test retrieving all projects for current user
    [Tags]    projects    read
    Register User    projall@example.com    projall    Proj All    password123
    ${token}=    Get Auth Token    projall    password123

    # Create multiple projects
    Create Project    Project One    PROJ1    ${TEST_PROJECT_DESC}    ${token}
    Create Project    Project Two    PROJ2    ${TEST_PROJECT_DESC}    ${token}

    # Get all projects
    ${response}=    Get All Projects    ${token}
    Response Status Should Be    ${response}    200
    ${projects}=    Set Variable    ${response.json()}
    ${count}=    Get Length    ${projects}
    Should Be True    ${count} >= 2

Update Project Successfully
    [Documentation]    Test updating project name and description
    [Tags]    projects    update
    Register User    projupdate@example.com    projupdate    Proj Update    password123
    ${token}=    Get Auth Token    projupdate    password123

    # Create project
    ${create_response}=    Create Project    Original Name    UPDPROJ    ${TEST_PROJECT_DESC}    ${token}
    ${project_id}=    Get From Dictionary    ${create_response.json()}    id

    # Update project
    ${response}=    Update Project    ${project_id}    ${token}    name=Updated Name    description=This is an updated description with sufficient length for validation requirements
    Response Status Should Be    ${response}    200
    Response Field Should Equal    ${response}    name    Updated Name

Update Project Unauthorized Should Fail
    [Documentation]    Test that only project members can update projects
    [Tags]    projects    update    authorization
    # User 1 creates project
    Register User    projowner@example.com    projowner    Proj Owner    password123
    ${token1}=    Get Auth Token    projowner    password123
    ${create_response}=    Create Project    Owner Project    OWNPROJ    ${TEST_PROJECT_DESC}    ${token1}
    ${project_id}=    Get From Dictionary    ${create_response.json()}    id

    # User 2 tries to update
    Register User    projhacker@example.com    projhacker    Proj Hacker    password123
    ${token2}=    Get Auth Token    projhacker    password123
    ${response}=    Update Project    ${project_id}    ${token2}    name=Hacked Name
    Response Status Should Be    ${response}    403

Delete Project Successfully
    [Documentation]    Test deleting a project
    [Tags]    projects    delete
    Register User    projdelete@example.com    projdelete    Proj Delete    password123
    ${token}=    Get Auth Token    projdelete    password123

    # Create project
    ${create_response}=    Create Project    Delete Me    DELPROJ    ${TEST_PROJECT_DESC}    ${token}
    ${project_id}=    Get From Dictionary    ${create_response.json()}    id

    # Delete project
    ${response}=    Delete Project    ${project_id}    ${token}
    Response Status Should Be    ${response}    204

    # Verify deleted
    ${get_response}=    Get Project By Id    ${project_id}    ${token}
    Response Status Should Be    ${get_response}    404

Delete Project Unauthorized Should Fail
    [Documentation]    Test that only authorized users can delete projects
    [Tags]    projects    delete    authorization
    # User 1 creates project
    Register User    projdelowner@example.com    projdelowner    Del Owner    password123
    ${token1}=    Get Auth Token    projdelowner    password123
    ${create_response}=    Create Project    Protected Project    PROTPROJ    ${TEST_PROJECT_DESC}    ${token1}
    ${project_id}=    Get From Dictionary    ${create_response.json()}    id

    # User 2 tries to delete
    Register User    projdelhacker@example.com    projdelhacker    Del Hacker    password123
    ${token2}=    Get Auth Token    projdelhacker    password123
    ${response}=    Delete Project    ${project_id}    ${token2}
    Response Status Should Be    ${response}    403

Access Project Without Permission Should Fail
    [Documentation]    Test that users cannot access projects they're not members of
    [Tags]    projects    authorization
    # User 1 creates private project
    Register User    projprivate@example.com    projprivate    Proj Private    password123
    ${token1}=    Get Auth Token    projprivate    password123
    ${create_response}=    Create Project    Private Project    PRIVPROJ    ${TEST_PROJECT_DESC}    ${token1}
    ${project_id}=    Get From Dictionary    ${create_response.json()}    id

    # User 2 tries to access (depending on API implementation, might be 403 or 404)
    Register User    projoutsider@example.com    projoutsider    Proj Outsider    password123
    ${token2}=    Get Auth Token    projoutsider    password123
    ${response}=    Get Project By Id    ${project_id}    ${token2}
    # Response should be 403 or 404
    Should Be True    ${response.status_code} in [403, 404]

*** Keywords ***
# No custom keywords needed for this test suite
