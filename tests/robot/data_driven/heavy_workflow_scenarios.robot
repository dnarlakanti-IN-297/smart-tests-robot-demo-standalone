*** Settings ***
Documentation     Heavy Workflow Scenario Tests
...               Deep end-to-end scenarios: each test creates a full project ecosystem
...               with multiple users, 10+ issues, comment threads, and tag assignments.
...               Designed to simulate enterprise-scale test execution time.
Library           RequestsLibrary
Library           Collections
Resource          ../resources/api_keywords.robot
Resource          ../resources/variables.robot
Resource          ../resources/setup_teardown.robot

Suite Setup       Suite Setup For API Tests
Suite Teardown    Suite Teardown For API Tests

Test Template     Run Heavy Workflow Scenario

*** Test Cases ***                    SUFFIX    KEY
Heavy Scenario 001                    hws001    HW001
Heavy Scenario 002                    hws002    HW002
Heavy Scenario 003                    hws003    HW003
Heavy Scenario 004                    hws004    HW004
Heavy Scenario 005                    hws005    HW005
Heavy Scenario 006                    hws006    HW006
Heavy Scenario 007                    hws007    HW007
Heavy Scenario 008                    hws008    HW008
Heavy Scenario 009                    hws009    HW009
Heavy Scenario 010                    hws010    HW010
Heavy Scenario 011                    hws011    HW011
Heavy Scenario 012                    hws012    HW012
Heavy Scenario 013                    hws013    HW013
Heavy Scenario 014                    hws014    HW014
Heavy Scenario 015                    hws015    HW015
Heavy Scenario 016                    hws016    HW016
Heavy Scenario 017                    hws017    HW017
Heavy Scenario 018                    hws018    HW018
Heavy Scenario 019                    hws019    HW019
Heavy Scenario 020                    hws020    HW020
Heavy Scenario 021                    hws021    HW021
Heavy Scenario 022                    hws022    HW022
Heavy Scenario 023                    hws023    HW023
Heavy Scenario 024                    hws024    HW024
Heavy Scenario 025                    hws025    HW025
Heavy Scenario 026                    hws026    HW026
Heavy Scenario 027                    hws027    HW027
Heavy Scenario 028                    hws028    HW028
Heavy Scenario 029                    hws029    HW029
Heavy Scenario 030                    hws030    HW030
Heavy Scenario 031                    hws031    HW031
Heavy Scenario 032                    hws032    HW032
Heavy Scenario 033                    hws033    HW033
Heavy Scenario 034                    hws034    HW034
Heavy Scenario 035                    hws035    HW035
Heavy Scenario 036                    hws036    HW036
Heavy Scenario 037                    hws037    HW037
Heavy Scenario 038                    hws038    HW038
Heavy Scenario 039                    hws039    HW039
Heavy Scenario 040                    hws040    HW040
Heavy Scenario 041                    hws041    HW041
Heavy Scenario 042                    hws042    HW042
Heavy Scenario 043                    hws043    HW043
Heavy Scenario 044                    hws044    HW044
Heavy Scenario 045                    hws045    HW045
Heavy Scenario 046                    hws046    HW046
Heavy Scenario 047                    hws047    HW047
Heavy Scenario 048                    hws048    HW048
Heavy Scenario 049                    hws049    HW049
Heavy Scenario 050                    hws050    HW050
Heavy Scenario 051                    hws051    HW051
Heavy Scenario 052                    hws052    HW052
Heavy Scenario 053                    hws053    HW053
Heavy Scenario 054                    hws054    HW054
Heavy Scenario 055                    hws055    HW055
Heavy Scenario 056                    hws056    HW056
Heavy Scenario 057                    hws057    HW057
Heavy Scenario 058                    hws058    HW058
Heavy Scenario 059                    hws059    HW059
Heavy Scenario 060                    hws060    HW060
Heavy Scenario 061                    hws061    HW061
Heavy Scenario 062                    hws062    HW062
Heavy Scenario 063                    hws063    HW063
Heavy Scenario 064                    hws064    HW064
Heavy Scenario 065                    hws065    HW065
Heavy Scenario 066                    hws066    HW066
Heavy Scenario 067                    hws067    HW067
Heavy Scenario 068                    hws068    HW068
Heavy Scenario 069                    hws069    HW069
Heavy Scenario 070                    hws070    HW070
Heavy Scenario 071                    hws071    HW071
Heavy Scenario 072                    hws072    HW072
Heavy Scenario 073                    hws073    HW073
Heavy Scenario 074                    hws074    HW074
Heavy Scenario 075                    hws075    HW075
Heavy Scenario 076                    hws076    HW076
Heavy Scenario 077                    hws077    HW077
Heavy Scenario 078                    hws078    HW078
Heavy Scenario 079                    hws079    HW079
Heavy Scenario 080                    hws080    HW080

