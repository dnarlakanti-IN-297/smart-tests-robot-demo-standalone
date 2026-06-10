*** Settings ***
Documentation     Bulk Issue Operations - Data Driven Tests
...               Each test creates 5 issues with comments and status transitions,
...               simulating a real sprint backlog processing workflow.
Library           RequestsLibrary
Library           Collections
Resource          ../resources/api_keywords.robot
Resource          ../resources/variables.robot
Resource          ../resources/setup_teardown.robot

Suite Setup       Suite Setup For API Tests
Suite Teardown    Suite Teardown For API Tests

Test Template     Run Bulk Issue Operations

*** Test Cases ***                   SUFFIX    KEY
Bulk Sprint Test 001                 bs001     BS001
Bulk Sprint Test 002                 bs002     BS002
Bulk Sprint Test 003                 bs003     BS003
Bulk Sprint Test 004                 bs004     BS004
Bulk Sprint Test 005                 bs005     BS005
Bulk Sprint Test 006                 bs006     BS006
Bulk Sprint Test 007                 bs007     BS007
Bulk Sprint Test 008                 bs008     BS008
Bulk Sprint Test 009                 bs009     BS009
Bulk Sprint Test 010                 bs010     BS010
Bulk Sprint Test 011                 bs011     BS011
Bulk Sprint Test 012                 bs012     BS012
Bulk Sprint Test 013                 bs013     BS013
Bulk Sprint Test 014                 bs014     BS014
Bulk Sprint Test 015                 bs015     BS015
Bulk Sprint Test 016                 bs016     BS016
Bulk Sprint Test 017                 bs017     BS017
Bulk Sprint Test 018                 bs018     BS018
Bulk Sprint Test 019                 bs019     BS019
Bulk Sprint Test 020                 bs020     BS020
Bulk Sprint Test 021                 bs021     BS021
Bulk Sprint Test 022                 bs022     BS022
Bulk Sprint Test 023                 bs023     BS023
Bulk Sprint Test 024                 bs024     BS024
Bulk Sprint Test 025                 bs025     BS025
Bulk Sprint Test 026                 bs026     BS026
Bulk Sprint Test 027                 bs027     BS027
Bulk Sprint Test 028                 bs028     BS028
Bulk Sprint Test 029                 bs029     BS029
Bulk Sprint Test 030                 bs030     BS030
Bulk Sprint Test 031                 bs031     BS031
Bulk Sprint Test 032                 bs032     BS032
Bulk Sprint Test 033                 bs033     BS033
Bulk Sprint Test 034                 bs034     BS034
Bulk Sprint Test 035                 bs035     BS035
Bulk Sprint Test 036                 bs036     BS036
Bulk Sprint Test 037                 bs037     BS037
Bulk Sprint Test 038                 bs038     BS038
Bulk Sprint Test 039                 bs039     BS039
Bulk Sprint Test 040                 bs040     BS040
Bulk Sprint Test 041                 bs041     BS041
Bulk Sprint Test 042                 bs042     BS042
Bulk Sprint Test 043                 bs043     BS043
Bulk Sprint Test 044                 bs044     BS044
Bulk Sprint Test 045                 bs045     BS045
Bulk Sprint Test 046                 bs046     BS046
Bulk Sprint Test 047                 bs047     BS047
Bulk Sprint Test 048                 bs048     BS048
Bulk Sprint Test 049                 bs049     BS049
Bulk Sprint Test 050                 bs050     BS050
Bulk Sprint Test 051                 bs051     BS051
Bulk Sprint Test 052                 bs052     BS052
Bulk Sprint Test 053                 bs053     BS053
Bulk Sprint Test 054                 bs054     BS054
Bulk Sprint Test 055                 bs055     BS055
Bulk Sprint Test 056                 bs056     BS056
Bulk Sprint Test 057                 bs057     BS057
Bulk Sprint Test 058                 bs058     BS058
Bulk Sprint Test 059                 bs059     BS059
Bulk Sprint Test 060                 bs060     BS060

