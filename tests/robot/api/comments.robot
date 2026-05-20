*** Settings ***
Documentation     Comment API Tests
...               Tests for comment CRUD operations and authorization
Library           RequestsLibrary
Library           Collections
Resource          ../resources/api_keywords.robot
Resource          ../resources/variables.robot
Resource          ../resources/setup_teardown.robot

Suite Setup       Suite Setup For API Tests
Suite Teardown    Suite Teardown For API Tests

*** Test Cases ***
Create Comment Successfully
    [Documentation]    Test creating a comment on an issue
    [Tags]    comments    create    smoke
    # Setup: Register user, create project and issue
    Register User    commentuser@example.com    commentuser    Comment User    password123
    ${token}=    Get Auth Token    commentuser    password123
    ${proj_response}=    Create Project    Comment Project    COMPROJ    ${TEST_PROJECT_DESC}    ${token}
    ${project_id}=    Get From Dictionary    ${proj_response.json()}    id
    ${issue_response}=    Create Issue    ${TEST_ISSUE_TITLE}    ${project_id}    ${token}
    ${issue_id}=    Get From Dictionary    ${issue_response.json()}    id

    # Create comment
    ${response}=    Create Comment    ${issue_id}    ${TEST_COMMENT_CONTENT}    ${token}

    Response Status Should Be    ${response}    201
    Response Should Contain Key    ${response}    id
    Response Field Should Equal    ${response}    content    ${TEST_COMMENT_CONTENT}
    Response Field Should Equal    ${response}    issue_id    ${issue_id}

Create Comment With Short Content Should Fail
    [Documentation]    Test that comment content must be at least 15 characters
    [Tags]    comments    create    validation
    Register User    comshort@example.com    comshort    Com Short    password123
    ${token}=    Get Auth Token    comshort    password123
    ${proj_response}=    Create Project    Short Com Proj    SHORTCOM    ${TEST_PROJECT_DESC}    ${token}
    ${project_id}=    Get From Dictionary    ${proj_response.json()}    id
    ${issue_response}=    Create Issue    ${TEST_ISSUE_TITLE}    ${project_id}    ${token}
    ${issue_id}=    Get From Dictionary    ${issue_response.json()}    id

    ${response}=    Create Comment    ${issue_id}    Short text    ${token}
    Response Status Should Be    ${response}    422

Create Comment On Non-Existent Issue Should Fail
    [Documentation]    Test that creating comment on non-existent issue fails
    [Tags]    comments    create    validation
    Register User    comnotfound@example.com    comnotfound    Com Not Found    password123
    ${token}=    Get Auth Token    comnotfound    password123

    ${response}=    Create Comment    99999    ${TEST_COMMENT_CONTENT}    ${token}
    Response Status Should Be    ${response}    404

Get Comments For Issue
    [Documentation]    Test retrieving all comments for an issue
    [Tags]    comments    read    smoke
    Register User    comget@example.com    comget    Com Get    password123
    ${token}=    Get Auth Token    comget    password123
    ${proj_response}=    Create Project    Get Com Proj    GETCOM    ${TEST_PROJECT_DESC}    ${token}
    ${project_id}=    Get From Dictionary    ${proj_response.json()}    id
    ${issue_response}=    Create Issue    ${TEST_ISSUE_TITLE}    ${project_id}    ${token}
    ${issue_id}=    Get From Dictionary    ${issue_response.json()}    id

    # Create multiple comments
    Create Comment    ${issue_id}    First comment with sufficient length for validation    ${token}
    Create Comment    ${issue_id}    Second comment with sufficient length for validation    ${token}

    # Get comments
    ${response}=    Get Comments For Issue    ${issue_id}    ${token}
    Response Status Should Be    ${response}    200
    ${comments}=    Set Variable    ${response.json()}
    ${count}=    Get Length    ${comments}
    Should Be True    ${count} >= 2

