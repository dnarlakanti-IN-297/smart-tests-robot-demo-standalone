*** Settings ***
Documentation     Boundary Condition Regression Tests
...               Tests API boundaries: min/max field lengths, invalid inputs,
...               authorization boundaries, and error response validation.
Library           RequestsLibrary
Library           Collections
Resource          ../resources/api_keywords.robot
Resource          ../resources/variables.robot
Resource          ../resources/setup_teardown.robot

Suite Setup       Suite Setup For API Tests
Suite Teardown    Suite Teardown For API Tests

Test Template     Validate API Boundary Conditions

*** Test Cases ***                    SUFFIX    KEY
Boundary Test 001                     bnd001    BND01
Boundary Test 002                     bnd002    BND02
Boundary Test 003                     bnd003    BND03
Boundary Test 004                     bnd004    BND04
Boundary Test 005                     bnd005    BND05
Boundary Test 006                     bnd006    BND06
Boundary Test 007                     bnd007    BND07
Boundary Test 008                     bnd008    BND08
Boundary Test 009                     bnd009    BND09
Boundary Test 010                     bnd010    BND10
Boundary Test 011                     bnd011    BND11
Boundary Test 012                     bnd012    BND12
Boundary Test 013                     bnd013    BND13
Boundary Test 014                     bnd014    BND14
Boundary Test 015                     bnd015    BND15
Boundary Test 016                     bnd016    BND16
Boundary Test 017                     bnd017    BND17
Boundary Test 018                     bnd018    BND18
Boundary Test 019                     bnd019    BND19
Boundary Test 020                     bnd020    BND20
Boundary Test 021                     bnd021    BND21
Boundary Test 022                     bnd022    BND22
Boundary Test 023                     bnd023    BND23
Boundary Test 024                     bnd024    BND24
Boundary Test 025                     bnd025    BND25
Boundary Test 026                     bnd026    BND26
Boundary Test 027                     bnd027    BND27
Boundary Test 028                     bnd028    BND28
Boundary Test 029                     bnd029    BND29
Boundary Test 030                     bnd030    BND30
Boundary Test 031                     bnd031    BND31
Boundary Test 032                     bnd032    BND32
Boundary Test 033                     bnd033    BND33
Boundary Test 034                     bnd034    BND34
Boundary Test 035                     bnd035    BND35
Boundary Test 036                     bnd036    BND36
Boundary Test 037                     bnd037    BND37
Boundary Test 038                     bnd038    BND38
Boundary Test 039                     bnd039    BND39
Boundary Test 040                     bnd040    BND40
Boundary Test 041                     bnd041    BND41
Boundary Test 042                     bnd042    BND42
Boundary Test 043                     bnd043    BND43
Boundary Test 044                     bnd044    BND44
Boundary Test 045                     bnd045    BND45
Boundary Test 046                     bnd046    BND46
Boundary Test 047                     bnd047    BND47
Boundary Test 048                     bnd048    BND48
Boundary Test 049                     bnd049    BND49
Boundary Test 050                     bnd050    BND50

*** Keywords ***
Validate API Boundary Conditions
    [Arguments]    ${suffix}    ${key}
    Register User    ${suffix}@example.com    ${suffix}    Boundary ${suffix}    password123
    ${token}=    Get Auth Token    ${suffix}    password123
    ${proj}=    Create Project    Boundary Project ${suffix}    ${key}    Boundary condition test project    ${token}
    Response Status Should Be    ${proj}    201
    ${proj_id}=    Get From Dictionary    ${proj.json()}    id

    # Boundary: issue title too short (< 20 chars) must fail
    ${short_title}=    Create Issue    Short title    ${proj_id}    ${token}
    Should Be True    ${short_title.status_code} in [400, 422]

    # Boundary: valid minimum-length title (exactly 20 chars) must succeed
    ${min_title}=    Create Issue    Exactly twenty chars!    ${proj_id}    ${token}
    Response Status Should Be    ${min_title}    201
    ${issue_id}=    Get From Dictionary    ${min_title.json()}    id

    # Boundary: get non-existent issue
    ${not_found}=    Get Issue By Id    99999999    ${token}
    Response Status Should Be    ${not_found}    404

    # Boundary: unauthorized access - another user cannot update this issue
    Register User    other-${suffix}@example.com    oth${suffix}    Other ${suffix}    password123
    ${other_token}=    Get Auth Token    oth${suffix}    password123
    ${unauthorized_update}=    Update Issue    ${issue_id}    ${other_token}    title=Unauthorized update attempt title here
    Should Be True    ${unauthorized_update.status_code} in [403, 404]

    # Boundary: unauthorized delete
    ${unauthorized_delete}=    Delete Issue    ${issue_id}    ${other_token}
    Should Be True    ${unauthorized_delete.status_code} in [403, 404]

    # Boundary: original owner can update
    ${auth_update}=    Update Issue    ${issue_id}    ${token}    title=Authorized update with sufficient title length
    Response Status Should Be    ${auth_update}    200

    # Boundary: create issue in non-existent project
    ${bad_project}=    Create Issue    Issue for non existent project title    99999999    ${token}
    Should Be True    ${bad_project.status_code} in [400, 403, 404, 422]

    # Boundary: comment too short
    ${short_comment}=    Create Comment    ${issue_id}    Hi    ${token}
    Should Be True    ${short_comment.status_code} in [400, 422]

    # Boundary: valid comment
    ${valid_comment}=    Create Comment    ${issue_id}    This is a valid comment with sufficient length for the system    ${token}
    Response Status Should Be    ${valid_comment}    201
    ${comment_id}=    Get From Dictionary    ${valid_comment.json()}    id

    # Boundary: tag duplicate name
    ${tag1}=    Create Tag    ${suffix}-unique-tag    ${token}
    Response Status Should Be    ${tag1}    201
    ${dup_tag}=    Create Tag    ${suffix}-unique-tag    ${token}
    Should Be True    ${dup_tag.status_code} in [400, 409, 422]

    # Cleanup
    Delete Comment    ${comment_id}    ${token}
    ${tag_id}=    Get From Dictionary    ${tag1.json()}    id
    Delete Tag    ${tag_id}    ${token}
