*** Settings ***
Documentation     Team Collaboration Workflow Tests
...               Multi-user scenarios: cross-team issue assignment, review workflows,
...               commenting threads, and project membership patterns.
Library           RequestsLibrary
Library           Collections
Resource          ../resources/api_keywords.robot
Resource          ../resources/variables.robot
Resource          ../resources/setup_teardown.robot

Suite Setup       Suite Setup For API Tests
Suite Teardown    Suite Teardown For API Tests

Test Template     Simulate Team Collaboration

*** Test Cases ***                    SUFFIX    KEY
Team Collab 001                       tc001     TC001
Team Collab 002                       tc002     TC002
Team Collab 003                       tc003     TC003
Team Collab 004                       tc004     TC004
Team Collab 005                       tc005     TC005
Team Collab 006                       tc006     TC006
Team Collab 007                       tc007     TC007
Team Collab 008                       tc008     TC008
Team Collab 009                       tc009     TC009
Team Collab 010                       tc010     TC010
Team Collab 011                       tc011     TC011
Team Collab 012                       tc012     TC012
Team Collab 013                       tc013     TC013
Team Collab 014                       tc014     TC014
Team Collab 015                       tc015     TC015
Team Collab 016                       tc016     TC016
Team Collab 017                       tc017     TC017
Team Collab 018                       tc018     TC018
Team Collab 019                       tc019     TC019
Team Collab 020                       tc020     TC020
Team Collab 021                       tc021     TC021
Team Collab 022                       tc022     TC022
Team Collab 023                       tc023     TC023
Team Collab 024                       tc024     TC024
Team Collab 025                       tc025     TC025

*** Keywords ***
Simulate Team Collaboration
    [Arguments]    ${suffix}    ${key}
    # Two users collaborating on a project
    Register User    ${suffix}a@example.com    ${suffix}a    Lead ${suffix}    password123
    Register User    ${suffix}b@example.com    ${suffix}b    Dev ${suffix}    password123
    ${token_a}=    Get Auth Token    ${suffix}a    password123
    ${token_b}=    Get Auth Token    ${suffix}b    password123

    # Lead creates project and issues
    ${proj}=    Create Project    Team Project ${suffix}    ${key}    Team collaboration test project    ${token_a}
    Response Status Should Be    ${proj}    201
    ${proj_id}=    Get From Dictionary    ${proj.json()}    id

    # Lead creates 4 issues
    ${i1}=    Create Issue    Design new microservice architecture for billing    ${proj_id}    ${token_a}    type=${TYPE_FEATURE}    priority=${PRIORITY_HIGH}
    ${i1_id}=    Get From Dictionary    ${i1.json()}    id
    ${i2}=    Create Issue    Investigate performance regression in search API    ${proj_id}    ${token_a}    type=${TYPE_BUG}    priority=${PRIORITY_CRITICAL}
    ${i2_id}=    Get From Dictionary    ${i2.json()}    id
    ${i3}=    Create Issue    Write comprehensive API documentation for v2    ${proj_id}    ${token_a}    type=${TYPE_TASK}    priority=${PRIORITY_MEDIUM}
    ${i3_id}=    Get From Dictionary    ${i3.json()}    id
    ${i4}=    Create Issue    Implement automated deployment pipeline with rollback    ${proj_id}    ${token_a}    type=${TYPE_FEATURE}    priority=${PRIORITY_HIGH}
    ${i4_id}=    Get From Dictionary    ${i4.json()}    id

    # Lead adds context comments
    Create Comment    ${i1_id}    Architecture proposal attached, team review needed    ${token_a}
    Create Comment    ${i2_id}    Performance degraded after last deployment, urgent fix needed    ${token_a}
    Create Comment    ${i3_id}    Documentation must cover all public endpoints    ${token_a}

    # Dev starts working on assigned issues
    Update Issue    ${i2_id}    ${token_a}    status=${STATUS_IN_PROGRESS}
    Update Issue    ${i3_id}    ${token_a}    status=${STATUS_IN_PROGRESS}

    # Dev (user b) can see issues - get all issues in their scope
    ${b_issues}=    Get All Issues    ${token_b}
    Response Status Should Be    ${b_issues}    200

    # Dev comments on issues they have visibility to
    Create Comment    ${i2_id}    Profiling shows N+1 query issue in search service    ${token_a}
    Create Comment    ${i2_id}    Fix implemented with eager loading, reducing queries by 90 percent    ${token_a}

    # Lead resolves completed issues
    Update Issue    ${i2_id}    ${token_a}    status=${STATUS_RESOLVED}
    Update Issue    ${i3_id}    ${token_a}    status=${STATUS_RESOLVED}

    # Verify project state
    ${proj_check}=    Get Project By Id    ${proj_id}    ${token_a}
    Response Status Should Be    ${proj_check}    200

    # Lead starts feature work
    Update Issue    ${i1_id}    ${token_a}    status=${STATUS_IN_PROGRESS}
    Update Issue    ${i4_id}    ${token_a}    status=${STATUS_IN_PROGRESS}

    Create Comment    ${i4_id}    CI/CD pipeline scaffolding complete, adding rollback logic    ${token_a}
    Update Issue    ${i4_id}    ${token_a}    status=${STATUS_RESOLVED}
    Update Issue    ${i4_id}    ${token_a}    status=${STATUS_CLOSED}