*** Keywords ***
Run Bulk Issue Operations
    [Arguments]    ${suffix}    ${key}
    Register User    ${suffix}@example.com    ${suffix}    User ${suffix}    password123
    ${token}=    Get Auth Token    ${suffix}    password123
    ${proj}=    Create Project    Project ${suffix}    ${key}    Bulk operations test project for sprint simulation    ${token}
    Response Status Should Be    ${proj}    201
    ${proj_id}=    Get From Dictionary    ${proj.json()}    id

    # Issue 1: Bug workflow
    ${i1}=    Create Issue    Authentication service failing for enterprise users    ${proj_id}    ${token}
    ...    type=${TYPE_BUG}    priority=${PRIORITY_CRITICAL}
    Response Status Should Be    ${i1}    201
    ${i1_id}=    Get From Dictionary    ${i1.json()}    id
    Create Comment    ${i1_id}    Triaged as P0 - investigating authentication service logs    ${token}
    Create Comment    ${i1_id}    Root cause found in token validation middleware component    ${token}
    Update Issue    ${i1_id}    ${token}    status=${STATUS_IN_PROGRESS}
    Update Issue    ${i1_id}    ${token}    status=${STATUS_RESOLVED}

    # Issue 2: Feature workflow
    ${i2}=    Create Issue    Add bulk export functionality for project reports    ${proj_id}    ${token}
    ...    type=${TYPE_FEATURE}    priority=${PRIORITY_HIGH}
    Response Status Should Be    ${i2}    201
    ${i2_id}=    Get From Dictionary    ${i2.json()}    id
    Create Comment    ${i2_id}    Requirements gathered from product team and stakeholders    ${token}
    Create Comment    ${i2_id}    Implementation started with CSV export module complete    ${token}
    Update Issue    ${i2_id}    ${token}    status=${STATUS_IN_PROGRESS}
    Update Issue    ${i2_id}    ${token}    status=${STATUS_RESOLVED}

    # Issue 3: Task workflow
    ${i3}=    Create Issue    Refactor database connection pooling for performance    ${proj_id}    ${token}
    ...    type=${TYPE_TASK}    priority=${PRIORITY_MEDIUM}
    Response Status Should Be    ${i3}    201
    ${i3_id}=    Get From Dictionary    ${i3.json()}    id
    Create Comment    ${i3_id}    Analysis complete - current pool size is suboptimal    ${token}
    Create Comment    ${i3_id}    New pool configuration tested and validated in staging    ${token}
    Update Issue    ${i3_id}    ${token}    status=${STATUS_IN_PROGRESS}
    Update Issue    ${i3_id}    ${token}    status=${STATUS_RESOLVED}

    # Issue 4: Bug low priority
    ${i4}=    Create Issue    Minor UI alignment issue in dashboard header section    ${proj_id}    ${token}
    ...    type=${TYPE_BUG}    priority=${PRIORITY_LOW}
    Response Status Should Be    ${i4}    201
    ${i4_id}=    Get From Dictionary    ${i4.json()}    id
    Create Comment    ${i4_id}    CSS fix identified for the header alignment problem    ${token}
    Create Comment    ${i4_id}    Fix deployed and verified across all supported browsers    ${token}
    Update Issue    ${i4_id}    ${token}    status=${STATUS_IN_PROGRESS}
    Update Issue    ${i4_id}    ${token}    status=${STATUS_CLOSED}

    # Issue 5: Feature medium
    ${i5}=    Create Issue    Implement notification system for issue status changes    ${proj_id}    ${token}
    ...    type=${TYPE_FEATURE}    priority=${PRIORITY_MEDIUM}
    Response Status Should Be    ${i5}    201
    ${i5_id}=    Get From Dictionary    ${i5.json()}    id
    Create Comment    ${i5_id}    Email notification templates designed and reviewed    ${token}
    Create Comment    ${i5_id}    Notification service integrated with existing email provider    ${token}
    Update Issue    ${i5_id}    ${token}    status=${STATUS_IN_PROGRESS}
    Update Issue    ${i5_id}    ${token}    status=${STATUS_RESOLVED}

    # Verify all issues exist
    ${all}=    Get All Issues    ${token}
    Response Status Should Be    ${all}    200
