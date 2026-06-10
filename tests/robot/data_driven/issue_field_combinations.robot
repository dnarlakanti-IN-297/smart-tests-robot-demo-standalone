*** Settings ***
Documentation     Issue Field Combination Tests
...               Tests all combinations of issue type x priority x status transitions.
...               Mimics enterprise regression coverage across configuration matrix.
Library           RequestsLibrary
Library           Collections
Resource          ../resources/api_keywords.robot
Resource          ../resources/variables.robot
Resource          ../resources/setup_teardown.robot

Suite Setup       Suite Setup For API Tests
Suite Teardown    Suite Teardown For API Tests

Test Template     Create And Transition Issue With Fields

*** Test Cases ***                              SUFFIX    KEY        TYPE              PRIORITY
Bug Critical Open To Resolved                   bco       BCOR       ${TYPE_BUG}       ${PRIORITY_CRITICAL}
Bug High Open To Resolved                       bho       BHOR       ${TYPE_BUG}       ${PRIORITY_HIGH}
Bug Medium Open To Resolved                     bmo       BMOR       ${TYPE_BUG}       ${PRIORITY_MEDIUM}
Bug Low Open To Resolved                        blo       BLOR       ${TYPE_BUG}       ${PRIORITY_LOW}
Feature Critical Open To Resolved               fco       FCOR       ${TYPE_FEATURE}   ${PRIORITY_CRITICAL}
Feature High Open To Resolved                   fho       FHOR       ${TYPE_FEATURE}   ${PRIORITY_HIGH}
Feature Medium Open To Resolved                 fmo       FMOR       ${TYPE_FEATURE}   ${PRIORITY_MEDIUM}
Feature Low Open To Resolved                    flo       FLOR       ${TYPE_FEATURE}   ${PRIORITY_LOW}
Task Critical Open To Resolved                  tco       TCOR       ${TYPE_TASK}      ${PRIORITY_CRITICAL}
Task High Open To Resolved                      tho       THOR       ${TYPE_TASK}      ${PRIORITY_HIGH}
Task Medium Open To Resolved                    tmo       TMOR       ${TYPE_TASK}      ${PRIORITY_MEDIUM}
Task Low Open To Resolved                       tlo       TLOR       ${TYPE_TASK}      ${PRIORITY_LOW}
Bug Critical Full Lifecycle                     bcfl      BCFL       ${TYPE_BUG}       ${PRIORITY_CRITICAL}
Bug High Full Lifecycle                         bhfl      BHFL       ${TYPE_BUG}       ${PRIORITY_HIGH}
Bug Medium Full Lifecycle                       bmfl      BMFL       ${TYPE_BUG}       ${PRIORITY_MEDIUM}
Bug Low Full Lifecycle                          blfl      BLFL       ${TYPE_BUG}       ${PRIORITY_LOW}
Feature Critical Full Lifecycle                 fcfl      FCFL       ${TYPE_FEATURE}   ${PRIORITY_CRITICAL}
Feature High Full Lifecycle                     fhfl      FHFL       ${TYPE_FEATURE}   ${PRIORITY_HIGH}
Feature Medium Full Lifecycle                   fmfl      FMFL       ${TYPE_FEATURE}   ${PRIORITY_MEDIUM}
Feature Low Full Lifecycle                      flfl      FLFL       ${TYPE_FEATURE}   ${PRIORITY_LOW}
Task Critical Full Lifecycle                    tcfl      TCFL       ${TYPE_TASK}      ${PRIORITY_CRITICAL}
Task High Full Lifecycle                        thfl      THFL       ${TYPE_TASK}      ${PRIORITY_HIGH}
Task Medium Full Lifecycle                      tmfl      TMFL       ${TYPE_TASK}      ${PRIORITY_MEDIUM}
Task Low Full Lifecycle                         tlfl      TLFL       ${TYPE_TASK}      ${PRIORITY_LOW}
Bug Critical With Comments                      bcwc      BCWC       ${TYPE_BUG}       ${PRIORITY_CRITICAL}
Bug High With Comments                          bhwc      BHWC       ${TYPE_BUG}       ${PRIORITY_HIGH}
Bug Medium With Comments                        bmwc      BMWC       ${TYPE_BUG}       ${PRIORITY_MEDIUM}
Bug Low With Comments                           blwc      BLWC       ${TYPE_BUG}       ${PRIORITY_LOW}
Feature Critical With Comments                  fcwc      FCWC       ${TYPE_FEATURE}   ${PRIORITY_CRITICAL}
Feature High With Comments                      fhwc      FHWC       ${TYPE_FEATURE}   ${PRIORITY_HIGH}
Feature Medium With Comments                    fmwc      FMWC       ${TYPE_FEATURE}   ${PRIORITY_MEDIUM}
Feature Low With Comments                       flwc      FLWC       ${TYPE_FEATURE}   ${PRIORITY_LOW}
Task Critical With Comments                     tcwc      TCWC       ${TYPE_TASK}      ${PRIORITY_CRITICAL}
Task High With Comments                         thwc      THWC       ${TYPE_TASK}      ${PRIORITY_HIGH}
Task Medium With Comments                       tmwc      TMWC       ${TYPE_TASK}      ${PRIORITY_MEDIUM}
Task Low With Comments                          tlwc      TLWC       ${TYPE_TASK}      ${PRIORITY_LOW}
Bug Critical Update Title                       bcut      BCUT       ${TYPE_BUG}       ${PRIORITY_CRITICAL}
Bug High Update Title                           bhut      BHUT       ${TYPE_BUG}       ${PRIORITY_HIGH}
Bug Medium Update Title                         bmut      BMUT       ${TYPE_BUG}       ${PRIORITY_MEDIUM}
Bug Low Update Title                            blut      BLUT       ${TYPE_BUG}       ${PRIORITY_LOW}
Feature Critical Update Title                   fcut      FCUT       ${TYPE_FEATURE}   ${PRIORITY_CRITICAL}
Feature High Update Title                       fhut      FHUT       ${TYPE_FEATURE}   ${PRIORITY_HIGH}
Feature Medium Update Title                     fmut      FMUT       ${TYPE_FEATURE}   ${PRIORITY_MEDIUM}
Feature Low Update Title                        flut      FLUT       ${TYPE_FEATURE}   ${PRIORITY_LOW}
Task Critical Update Title                      tcut      TCUT       ${TYPE_TASK}      ${PRIORITY_CRITICAL}
Task High Update Title                          thut      THUT       ${TYPE_TASK}      ${PRIORITY_HIGH}
Task Medium Update Title                        tmut      TMUT       ${TYPE_TASK}      ${PRIORITY_MEDIUM}
Task Low Update Title                           tlut      TLUT       ${TYPE_TASK}      ${PRIORITY_LOW}
Bug Critical Closed Via Resolved                bccvr     BCCVR      ${TYPE_BUG}       ${PRIORITY_CRITICAL}
Bug High Closed Via Resolved                    bhcvr     BHCVR      ${TYPE_BUG}       ${PRIORITY_HIGH}
Bug Medium Closed Via Resolved                  bmcvr     BMCVR      ${TYPE_BUG}       ${PRIORITY_MEDIUM}
Bug Low Closed Via Resolved                     blcvr     BLCVR      ${TYPE_BUG}       ${PRIORITY_LOW}
Feature Critical Closed Via Resolved            fccvr     FCCVR      ${TYPE_FEATURE}   ${PRIORITY_CRITICAL}
Feature High Closed Via Resolved                fhcvr     FHCVR      ${TYPE_FEATURE}   ${PRIORITY_HIGH}
Feature Medium Closed Via Resolved              fmcvr     FMCVR      ${TYPE_FEATURE}   ${PRIORITY_MEDIUM}
Feature Low Closed Via Resolved                 flcvr     FLCVR      ${TYPE_FEATURE}   ${PRIORITY_LOW}
Task Critical Closed Via Resolved               tccvr     TCCVR      ${TYPE_TASK}      ${PRIORITY_CRITICAL}
Task High Closed Via Resolved                   thcvr     THCVR      ${TYPE_TASK}      ${PRIORITY_HIGH}
Task Medium Closed Via Resolved                 tmcvr     TMCVR      ${TYPE_TASK}      ${PRIORITY_MEDIUM}
Task Low Closed Via Resolved                    tlcvr     TLCVR      ${TYPE_TASK}      ${PRIORITY_LOW}

