*** Settings ***
Documentation     Issue Lifecycle Integration Tests
...               Tests covering complete issue lifecycle from creation to closure
Library           RequestsLibrary
Library           Collections
Resource          ../resources/api_keywords.robot
Resource          ../resources/variables.robot
Resource          ../resources/setup_teardown.robot

Suite Setup       Suite Setup For API Tests
Suite Teardown    Suite Teardown For API Tests

*** Test Cases ***
Complete Issue Lifecycle Open To Closed
    [Documentation]    Test full issue lifecycle: open → in_progress → resolved → closed
    [Tags]    integration    lifecycle    smoke
    # Setup user and project
    Register User    lifecycle1@example.com    lifecycle1    Lifecycle User 1    password123
    ${token}=    Get Auth Token    lifecycle1    password123
    ${proj_response}=    Create Project    Lifecycle Project    LIFE    ${TEST_PROJECT_DESC}    ${token}
    ${project_id}=    Get From Dictionary    ${proj_response.json()}    id

    # Create issue (starts as open)
    ${issue_response}=    Create Issue    Issue to track through complete lifecycle    ${project_id}    ${token}
    ...    description=${TEST_ISSUE_DESC}
    Response Status Should Be    ${issue_response}    201
    ${issue_id}=    Get From Dictionary    ${issue_response.json()}    id
    Response Field Should Equal    ${issue_response}    status    ${STATUS_OPEN}

    # Transition to in_progress
    ${progress_response}=    Update Issue    ${issue_id}    ${token}    status=${STATUS_IN_PROGRESS}
    Response Status Should Be    ${progress_response}    200
    Response Field Should Equal    ${progress_response}    status    ${STATUS_IN_PROGRESS}

    # Add work comment
    Create Comment    ${issue_id}    Working on this issue, making good progress here    ${token}

    # Transition to resolved
    ${resolved_response}=    Update Issue    ${issue_id}    ${token}    status=${STATUS_RESOLVED}
    Response Status Should Be    ${resolved_response}    200
    Response Field Should Equal    ${resolved_response}    status    ${STATUS_RESOLVED}

    # Transition to closed
    ${closed_response}=    Update Issue    ${issue_id}    ${token}    status=${STATUS_CLOSED}
    Response Status Should Be    ${closed_response}    200
    Response Field Should Equal    ${closed_response}    status    ${STATUS_CLOSED}

Issue With Multiple Updates And Comments
    [Documentation]    Test issue with multiple updates and comments throughout lifecycle
    [Tags]    integration    lifecycle    updates
    # Setup
    Register User    updates@example.com    updates    Updates User    password123
    ${token}=    Get Auth Token    updates    password123
    ${proj_response}=    Create Project    Updates Project    UPDT    ${TEST_PROJECT_DESC}    ${token}
    ${project_id}=    Get From Dictionary    ${proj_response.json()}    id

    # Create issue
    ${issue_response}=    Create Issue    Issue requiring multiple updates and discussions    ${project_id}    ${token}
    ...    priority=${PRIORITY_MEDIUM}
    ${issue_id}=    Get From Dictionary    ${issue_response.json()}    id

    # Add initial analysis comment
    Create Comment    ${issue_id}    Initial analysis shows this requires more investigation    ${token}

    # Update title
    ${update1}=    Update Issue    ${issue_id}    ${token}
    ...    title=Updated issue requiring urgent attention and team review
    Response Status Should Be    ${update1}    200

    # Add findings comment
    Create Comment    ${issue_id}    Found the root cause, starting implementation now    ${token}

    # Move to in_progress
    ${update2}=    Update Issue    ${issue_id}    ${token}    status=${STATUS_IN_PROGRESS}
    Response Status Should Be    ${update2}    200

    # Add completion comment
    Create Comment    ${issue_id}    Implementation complete, ready for testing and review    ${token}

    # Resolve issue
    ${update3}=    Update Issue    ${issue_id}    ${token}    status=${STATUS_RESOLVED}
    Response Status Should Be    ${update3}    200

    # Verify all comments exist
    ${comments}=    Get Comments For Issue    ${issue_id}    ${token}
    Response Status Should Be    ${comments}    200
    ${comments_list}=    Set Variable    ${comments.json()}
    ${count}=    Get Length    ${comments_list}
    Should Be True    ${count} >= 3

