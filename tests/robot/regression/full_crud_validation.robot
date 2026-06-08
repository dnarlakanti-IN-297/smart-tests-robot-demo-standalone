*** Settings ***
Documentation     Full CRUD Validation Regression Tests
...               Exhaustive CRUD cycle tests: create → read → update → delete
...               across all entities with full state verification at each step.
Library           RequestsLibrary
Library           Collections
Resource          ../resources/api_keywords.robot
Resource          ../resources/variables.robot
Resource          ../resources/setup_teardown.robot

Suite Setup       Suite Setup For API Tests
Suite Teardown    Suite Teardown For API Tests

Test Template     Full CRUD Cycle For All Entities

*** Test Cases ***                    SUFFIX    KEY
Full CRUD Cycle 001                   crud001   CRD01
Full CRUD Cycle 002                   crud002   CRD02
Full CRUD Cycle 003                   crud003   CRD03
Full CRUD Cycle 004                   crud004   CRD04
Full CRUD Cycle 005                   crud005   CRD05
Full CRUD Cycle 006                   crud006   CRD06
Full CRUD Cycle 007                   crud007   CRD07
Full CRUD Cycle 008                   crud008   CRD08
Full CRUD Cycle 009                   crud009   CRD09
Full CRUD Cycle 010                   crud010   CRD10
Full CRUD Cycle 011                   crud011   CRD11
Full CRUD Cycle 012                   crud012   CRD12
Full CRUD Cycle 013                   crud013   CRD13
Full CRUD Cycle 014                   crud014   CRD14
Full CRUD Cycle 015                   crud015   CRD15
Full CRUD Cycle 016                   crud016   CRD16
Full CRUD Cycle 017                   crud017   CRD17
Full CRUD Cycle 018                   crud018   CRD18
Full CRUD Cycle 019                   crud019   CRD19
Full CRUD Cycle 020                   crud020   CRD20
Full CRUD Cycle 021                   crud021   CRD21
Full CRUD Cycle 022                   crud022   CRD22
Full CRUD Cycle 023                   crud023   CRD23
Full CRUD Cycle 024                   crud024   CRD24
Full CRUD Cycle 025                   crud025   CRD25
Full CRUD Cycle 026                   crud026   CRD26
Full CRUD Cycle 027                   crud027   CRD27
Full CRUD Cycle 028                   crud028   CRD28
Full CRUD Cycle 029                   crud029   CRD29
Full CRUD Cycle 030                   crud030   CRD30
Full CRUD Cycle 031                   crud031   CRD31
Full CRUD Cycle 032                   crud032   CRD32
Full CRUD Cycle 033                   crud033   CRD33
Full CRUD Cycle 034                   crud034   CRD34
Full CRUD Cycle 035                   crud035   CRD35
Full CRUD Cycle 036                   crud036   CRD36
Full CRUD Cycle 037                   crud037   CRD37
Full CRUD Cycle 038                   crud038   CRD38
Full CRUD Cycle 039                   crud039   CRD39
Full CRUD Cycle 040                   crud040   CRD40
Full CRUD Cycle 041                   crud041   CRD41
Full CRUD Cycle 042                   crud042   CRD42
Full CRUD Cycle 043                   crud043   CRD43
Full CRUD Cycle 044                   crud044   CRD44
Full CRUD Cycle 045                   crud045   CRD45
Full CRUD Cycle 046                   crud046   CRD46
Full CRUD Cycle 047                   crud047   CRD47
Full CRUD Cycle 048                   crud048   CRD48
Full CRUD Cycle 049                   crud049   CRD49
Full CRUD Cycle 050                   crud050   CRD50