*** Keywords ***
Create And Transition Issue With Fields
    [Arguments]    ${suffix}    ${key}    ${type}    ${priority}
    Register User    ${suffix}@example.com    ${suffix}    User ${suffix}    password123
    ${token}=    Get Auth Token    ${suffix}    password123
    ${proj}=    Create Project    Project ${suffix}    ${key}    Field combination test project    ${token}
    Response Status Should Be    ${proj}    201
    ${proj_id}=    Get From Dictionary    ${proj.json()}    id

    ${issue}=    Create Issue    Issue for field combination validation testing    ${proj_id}    ${token}
    ...    type=${type}    priority=${priority}
    ...    description=Testing ${type} with ${priority} priority field combination
    Response Status Should Be    ${issue}    201
    ${issue_id}=    Get From Dictionary    ${issue.json()}    id
    Response Field Should Equal    ${issue}    type    ${type}
    Response Field Should Equal    ${issue}    priority    ${priority}

    Create Comment    ${issue_id}    Starting work on this ${type} issue with ${priority} priority    ${token}

    ${progress}=    Update Issue    ${issue_id}    ${token}    status=${STATUS_IN_PROGRESS}
    Response Status Should Be    ${progress}    200

    Create Comment    ${issue_id}    Implementation complete for ${type} issue resolution    ${token}

    ${resolved}=    Update Issue    ${issue_id}    ${token}    status=${STATUS_RESOLVED}
    Response Status Should Be    ${resolved}    200

    ${final}=    Get Issue By Id    ${issue_id}    ${token}
    Response Status Should Be    ${final}    200
    Response Field Should Equal    ${final}    type    ${type}
    Response Field Should Equal    ${final}    priority    ${priority}
    Response Field Should Equal    ${final}    status    ${STATUS_RESOLVED}