Bug Fix Workflow With Type And Priority
    [Documentation]    Test bug fix workflow with type-specific handling
    [Tags]    integration    lifecycle    bug
    # Setup
    Register User    bugfix@example.com    bugfix    Bug Fix User    password123
    ${token}=    Get Auth Token    bugfix    password123
    ${proj_response}=    Create Project    Bug Fix Project    BUGFIX    ${TEST_PROJECT_DESC}    ${token}
    ${project_id}=    Get From Dictionary    ${proj_response.json()}    id

    # Report critical bug
    ${bug_response}=    Create Issue    Critical production bug affecting all users    ${project_id}    ${token}
    ...    type=${TYPE_BUG}
    ...    priority=${PRIORITY_CRITICAL}
    ...    description=Users are unable to login due to authentication service failure
    Response Status Should Be    ${bug_response}    201
    ${issue_id}=    Get From Dictionary    ${bug_response.json()}    id
    Response Field Should Equal    ${bug_response}    type    ${TYPE_BUG}
    Response Field Should Equal    ${bug_response}    priority    ${PRIORITY_CRITICAL}

    # Add triage comment
    ${triage}=    Create Comment    ${issue_id}    Triaged as P0, investigating authentication service logs    ${token}
    Response Status Should Be    ${triage}    201

    # Start working on bug
    ${start_work}=    Update Issue    ${issue_id}    ${token}    status=${STATUS_IN_PROGRESS}
    Response Status Should Be    ${start_work}    200

    # Add fix comment
    ${fix}=    Create Comment    ${issue_id}    Fixed authentication token validation, deploying hotfix    ${token}
    Response Status Should Be    ${fix}    201

    # Resolve bug
    ${resolve}=    Update Issue    ${issue_id}    ${token}    status=${STATUS_RESOLVED}
    Response Status Should Be    ${resolve}    200

    # Verify fix comment
    ${verify}=    Create Comment    ${issue_id}    Verified in production, all users can login successfully    ${token}
    Response Status Should Be    ${verify}    201

    # Close bug
    ${close}=    Update Issue    ${issue_id}    ${token}    status=${STATUS_CLOSED}
    Response Status Should Be    ${close}    200
    Response Field Should Equal    ${close}    status    ${STATUS_CLOSED}

Feature Request Workflow
    [Documentation]    Test feature request workflow from proposal to implementation
    [Tags]    integration    lifecycle    feature
    # Setup
    Register User    feature@example.com    feature    Feature User    password123
    ${token}=    Get Auth Token    feature    password123
    ${proj_response}=    Create Project    Feature Project    FEAT    ${TEST_PROJECT_DESC}    ${token}
    ${project_id}=    Get From Dictionary    ${proj_response.json()}    id

    # Create feature request
    ${feature_response}=    Create Issue    Add export functionality for user reports    ${project_id}    ${token}
    ...    type=${TYPE_FEATURE}
    ...    priority=${PRIORITY_MEDIUM}
    ...    description=Users need ability to export reports in CSV and PDF formats
    Response Status Should Be    ${feature_response}    201
    ${issue_id}=    Get From Dictionary    ${feature_response.json()}    id
    Response Field Should Equal    ${feature_response}    type    ${TYPE_FEATURE}

    # Add requirements comment
    ${requirements}=    Create Comment    ${issue_id}    Requirements gathered: CSV and PDF export with custom filters    ${token}
    Response Status Should Be    ${requirements}    201

    # Start implementation
    ${start}=    Update Issue    ${issue_id}    ${token}    status=${STATUS_IN_PROGRESS}
    Response Status Should Be    ${start}    200

    # Add progress comment
    ${progress}=    Create Comment    ${issue_id}    CSV export implemented, working on PDF generation next    ${token}
    Response Status Should Be    ${progress}    201

    # Complete implementation
    ${complete}=    Create Comment    ${issue_id}    Both CSV and PDF export completed, ready for testing    ${token}
    Response Status Should Be    ${complete}    201

    # Resolve feature
    ${resolve}=    Update Issue    ${issue_id}    ${token}    status=${STATUS_RESOLVED}
    Response Status Should Be    ${resolve}    200

    # Close after verification
    ${close}=    Update Issue    ${issue_id}    ${token}    status=${STATUS_CLOSED}
    Response Status Should Be    ${close}    200

    # Verify final state
    ${final}=    Get Issue By Id    ${issue_id}    ${token}
    Response Status Should Be    ${final}    200
    Response Field Should Equal    ${final}    status    ${STATUS_CLOSED}
    Response Field Should Equal    ${final}    type    ${TYPE_FEATURE}

*** Keywords ***
# No custom keywords needed for this test suite