Update Comment Successfully
    [Documentation]    Test updating a comment by its author
    [Tags]    comments    update
    Register User    comupdate@example.com    comupdate    Com Update    password123
    ${token}=    Get Auth Token    comupdate    password123
    ${proj_response}=    Create Project    Update Com Proj    UPDCOM    ${TEST_PROJECT_DESC}    ${token}
    ${project_id}=    Get From Dictionary    ${proj_response.json()}    id
    ${issue_response}=    Create Issue    ${TEST_ISSUE_TITLE}    ${project_id}    ${token}
    ${issue_id}=    Get From Dictionary    ${issue_response.json()}    id

    # Create comment
    ${create_response}=    Create Comment    ${issue_id}    Original comment with sufficient length    ${token}
    ${comment_id}=    Get From Dictionary    ${create_response.json()}    id

    # Update comment
    ${response}=    Update Comment    ${comment_id}    Updated comment with sufficient length for validation    ${token}
    Response Status Should Be    ${response}    200
    Response Field Should Equal    ${response}    content    Updated comment with sufficient length for validation

Update Comment By Non-Author Should Fail
    [Documentation]    Test that only comment author can update their comment
    [Tags]    comments    update    authorization
    # User 1 creates comment
    Register User    comauthor@example.com    comauthor    Com Author    password123
    ${token1}=    Get Auth Token    comauthor    password123
    ${proj_response}=    Create Project    Auth Com Proj    AUTHCOM    ${TEST_PROJECT_DESC}    ${token1}
    ${project_id}=    Get From Dictionary    ${proj_response.json()}    id
    ${issue_response}=    Create Issue    ${TEST_ISSUE_TITLE}    ${project_id}    ${token1}
    ${issue_id}=    Get From Dictionary    ${issue_response.json()}    id
    ${create_response}=    Create Comment    ${issue_id}    ${TEST_COMMENT_CONTENT}    ${token1}
    ${comment_id}=    Get From Dictionary    ${create_response.json()}    id

    # User 2 tries to update (Note: User 2 needs to be added as project member to have read access)
    Register User    comhacker@example.com    comhacker    Com Hacker    password123
    ${token2}=    Get Auth Token    comhacker    password123
    ${response}=    Update Comment    ${comment_id}    Hacked comment with sufficient length    ${token2}
    # Might be 403 or 404 depending on whether non-members can see the comment
    Should Be True    ${response.status_code} in [403, 404]

Delete Comment Successfully
    [Documentation]    Test deleting a comment by its author
    [Tags]    comments    delete
    Register User    comdelete@example.com    comdelete    Com Delete    password123
    ${token}=    Get Auth Token    comdelete    password123
    ${proj_response}=    Create Project    Delete Com Proj    DELCOM    ${TEST_PROJECT_DESC}    ${token}
    ${project_id}=    Get From Dictionary    ${proj_response.json()}    id
    ${issue_response}=    Create Issue    ${TEST_ISSUE_TITLE}    ${project_id}    ${token}
    ${issue_id}=    Get From Dictionary    ${issue_response.json()}    id
    ${create_response}=    Create Comment    ${issue_id}    ${TEST_COMMENT_CONTENT}    ${token}
    ${comment_id}=    Get From Dictionary    ${create_response.json()}    id

    # Delete comment
    ${response}=    Delete Comment    ${comment_id}    ${token}
    Response Status Should Be    ${response}    204

Delete Comment By Non-Author Should Fail
    [Documentation]    Test that only comment author can delete their comment
    [Tags]    comments    delete    authorization
    # User 1 creates comment
    Register User    comdel1@example.com    comdel1    Com Del1    password123
    ${token1}=    Get Auth Token    comdel1    password123
    ${proj_response}=    Create Project    Del Com Proj2    DELCOM2    ${TEST_PROJECT_DESC}    ${token1}
    ${project_id}=    Get From Dictionary    ${proj_response.json()}    id
    ${issue_response}=    Create Issue    ${TEST_ISSUE_TITLE}    ${project_id}    ${token1}
    ${issue_id}=    Get From Dictionary    ${issue_response.json()}    id
    ${create_response}=    Create Comment    ${issue_id}    ${TEST_COMMENT_CONTENT}    ${token1}
    ${comment_id}=    Get From Dictionary    ${create_response.json()}    id

    # User 2 tries to delete
    Register User    comdel2@example.com    comdel2    Com Del2    password123
    ${token2}=    Get Auth Token    comdel2    password123
    ${response}=    Delete Comment    ${comment_id}    ${token2}
    # Might be 403 or 404 depending on implementation
    Should Be True    ${response.status_code} in [403, 404]

*** Keywords ***
# No custom keywords needed for this test suite
