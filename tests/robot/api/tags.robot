*** Settings ***
Documentation     Tag API Tests
...               Tests for tag CRUD operations
Library           RequestsLibrary
Library           Collections
Resource          ../resources/api_keywords.robot
Resource          ../resources/variables.robot
Resource          ../resources/setup_teardown.robot

Suite Setup       Suite Setup For API Tests
Suite Teardown    Suite Teardown For API Tests

*** Test Cases ***
Create Tag Successfully
    [Documentation]    Test creating a new tag with valid data
    [Tags]    tags    create    smoke
    Register User    taguser@example.com    taguser    Tag User    password123
    ${token}=    Get Auth Token    taguser    password123

    ${response}=    Create Tag    enhancement    ${token}
    Response Status Should Be    ${response}    201
    Response Should Contain Key    ${response}    id
    Response Field Should Equal    ${response}    name    enhancement

Create Tag With Custom Color
    [Documentation]    Test creating a tag with custom color
    [Tags]    tags    create
    Register User    tagcolor@example.com    tagcolor    Tag Color    password123
    ${token}=    Get Auth Token    tagcolor    password123

    ${response}=    Create Tag    urgent    ${token}    \#ff0000
    Response Status Should Be    ${response}    201
    Response Field Should Equal    ${response}    color    \#ff0000

Create Tag With Duplicate Name Should Fail
    [Documentation]    Test that tag names must be unique
    [Tags]    tags    create    validation
    Register User    tagdup@example.com    tagdup    Tag Dup    password123
    ${token}=    Get Auth Token    tagdup    password123

    # First tag
    ${response1}=    Create Tag    duplicate    ${token}
    Response Status Should Be    ${response1}    201

    # Second tag with same name
    ${response2}=    Create Tag    duplicate    ${token}
    Response Status Should Be    ${response2}    400

Get All Tags
    [Documentation]    Test retrieving all tags
    [Tags]    tags    read    smoke
    Register User    taggetall@example.com    taggetall    Tag Get All    password123
    ${token}=    Get Auth Token    taggetall    password123

    # Create multiple tags
    Create Tag    bug    ${token}
    Create Tag    feature    ${token}

    # Get all tags
    ${response}=    Get All Tags    ${token}
    Response Status Should Be    ${response}    200
    ${tags}=    Set Variable    ${response.json()}
    Should Not Be Empty    ${tags}

Delete Tag Successfully
    [Documentation]    Test deleting a tag
    [Tags]    tags    delete
    Register User    tagdel@example.com    tagdel    Tag Del    password123
    ${token}=    Get Auth Token    tagdel    password123

    # Create tag
    ${create_response}=    Create Tag    temporary    ${token}
    ${tag_id}=    Get From Dictionary    ${create_response.json()}    id

    # Delete tag
    ${response}=    Delete Tag    ${tag_id}    ${token}
    Response Status Should Be    ${response}    204

*** Keywords ***
# No custom keywords needed for this test suite
