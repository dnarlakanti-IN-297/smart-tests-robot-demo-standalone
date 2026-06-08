*** Settings ***
Documentation     Sprint Simulation Workflow Tests
...               Simulates a full sprint: backlog grooming, sprint planning,
...               daily standups (status updates), and sprint review.
Library           RequestsLibrary
Library           Collections
Resource          ../resources/api_keywords.robot
Resource          ../resources/variables.robot
Resource          ../resources/setup_teardown.robot

Suite Setup       Suite Setup For API Tests
Suite Teardown    Suite Teardown For API Tests

Test Template     Simulate Full Sprint

*** Test Cases ***                    SUFFIX    KEY
Sprint Simulation 001                 spr001    SP001
Sprint Simulation 002                 spr002    SP002
Sprint Simulation 003                 spr003    SP003
Sprint Simulation 004                 spr004    SP004
Sprint Simulation 005                 spr005    SP005
Sprint Simulation 006                 spr006    SP006
Sprint Simulation 007                 spr007    SP007
Sprint Simulation 008                 spr008    SP008
Sprint Simulation 009                 spr009    SP009
Sprint Simulation 010                 spr010    SP010
Sprint Simulation 011                 spr011    SP011
Sprint Simulation 012                 spr012    SP012
Sprint Simulation 013                 spr013    SP013
Sprint Simulation 014                 spr014    SP014
Sprint Simulation 015                 spr015    SP015
Sprint Simulation 016                 spr016    SP016
Sprint Simulation 017                 spr017    SP017
Sprint Simulation 018                 spr018    SP018
Sprint Simulation 019                 spr019    SP019
Sprint Simulation 020                 spr020    SP020
Sprint Simulation 021                 spr021    SP021
Sprint Simulation 022                 spr022    SP022
Sprint Simulation 023                 spr023    SP023
Sprint Simulation 024                 spr024    SP024
Sprint Simulation 025                 spr025    SP025
Sprint Simulation 026                 spr026    SP026
Sprint Simulation 027                 spr027    SP027
Sprint Simulation 028                 spr028    SP028
Sprint Simulation 029                 spr029    SP029
Sprint Simulation 030                 spr030    SP030

*** Keywords ***
Simulate Full Sprint
    [Arguments]    ${suffix}    ${key}
    Register User    ${suffix}@example.com    ${suffix}    Sprint User ${suffix}    password123
    ${token}=    Get Auth Token    ${suffix}    password123
    ${proj}=    Create Project    Sprint ${suffix}    ${key}    Sprint simulation project for ${suffix}    ${token}
    Response Status Should Be    ${proj}    201
    ${proj_id}=    Get From Dictionary    ${proj.json()}    id

    # Backlog: create 8 issues
    ${i1}=    Create Issue    Implement user authentication with OAuth2 provider    ${proj_id}    ${token}    type=${TYPE_FEATURE}    priority=${PRIORITY_HIGH}
    ${i1_id}=    Get From Dictionary    ${i1.json()}    id
    ${i2}=    Create Issue    Fix critical memory leak in background job processor    ${proj_id}    ${token}    type=${TYPE_BUG}    priority=${PRIORITY_CRITICAL}
    ${i2_id}=    Get From Dictionary    ${i2.json()}    id
    ${i3}=    Create Issue    Refactor API response serialization layer entirely    ${proj_id}    ${token}    type=${TYPE_TASK}    priority=${PRIORITY_MEDIUM}
    ${i3_id}=    Get From Dictionary    ${i3.json()}    id
    ${i4}=    Create Issue    Add pagination support to all list endpoints    ${proj_id}    ${token}    type=${TYPE_FEATURE}    priority=${PRIORITY_HIGH}
    ${i4_id}=    Get From Dictionary    ${i4.json()}    id
    ${i5}=    Create Issue    Update dependencies to latest secure versions    ${proj_id}    ${token}    type=${TYPE_TASK}    priority=${PRIORITY_MEDIUM}
    ${i5_id}=    Get From Dictionary    ${i5.json()}    id
    ${i6}=    Create Issue    Write integration tests for payment service module    ${proj_id}    ${token}    type=${TYPE_TASK}    priority=${PRIORITY_HIGH}
    ${i6_id}=    Get From Dictionary    ${i6.json()}    id
    ${i7}=    Create Issue    Implement rate limiting on public API endpoints    ${proj_id}    ${token}    type=${TYPE_FEATURE}    priority=${PRIORITY_MEDIUM}
    ${i7_id}=    Get From Dictionary    ${i7.json()}    id
    ${i8}=    Create Issue    Add database index for improved query performance    ${proj_id}    ${token}    type=${TYPE_TASK}    priority=${PRIORITY_LOW}
    ${i8_id}=    Get From Dictionary    ${i8.json()}    id

    # Sprint planning: add planning comments
    Create Comment    ${i1_id}    Sprint planning: estimated 3 story points for OAuth2 integration    ${token}
    Create Comment    ${i2_id}    Sprint planning: P0 bug must be fixed in this sprint iteration    ${token}
    Create Comment    ${i3_id}    Sprint planning: estimated 5 story points for refactoring work    ${token}
    Create Comment    ${i4_id}    Sprint planning: estimated 2 story points for pagination feature    ${token}

    # Day 1 standup: start top 4 items
    Update Issue    ${i1_id}    ${token}    status=${STATUS_IN_PROGRESS}
    Update Issue    ${i2_id}    ${token}    status=${STATUS_IN_PROGRESS}
    Update Issue    ${i3_id}    ${token}    status=${STATUS_IN_PROGRESS}
    Update Issue    ${i4_id}    ${token}    status=${STATUS_IN_PROGRESS}

    # Day 2 standup: progress updates
    Create Comment    ${i1_id}    Day 2: OAuth2 provider integration 50 percent complete    ${token}
    Create Comment    ${i2_id}    Day 2: Memory leak identified in job scheduler component    ${token}
    Create Comment    ${i3_id}    Day 2: Serialization layer refactor 30 percent complete    ${token}

    # Day 3: resolve bugs and complete features
    Create Comment    ${i2_id}    Fix deployed to staging, memory usage back to normal levels    ${token}
    Update Issue    ${i2_id}    ${token}    status=${STATUS_RESOLVED}
    Update Issue    ${i4_id}    ${token}    status=${STATUS_RESOLVED}

    # Day 4: complete remaining items
    Create Comment    ${i1_id}    OAuth2 integration complete and unit tests passing    ${token}
    Update Issue    ${i1_id}    ${token}    status=${STATUS_RESOLVED}
    Update Issue    ${i3_id}    ${token}    status=${STATUS_RESOLVED}

    # Sprint review: close completed items
    Update Issue    ${i1_id}    ${token}    status=${STATUS_CLOSED}
    Update Issue    ${i2_id}    ${token}    status=${STATUS_CLOSED}
    Update Issue    ${i3_id}    ${token}    status=${STATUS_CLOSED}
    Update Issue    ${i4_id}    ${token}    status=${STATUS_CLOSED}

    # Carry-over items stay open for next sprint
    ${all}=    Get All Issues    ${token}
    Response Status Should Be    ${all}    200
