*** Settings ***
Documentation     Project Workflow Integration Tests
...               End-to-end workflow tests covering multiple operations
Library           RequestsLibrary
Library           Collections
Resource          ../resources/api_keywords.robot
Resource          ../resources/variables.robot
Resource          ../resources/setup_teardown.robot

Suite Setup       Suite Setup For API Tests
Suite Teardown    Suite Teardown For API Tests

*** Test Cases ***
Complete Project Creation And Issue Workflow
    [Documentation]    Test complete workflow: create project → create issue → add comment
    [Tags]    integration    workflow    smoke
    # Register user and get token
    Register User    workflow1@example.com    workflow1    Workflow User 1    password123
    ${token}=    Get Auth Token    workflow1    password123

    # Create project
    ${proj_response}=    Create Project    Workflow Project    WFLOW    ${TEST_PROJECT_DESC}    ${token}
    Response Status Should Be    ${proj_response}    201
    ${project_id}=    Get From Dictionary    ${proj_response.json()}    id

    # Create issue in project
    ${issue_response}=    Create Issue    ${TEST_ISSUE_TITLE}    ${project_id}    ${token}
    ...    description=${TEST_ISSUE_DESC}
    Response Status Should Be    ${issue_response}    201
    ${issue_id}=    Get From Dictionary    ${issue_response.json()}    id

    # Add comment to issue
    ${comment_response}=    Create Comment    ${issue_id}    ${TEST_COMMENT_CONTENT}    ${token}
    Response Status Should Be    ${comment_response}    201

    # Verify all resources exist
    ${get_proj}=    Get Project By Id    ${project_id}    ${token}
    Response Status Should Be    ${get_proj}    200
    ${get_issue}=    Get Issue By Id    ${issue_id}    ${token}
    Response Status Should Be    ${get_issue}    200

Multi User Project Collaboration Workflow
    [Documentation]    Test workflow with multiple users collaborating on a project
    [Tags]    integration    workflow    collaboration
    # User 1 creates project
    Register User    collab1@example.com    collab1    Collab User 1    password123
    ${token1}=    Get Auth Token    collab1    password123
    ${proj_response}=    Create Project    Collaboration Project    COLLAB    ${TEST_PROJECT_DESC}    ${token1}
    ${project_id}=    Get From Dictionary    ${proj_response.json()}    id

    # User 1 creates issue
    ${issue_response}=    Create Issue    Collaborative issue requiring team input    ${project_id}    ${token1}
    ${issue_id}=    Get From Dictionary    ${issue_response.json()}    id

    # User 1 adds first comment
    ${comment1}=    Create Comment    ${issue_id}    First comment from project creator with sufficient length    ${token1}
    Response Status Should Be    ${comment1}    201

    # User 1 updates issue status
    ${update_response}=    Update Issue    ${issue_id}    ${token1}    status=${STATUS_IN_PROGRESS}
    Response Status Should Be    ${update_response}    200
    Response Field Should Equal    ${update_response}    status    ${STATUS_IN_PROGRESS}

Project With Tags And Issues Workflow
    [Documentation]    Test workflow: create project → create tags → create issues with tags
    [Tags]    integration    workflow    tags
    # Setup user and project
    Register User    tagflow@example.com    tagflow    Tag Flow User    password123
    ${token}=    Get Auth Token    tagflow    password123
    ${proj_response}=    Create Project    Tagged Project    TAGGED    ${TEST_PROJECT_DESC}    ${token}
    ${project_id}=    Get From Dictionary    ${proj_response.json()}    id

    # Create multiple tags
    ${red_color}=    Set Variable    \#ff0000
    ${green_color}=    Set Variable    \#00ff00
    ${bug_tag}=    Create Tag    bug    ${token}    ${red_color}
    Response Status Should Be    ${bug_tag}    201
    ${feature_tag}=    Create Tag    feature    ${token}    ${green_color}
    Response Status Should Be    ${feature_tag}    201

    # Create issues of different types
    ${bug_issue}=    Create Issue    Critical bug requiring immediate attention    ${project_id}    ${token}
    ...    type=${TYPE_BUG}    priority=${PRIORITY_HIGH}
    Response Status Should Be    ${bug_issue}    201

    ${feature_issue}=    Create Issue    New feature for enhancing user experience    ${project_id}    ${token}
    ...    type=${TYPE_FEATURE}    priority=${PRIORITY_MEDIUM}
    Response Status Should Be    ${feature_issue}    201

    # Verify all tags exist
    ${tags_response}=    Get All Tags    ${token}
    Response Status Should Be    ${tags_response}    200

Issue Priority And Type Combinations Workflow
    [Documentation]    Test creating issues with various priority and type combinations
    [Tags]    integration    workflow    combinations
    # Setup
    Register User    combo@example.com    combo    Combo User    password123
    ${token}=    Get Auth Token    combo    password123
    ${proj_response}=    Create Project    Combination Project    COMBO    ${TEST_PROJECT_DESC}    ${token}
    ${project_id}=    Get From Dictionary    ${proj_response.json()}    id

    # Create bug with critical priority
    ${critical_bug}=    Create Issue    Critical security vulnerability needs immediate fix    ${project_id}    ${token}
    ...    type=${TYPE_BUG}    priority=${PRIORITY_CRITICAL}
    Response Status Should Be    ${critical_bug}    201
    Response Field Should Equal    ${critical_bug}    type    ${TYPE_BUG}
    Response Field Should Equal    ${critical_bug}    priority    ${PRIORITY_CRITICAL}

    # Create feature with low priority
    ${low_feature}=    Create Issue    Nice to have feature for future consideration    ${project_id}    ${token}
    ...    type=${TYPE_FEATURE}    priority=${PRIORITY_LOW}
    Response Status Should Be    ${low_feature}    201
    Response Field Should Equal    ${low_feature}    type    ${TYPE_FEATURE}
    Response Field Should Equal    ${low_feature}    priority    ${PRIORITY_LOW}

    # Create task with medium priority
    ${medium_task}=    Create Issue    Regular maintenance task for system health    ${project_id}    ${token}
    ...    type=${TYPE_TASK}    priority=${PRIORITY_MEDIUM}
    Response Status Should Be    ${medium_task}    201
    Response Field Should Equal    ${medium_task}    type    ${TYPE_TASK}
    Response Field Should Equal    ${medium_task}    priority    ${PRIORITY_MEDIUM}

    # Verify all issues exist
    ${all_issues}=    Get All Issues    ${token}
    Response Status Should Be    ${all_issues}    200
    ${issues_list}=    Set Variable    ${all_issues.json()}
    ${count}=    Get Length    ${issues_list}
    Should Be True    ${count} >= 3

*** Keywords ***
# No custom keywords needed for this test suite