*** Keywords ***
Run Heavy Workflow Scenario
    [Arguments]    ${suffix}    ${key}
    Register User    ${suffix}@example.com    ${suffix}    Heavy ${suffix}    password123
    ${token}=    Get Auth Token    ${suffix}    password123
    ${proj}=    Create Project    Heavy Project ${suffix}    ${key}    Heavy workflow scenario project    ${token}
    Response Status Should Be    ${proj}    201
    ${proj_id}=    Get From Dictionary    ${proj.json()}    id

    # Create 3 tags for this project
    ${tag1}=    Create Tag    ${suffix}-backend    ${token}    #e74c3c
    Response Status Should Be    ${tag1}    201
    ${tag2}=    Create Tag    ${suffix}-frontend    ${token}    #2ecc71
    Response Status Should Be    ${tag2}    201
    ${tag3}=    Create Tag    ${suffix}-database    ${token}    #3498db
    Response Status Should Be    ${tag3}    201

    # Create 10 issues across all types and priorities
    ${i1}=    Create Issue    Backend service authentication is completely broken    ${proj_id}    ${token}    type=${TYPE_BUG}    priority=${PRIORITY_CRITICAL}
    ${i1_id}=    Get From Dictionary    ${i1.json()}    id
    ${i2}=    Create Issue    Frontend dashboard shows incorrect metrics data    ${proj_id}    ${token}    type=${TYPE_BUG}    priority=${PRIORITY_HIGH}
    ${i2_id}=    Get From Dictionary    ${i2.json()}    id
    ${i3}=    Create Issue    Database query performance degraded by fifty percent    ${proj_id}    ${token}    type=${TYPE_BUG}    priority=${PRIORITY_HIGH}
    ${i3_id}=    Get From Dictionary    ${i3.json()}    id
    ${i4}=    Create Issue    Implement real-time notifications using WebSocket protocol    ${proj_id}    ${token}    type=${TYPE_FEATURE}    priority=${PRIORITY_HIGH}
    ${i4_id}=    Get From Dictionary    ${i4.json()}    id
    ${i5}=    Create Issue    Add advanced search with full-text indexing support    ${proj_id}    ${token}    type=${TYPE_FEATURE}    priority=${PRIORITY_MEDIUM}
    ${i5_id}=    Get From Dictionary    ${i5.json()}    id
    ${i6}=    Create Issue    Create automated database backup and restore system    ${proj_id}    ${token}    type=${TYPE_FEATURE}    priority=${PRIORITY_MEDIUM}
    ${i6_id}=    Get From Dictionary    ${i6.json()}    id
    ${i7}=    Create Issue    Upgrade all Python dependencies to latest secure versions    ${proj_id}    ${token}    type=${TYPE_TASK}    priority=${PRIORITY_MEDIUM}
    ${i7_id}=    Get From Dictionary    ${i7.json()}    id
    ${i8}=    Create Issue    Improve unit test coverage to minimum ninety percent    ${proj_id}    ${token}    type=${TYPE_TASK}    priority=${PRIORITY_MEDIUM}
    ${i8_id}=    Get From Dictionary    ${i8.json()}    id
    ${i9}=    Create Issue    Write API documentation for all public endpoints    ${proj_id}    ${token}    type=${TYPE_TASK}    priority=${PRIORITY_LOW}
    ${i9_id}=    Get From Dictionary    ${i9.json()}    id
    ${i10}=    Create Issue    Clean up unused feature flags in configuration    ${proj_id}    ${token}    type=${TYPE_TASK}    priority=${PRIORITY_LOW}
    ${i10_id}=    Get From Dictionary    ${i10.json()}    id

    # Triage: comment on critical and high priority issues
    Create Comment    ${i1_id}    CRITICAL: Auth service down, investigating JWT token validation failure    ${token}
    Create Comment    ${i1_id}    Root cause: expired signing key not rotated on schedule    ${token}
    Create Comment    ${i1_id}    Fix deployed: new signing key active, all tokens validated    ${token}
    Create Comment    ${i2_id}    Metrics endpoint returning cached stale data from previous day    ${token}
    Create Comment    ${i2_id}    Cache invalidation logic updated, metrics now refresh correctly    ${token}
    Create Comment    ${i3_id}    Missing index on foreign key column causing full table scans    ${token}
    Create Comment    ${i3_id}    Index added in migration, query time reduced from 4s to 50ms    ${token}

    # Start working on critical items
    Update Issue    ${i1_id}    ${token}    status=${STATUS_IN_PROGRESS}
    Update Issue    ${i2_id}    ${token}    status=${STATUS_IN_PROGRESS}
    Update Issue    ${i3_id}    ${token}    status=${STATUS_IN_PROGRESS}
    Update Issue    ${i4_id}    ${token}    status=${STATUS_IN_PROGRESS}

    # Resolve critical bugs
    Update Issue    ${i1_id}    ${token}    status=${STATUS_RESOLVED}
    Update Issue    ${i2_id}    ${token}    status=${STATUS_RESOLVED}
    Update Issue    ${i3_id}    ${token}    status=${STATUS_RESOLVED}

    # Continue with features
    Create Comment    ${i4_id}    WebSocket server implemented, client integration in progress    ${token}
    Create Comment    ${i5_id}    Elasticsearch integration planned for full-text search capability    ${token}
    Update Issue    ${i5_id}    ${token}    status=${STATUS_IN_PROGRESS}
    Update Issue    ${i7_id}    ${token}    status=${STATUS_IN_PROGRESS}
    Update Issue    ${i8_id}    ${token}    status=${STATUS_IN_PROGRESS}

    # Resolve completed items
    Update Issue    ${i4_id}    ${token}    status=${STATUS_RESOLVED}
    Update Issue    ${i7_id}    ${token}    status=${STATUS_RESOLVED}

    # Verify full issue list
    ${all_issues}=    Get All Issues    ${token}
    Response Status Should Be    ${all_issues}    200

    # Close resolved critical bugs
    Update Issue    ${i1_id}    ${token}    status=${STATUS_CLOSED}
    Update Issue    ${i2_id}    ${token}    status=${STATUS_CLOSED}
    Update Issue    ${i3_id}    ${token}    status=${STATUS_CLOSED}

    # Cleanup tags
    ${tag1_id}=    Get From Dictionary    ${tag1.json()}    id
    ${tag2_id}=    Get From Dictionary    ${tag2.json()}    id
    ${tag3_id}=    Get From Dictionary    ${tag3.json()}    id
    Delete Tag    ${tag1_id}    ${token}
    Delete Tag    ${tag2_id}    ${token}
    Delete Tag    ${tag3_id}    ${token}