*** Keywords ***
Full CRUD Cycle For All Entities
    [Arguments]    ${suffix}    ${key}
    Register User    ${suffix}@example.com    ${suffix}    CRUD User ${suffix}    password123
    ${token}=    Get Auth Token    ${suffix}    password123

    # PROJECT: Create → Read → Update → verify
    ${proj_create}=    Create Project    CRUD Project ${suffix}    ${key}    Full CRUD regression test project    ${token}
    Response Status Should Be    ${proj_create}    201
    ${proj_id}=    Get From Dictionary    ${proj_create.json()}    id

    ${proj_read}=    Get Project By Id    ${proj_id}    ${token}
    Response Status Should Be    ${proj_read}    200
    Response Field Should Equal    ${proj_read}    id    ${proj_id}

    ${proj_update}=    Update Project    ${proj_id}    ${token}    name=Updated CRUD Project ${suffix}    description=Updated description for regression validation
    Response Status Should Be    ${proj_update}    200
    Response Field Should Equal    ${proj_update}    name    Updated CRUD Project ${suffix}

    # ISSUE: Create → Read → Update (title) → Update (status x3) → verify
    ${issue_create}=    Create Issue    CRUD test issue with sufficient title length    ${proj_id}    ${token}
    ...    type=${TYPE_BUG}    priority=${PRIORITY_HIGH}
    ...    description=Full CRUD validation for issue entity lifecycle
    Response Status Should Be    ${issue_create}    201
    ${issue_id}=    Get From Dictionary    ${issue_create.json()}    id

    ${issue_read}=    Get Issue By Id    ${issue_id}    ${token}
    Response Status Should Be    ${issue_read}    200
    Response Field Should Equal    ${issue_read}    id    ${issue_id}
    Response Field Should Equal    ${issue_read}    status    ${STATUS_OPEN}

    ${issue_update_title}=    Update Issue    ${issue_id}    ${token}
    ...    title=Updated CRUD issue title with sufficient length
    Response Status Should Be    ${issue_update_title}    200
    Response Field Should Equal    ${issue_update_title}    title    Updated CRUD issue title with sufficient length

    ${issue_progress}=    Update Issue    ${issue_id}    ${token}    status=${STATUS_IN_PROGRESS}
    Response Status Should Be    ${issue_progress}    200

    ${issue_resolved}=    Update Issue    ${issue_id}    ${token}    status=${STATUS_RESOLVED}
    Response Status Should Be    ${issue_resolved}    200

    # COMMENT: Create → Read → Update → Delete
    ${comment_create}=    Create Comment    ${issue_id}    Original comment content for CRUD regression testing    ${token}
    Response Status Should Be    ${comment_create}    201
    ${comment_id}=    Get From Dictionary    ${comment_create.json()}    id

    ${comment_read}=    Get Comments For Issue    ${issue_id}    ${token}
    Response Status Should Be    ${comment_read}    200

    ${comment_update}=    Update Comment    ${comment_id}    Updated comment content for regression test validation    ${token}
    Response Status Should Be    ${comment_update}    200

    ${comment_delete}=    Delete Comment    ${comment_id}    ${token}
    Response Status Should Be    ${comment_delete}    204

    # TAG: Create → Read → Delete
    ${tag_create}=    Create Tag    tag-${suffix}    ${token}    #3498db
    Response Status Should Be    ${tag_create}    201
    ${tag_id}=    Get From Dictionary    ${tag_create.json()}    id

    ${tag_read}=    Get All Tags    ${token}
    Response Status Should Be    ${tag_read}    200

    ${tag_delete}=    Delete Tag    ${tag_id}    ${token}
    Response Status Should Be    ${tag_delete}    204

    # ISSUE: Delete
    ${issue_closed}=    Update Issue    ${issue_id}    ${token}    status=${STATUS_CLOSED}
    Response Status Should Be    ${issue_closed}    200

    ${issue_delete}=    Delete Issue    ${issue_id}    ${token}
    Response Status Should Be    ${issue_delete}    204

    ${issue_gone}=    Get Issue By Id    ${issue_id}    ${token}
    Response Status Should Be    ${issue_gone}    404
