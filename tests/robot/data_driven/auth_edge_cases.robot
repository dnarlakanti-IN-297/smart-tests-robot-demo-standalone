*** Settings ***
Documentation     Authentication Edge Case Tests
...               Data-driven tests covering registration, login, and token validation
...               edge cases across many user variations.
Library           RequestsLibrary
Library           Collections
Library           String
Resource          ../resources/api_keywords.robot
Resource          ../resources/variables.robot
Resource          ../resources/setup_teardown.robot

Suite Setup       Suite Setup For API Tests
Suite Teardown    Suite Teardown For API Tests

Test Template     Register Login And Access Protected Resources

*** Test Cases ***                              SUFFIX
Auth Edge Case User 001                         aec001
Auth Edge Case User 002                         aec002
Auth Edge Case User 003                         aec003
Auth Edge Case User 004                         aec004
Auth Edge Case User 005                         aec005
Auth Edge Case User 006                         aec006
Auth Edge Case User 007                         aec007
Auth Edge Case User 008                         aec008
Auth Edge Case User 009                         aec009
Auth Edge Case User 010                         aec010
Auth Edge Case User 011                         aec011
Auth Edge Case User 012                         aec012
Auth Edge Case User 013                         aec013
Auth Edge Case User 014                         aec014
Auth Edge Case User 015                         aec015
Auth Edge Case User 016                         aec016
Auth Edge Case User 017                         aec017
Auth Edge Case User 018                         aec018
Auth Edge Case User 019                         aec019
Auth Edge Case User 020                         aec020
Auth Edge Case User 021                         aec021
Auth Edge Case User 022                         aec022
Auth Edge Case User 023                         aec023
Auth Edge Case User 024                         aec024
Auth Edge Case User 025                         aec025
Auth Edge Case User 026                         aec026
Auth Edge Case User 027                         aec027
Auth Edge Case User 028                         aec028
Auth Edge Case User 029                         aec029
Auth Edge Case User 030                         aec030
Auth Edge Case User 031                         aec031
Auth Edge Case User 032                         aec032
Auth Edge Case User 033                         aec033
Auth Edge Case User 034                         aec034
Auth Edge Case User 035                         aec035
Auth Edge Case User 036                         aec036
Auth Edge Case User 037                         aec037
Auth Edge Case User 038                         aec038
Auth Edge Case User 039                         aec039
Auth Edge Case User 040                         aec040

*** Keywords ***
Register Login And Access Protected Resources
    [Arguments]    ${suffix}
    # Register new user
    ${reg}=    Register User    ${suffix}@example.com    ${suffix}    User ${suffix}    password123
    Should Be True    ${reg.status_code} in [200, 201]

    # Login
    ${token}=    Get Auth Token    ${suffix}    password123

    # Access protected endpoint - current user profile
    ${me}=    Get Current User    ${token}
    Response Status Should Be    ${me}    200
    Response Should Contain Key    ${me}    username
    Response Field Should Equal    ${me}    username    ${suffix}

    # Create a project to confirm full auth access
    ${proj_key}=    Convert To Upper Case    ${suffix}
    ${proj}=    Create Project    Auth Project ${suffix}    ${proj_key}    Auth edge case project for testing authentication and authorization validation flows    ${token}
    Response Status Should Be    ${proj}    201

    # Access projects list
    ${projects}=    Get All Projects    ${token}
    Response Status Should Be    ${projects}    200

    # Verify duplicate registration is rejected
    ${dup}=    Register User    ${suffix}@example.com    ${suffix}    User ${suffix}    password123
    Should Be True    ${dup.status_code} in [400, 409, 422]

    # Verify wrong password fails
    ${bad_login}=    Login User    ${suffix}    wrongpassword
    Should Be True    ${bad_login.status_code} in [400, 401, 422]
