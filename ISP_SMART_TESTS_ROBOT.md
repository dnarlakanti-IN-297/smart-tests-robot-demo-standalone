# Smart Tests with Robot Framework

| | |
|---|---|
| **Author(s)** | PS Team (Anudeep) |
| **Team** | PS |
| **Date** | 2026-06-10 |
| **PS Official** | Pending |
| **ENG Approval** | Pending |

---

> **Important — CRITICAL REQUIREMENT**
>
> Smart Tests must be enabled for your CloudBees Unify organization before following this guide. An organization is enabled with **either PTSv1 or PTSv2 — not both simultaneously.** Which version your org has determines the prediction engine, not the CLI.
>
> - **PTSv1 (ML-based):** Uses a machine learning model trained on your historical test run data. Requires 3-5 observation runs before predictions appear.
> - **PTSv2 (AI-based):** Uses OpenAI to predict affected tests from the first run. No warm-up required.
>
> The `smart-tests-cli` is the same for both versions. The token you create in CloudBees Unify determines which prediction engine runs — a PTSv1 token connects to the ML model; a PTSv2 token connects to OpenAI.
>
> **To enable Smart Tests for your org/suborg:** Contact your CloudBees account team and provide your org/suborg ID.
>
> **Finding your org/suborg ID:**
> 1. Log in to cloudbees.io
> 2. Navigate to Admin Settings > Organization Profile
> 3. Copy your Organization ID
>
> **Important note about sub-organizations:** Smart Tests must be enabled separately for each suborg where you intend to use it. Enabling it on a parent organization does not automatically enable it for child sub-organizations.

---

## PTSv1 vs PTSv2: Key Differences

| | PTSv1 (ML-based) | PTSv2 (AI-based) |
|---|---|---|
| **Prediction engine** | Machine learning model trained on your historical runs | OpenAI — analyzes code changes directly |
| **CLI package** | `smart-tests-cli==2.11.2` | `smart-tests-cli==2.11.2` |
| **Token connects to** | CloudBees ML prediction service | OpenAI via CloudBees |
| **Warm-up required** | Yes — 3-5 runs before predictions appear | No — predictions available from first run |
| **Session reference syntax** | `@session.txt` | `@session.txt` |
| **Dry-run flag** | `--outputdir <dir>` | `--outputdir <dir>` |
| **`record commit` step** | Required (same CLI) | Required |
| **Workflow commands** | Identical to PTSv2 | Identical to PTSv1 |
| **Demo branch** | `patch-robot-demo-ptsv1` | `patch-robot-demo-ptsv2` |
| **Demo workflow file** | `tests-robot-smarttests-pts-v1.yml` | `tests-robot-smarttests-pts-v2.yml` |

> **Note — One CLI, two engines:** The `smart-tests-cli` commands, flags, and workflow structure are completely identical for PTSv1 and PTSv2. No separate CLI, no separate install. The token you configure is the only thing that changes — it routes the request to either the ML engine (PTSv1) or OpenAI (PTSv2).

---

## Qualification Criteria

Before proceeding with Smart Tests adoption, the customer must meet ALL of the following requirements. These apply to both PTSv1 and PTSv2.

### 1. Long-Running Test Suite

| Requirement | Details |
|---|---|
| **Minimum Runtime** | Full test suite must take 15+ minutes to execute |
| **Rationale** | Smart Tests provides the most value when test execution time is significant. Shorter test suites (<15 minutes) may not justify the implementation effort. |
| **How to Measure** | Review recent CI/CD pipeline execution times for test stages |

> **Tip — Ideal Candidates**
>
> - Test suites taking 30-60+ minutes: High value opportunity
> - Test suites taking 15-30 minutes: Good candidate
> - Test suites taking <15 minutes: Consider future growth or wait until suite grows

### 2. Independent Tests

| Requirement | Details |
|---|---|
| **Test Independence** | Tests must be independently executable without dependencies on test execution order |
| **Rationale** | Smart Tests creates subsets of tests to run. If tests depend on other tests running first (shared state, execution order), subsetting will cause failures. |
| **How to Validate** | Tests can be run in isolation or random order without affecting results |

> **Warning — Common Anti-Patterns That Disqualify**
>
> - Tests that rely on shared global state modified by other tests
> - Tests that must run in specific order (Test B depends on Test A's side effects)
> - Test suites using resource-level ordering mechanisms or global Suite Setup that modifies shared state
> - Setup/teardown logic that assumes all tests run together
>
> If these patterns exist, the customer must refactor tests before Smart Tests adoption.

### 3. Git Version Control

| Requirement | Details |
|---|---|
| **Version Control** | Must be using Git for source control |
| **Rationale** | Smart Tests analyzes code changes via `git diff` to predict affected tests. Git is the only supported VCS. |
| **Supported** | GitHub, GitLab, Bitbucket, Azure Repos, self-hosted Git servers |
| **Not Supported** | Subversion (SVN), Mercurial, Perforce, TFS (non-Git) |

### 4. Test File Organization

| Requirement | Details |
|---|---|
| **File Structure** | Tests must be organized across multiple `.robot` files, not a single monolithic file |
| **Rationale** | Smart Tests maps code changes to test files. A single file containing all tests prevents effective subsetting. |
| **Good Structure** | Tests organized by feature, module, layer, or functional area across multiple files |
| **Disqualifying Structure** | Single `all_tests.robot` file containing hundreds of tests |

> **Tip — Acceptable Robot Framework Organization Patterns**
>
> ```
> ✓ By feature:
>   tests/robot/auth/login_tests.robot
>   tests/robot/auth/permission_tests.robot
>   tests/robot/projects/project_crud_tests.robot
>
> ✓ By layer:
>   tests/robot/api/auth_api.robot
>   tests/robot/api/projects_api.robot
>   tests/robot/data_driven/auth_edge_cases.robot
>
> ✗ Disqualifying:
>   tests/robot/all_tests.robot (500 tests in one file)
> ```

### 5. Supported Test Framework

Robot Framework is an officially supported Smart Tests framework.

| Test Framework | `test_runner` Value | Additional Setup Required | Language/Ecosystem |
|---|---|---|---|
| pytest | `pytest` | No | Python |
| **Robot Framework** | **`robot`** | **No** | **Python (Keyword-driven)** |
| Playwright | `playwright` | No | JavaScript/TypeScript |
| Jest | `jest` | No | JavaScript/TypeScript |
| Maven | `maven` | No | Java |
| Gradle | `gradle` | No | Java/Kotlin |

### 6. CI/CD Platform Requirements

| Requirement | Details |
|---|---|
| **Python 3.7+** | Smart Tests CLI requires Python 3.7 or later on CI runners |
| **Java Runtime** | Java runtime environment required for CLI execution |
| **CLI Execution** | CI platform must allow running `smart-tests` CLI commands |
| **Environment Variables** | Must support setting secrets/environment variables (for Smart Tests API token) |

**PS-Tested CI/CD Platforms:**
- CloudBees Unify
- GitHub Actions
- CloudBees CI
- Jenkins

> **Tip — Validation Steps**
>
> To verify CI platform compatibility:
> 1. Check Python version: `python --version` (must be 3.7+)
> 2. Check Java availability: `java -version`
> 3. Test CLI installation: `pip install smart-tests-cli && smart-tests --version`
> 4. Verify network access to CloudBees API endpoints
>
> If all commands succeed, the platform is compatible.

---

## Overview

This guide teaches CloudBees Smart Tests predictive test selection using a Robot Framework application as the implementation pattern. The concepts and integration patterns apply to any project using Robot Framework for testing, regardless of whether your organization uses PTSv1 or PTSv2.

**Demonstration Repository:** https://github.com/cloudbees-ps/smart-tests-robot-demo

The repository includes three demo branches — full-suite and quick variants:

| Version | Branch | Workflow | Tests | Latency |
|---|---|---|---|---|
| PTSv2 (AI-based) | `patch-robot-demo-ptsv2` | `tests-robot-smarttests-pts-v2.yml` | 451 | 500ms simulated |
| PTSv1 (ML-based) | `patch-robot-demo-ptsv1` | `tests-robot-smarttests-pts-v1.yml` | 451 | 500ms simulated |
| PTSv1 quick | `patch-robot-demo-quick` | `tests-robot-smarttests-pts-v1-quick.yml` | 40 | 0ms |
| PTSv2 quick | `patch-robot-demo-quick` | `tests-robot-smarttests-pts-v2-quick.yml` | 40 | 0ms |

**Why the Demo Has Simulated Latency?** The demo application includes 500ms of simulated API latency per request, bringing the full 451-test suite to approximately 31 minutes. This simulates a realistic enterprise test suite.

### By the end of this guide, you will:

- Understand the difference between PTSv1 (ML-based) and PTSv2 (AI-based) prediction engines
- Know how to configure `smart-tests-cli` for either version using the appropriate token
- Understand observation mode, production mode, and when to use each
- Interpret the CloudBees Unify dashboard to track session status and subset accuracy
- Know the integration pattern and common pitfalls for Robot Framework with Smart Tests

**Target Audience:** Teams using Python and Robot Framework for testing

**Estimated Time:**
- PTSv2: 30-45 minutes (predictions from first run)
- PTSv1: 45-60 minutes plus 3-5 observation runs to warm up the model

---

## Prerequisites

### General Requirements (Any Customer)

| Requirement | Notes |
|---|---|
| **Python 3.7+** | Smart Tests CLI requires modern Python |
| **Robot Framework installed** | Any version ≥ 7.0 |
| **CI/CD pipeline** | GitHub Actions, Jenkins, GitLab CI, etc. |
| **Git repository** | For change detection |
| **CloudBees account** | Edition requirement has not been confirmed. Contact your CloudBees account team for licensing details. |
| **Smart Tests enabled** | PTSv1 or PTSv2 — contact CloudBees to enable the appropriate version for your org |

### Demo-Specific Requirements

| Requirement | Notes |
|---|---|
| **GitHub account** | To fork the demo repository |
| **GitHub Actions enabled** | Ability to run workflows in your fork |
| **Two CloudBees Unify workspaces** | One with PTSv1 enabled, one with PTSv2 enabled — required to run both versions of the demo. A single workspace is enabled for only one version at a time. |
| **Time commitment** | 30-60 minutes depending on version |

> **Note — Two workspaces required for the full demo:** PTSv1 and PTSv2 cannot be enabled on the same workspace simultaneously. To demonstrate both versions side by side, you need two separate workspaces (or two separate orgs/suborgs in CloudBees Unify), each enabled for the respective version. Create one API token per workspace and add both to GitHub secrets: `PTSv1_TOKEN` from the PTSv1-enabled workspace, `PTSv2_TOKEN` from the PTSv2-enabled workspace.
>
> If you only have one workspace (one version enabled), you can still follow this guide — just use the branch and workflow that match your enabled version.

### Parameterized Values

| Placeholder | Description | Where to Find |
|---|---|---|
| `<YOUR_PTSv1_TOKEN>` | CloudBees API token from your PTSv1-enabled workspace | CloudBees UI: Smart Tests > Settings > Create a Workspace API Key (on the PTSv1 workspace) |
| `<YOUR_PTSv2_TOKEN>` | CloudBees API token from your PTSv2-enabled workspace | CloudBees UI: Smart Tests > Settings > Create a Workspace API Key (on the PTSv2 workspace) |

---

## Implementation

### Initial Setup

#### Fork the Repository

1. Navigate to: https://github.com/cloudbees-ps/smart-tests-robot-demo
2. Click **Fork** button (top right)
3. Select your GitHub account
4. Uncheck **Copy the `main` branch only** — all demo branches must be included
5. Wait for fork to complete

**Result:** Personal copy of repository under your GitHub account with all demo branches (`patch-robot-demo-ptsv2`, `patch-robot-demo-ptsv1`, `patch-robot-demo-quick`)

#### Enable GitHub Actions

1. Go to your forked repository
2. Click **Actions** tab
3. If prompted, click "I understand my workflows, go ahead and enable them"

**Workflows Available:**
- **Robot Framework Tests (PTSv2):** PTSv2 full suite — `patch-robot-demo-ptsv2` branch (451 tests, 500ms latency)
- **Robot Framework Tests (PTSv1):** PTSv1 full suite — `patch-robot-demo-ptsv1` branch (451 tests, 500ms latency)
- **Robot Framework Tests (Quick - PTSv2):** PTSv2 fast demo — `patch-robot-demo-quick` branch (40 tests, 0ms)
- **Robot Framework Tests (Quick - PTSv1):** PTSv1 warm-up — `patch-robot-demo-quick` branch (40 tests, 0ms)
- **Robot Framework Tests (No Smart Tests - Baseline):** Full suite without Smart Tests, for comparison

#### Configure Smart Tests Token

**Obtain CloudBees API Token:**

1. Log in to https://cloudbees.io
2. Navigate to **Smart Tests > Settings**
3. Click **Create a Workspace API Key**
4. Enter a key name (e.g., `robot-demo-token`)
5. Copy the generated token

> **Note:** Store this token securely. You'll only see it once. The token type (PTSv1 or PTSv2) is determined by which version your org has enabled in CloudBees Unify.

**Add Token to GitHub:**

Add only the secret that matches the version your org has enabled — you need one secret, not both.

1. Go to your forked repository
2. Navigate to **Settings > Secrets and variables > Actions**
3. Click **New repository secret**
4. Configure based on your org's version:

| Your org version | Secret Name | Secret Value |
|---|---|---|
| PTSv2 | `PTSv2_TOKEN` | Token from your PTSv2-enabled org/workspace |
| PTSv1 | `PTSv1_TOKEN` | Token from your PTSv1-enabled org/workspace |

5. Click **Add secret**

> **Note:** Both `PTSv1_TOKEN` and `PTSv2_TOKEN` map to the `SMART_TESTS_TOKEN` environment variable inside the workflow — the CLI always reads `SMART_TESTS_TOKEN` at runtime. The separate secret names make it clear which token belongs to which engine.

**Verification:** Secret appears in repository secrets list

---

### Hands-On: Observing Smart Tests

> **Three modes — understand these before you start:**
>
> | Mode | Workflow | What runs | What you learn |
> |---|---|---|---|
> | **Baseline** | `tests-robot-no-smarttests.yml` | All tests, no Smart Tests | How long your full suite takes with no optimization — your "before" number |
> | **Observation** | Smart Tests workflow, `mode: observation` | All tests, Smart Tests records results | Unify shows how much time Smart Tests *would* save — savings are projected, not yet realized |
> | **Production** | Smart Tests workflow, `mode: production` | Only the predicted subset | Actual time savings are realized — this is the goal |
>
> Run them in this order: Baseline → Observation → Production.

**All five workflows at a glance:**

| Workflow (Actions sidebar name) | File | Branch to select | Tests | Purpose |
|---|---|---|---|---|
| Robot Framework Tests (No Smart Tests - Baseline) | `tests-robot-no-smarttests.yml` | `patch-robot-demo-ptsv2` or `patch-robot-demo-ptsv1` | 451 | Establish reference runtime |
| Robot Framework Tests (PTSv2) | `tests-robot-smarttests-pts-v2.yml` | `patch-robot-demo-ptsv2` | 451 | PTSv2 full demo — 1 observation run, then production |
| Robot Framework Tests (PTSv1) | `tests-robot-smarttests-pts-v1.yml` | `patch-robot-demo-ptsv1` | 451 | PTSv1 full demo — 5-6 observation runs, then production |
| Robot Framework Tests (Quick - PTSv2) | `tests-robot-smarttests-pts-v2-quick.yml` | `patch-robot-demo-quick` | 40 | Fast PTSv2 demo — predictions in ~1-2 minutes |
| Robot Framework Tests (Quick - PTSv1) | `tests-robot-smarttests-pts-v1-quick.yml` | `patch-robot-demo-quick` | 40 | PTSv1 warm-up / fast demo — ~1-2 minutes per run |

---

#### Step 1 — Establish Your Baseline

**Workflow:** `Robot Framework Tests (No Smart Tests - Baseline)` (`tests-robot-no-smarttests.yml`)

This workflow has no Smart Tests integration. It runs your entire test suite from start to finish with no optimization. The result — approximately 31 minutes — is your reference number. You will compare every Smart Tests run against this number to measure how much time is saved.

1. Navigate to the **Actions** tab in your forked repository
2. In the left sidebar, click **Robot Framework Tests (No Smart Tests - Baseline)**
3. Click **Run workflow** (top right of the workflow list)
4. In the dropdown, select the branch that matches the version you want to demo:
   - `patch-robot-demo-ptsv2` — if you are running the PTSv2 demo
   - `patch-robot-demo-ptsv1` — if you are running the PTSv1 demo
5. Click **Run workflow**

Wait approximately 31 minutes for the workflow to complete.

**What you get:** The full test suite runtime with no optimization. Note this number — every Smart Tests run you do on the same branch will be compared against it.

> **Note:** Run the baseline on the same full-suite branch you plan to use for your Smart Tests demo. The quick branch (`patch-robot-demo-quick`) has 0ms latency and only 40 tests — a baseline there is not a meaningful comparison for the full 451-test demo.

---

#### Step 2 — Run Smart Tests

Choose the scenario that matches your org's enabled version and how much time you have.

---

##### Scenario A: PTSv2 — Full Suite (451 tests, ~31 min baseline)

PTSv2 uses AI to predict affected tests. **Predictions are available from the very first run** — no warm-up needed. One observation run is all you need before switching to production.

**Workflow:** `Robot Framework Tests (PTSv2)` (`tests-robot-smarttests-pts-v2.yml`)
**Branch:** `patch-robot-demo-ptsv2`

**Run 1 — Observation mode:**

1. In the **Actions** sidebar, click **Robot Framework Tests (PTSv2)**
2. Click **Run workflow**
3. Set the following inputs:
   - **Branch:** `patch-robot-demo-ptsv2`
   - **mode:** `observation`
   - **target:** `--target 75%`
4. Click **Run workflow**

Wait ~31 minutes for completion.

**After the run — check CloudBees Unify (Smart Tests > Sessions):**
```
Session status    : Observation mode
Tests executed    : 451
Projected subset  : ~340 tests at 75% target
```
All 451 tests ran — this is observation mode, so nothing was skipped. But Unify is now showing you what Smart Tests *would have* run (about 340 tests) and the time you *would have* saved. These are projected savings. To realize the actual savings, run in production mode.

**Run 2 — Production mode (realize actual savings):**

1. Click **Robot Framework Tests (PTSv2)** > **Run workflow**
2. Set the following inputs:
   - **Branch:** `patch-robot-demo-ptsv2`
   - **mode:** `production`
   - **target:** `--target 75%`
3. Click **Run workflow**

Wait ~23 minutes.

**After the run:** Only ~340 tests ran instead of 451. Actual runtime dropped from ~31 minutes to ~23 minutes — 25% time saved.

---

##### Scenario B: PTSv1 — Full Suite (451 tests, ~31 min baseline)

PTSv1 uses a machine learning model that learns from your historical test run data. **The model needs 5-6 observation runs before it can generate predictions.** To avoid waiting 31 minutes per warm-up run, use the quick branch first (40 tests, ~1-2 min each) to build history, then switch to the full branch.

**Phase 1 — Warm up the ML model on the quick branch (5-6 runs)**

**Workflow:** `Robot Framework Tests (Quick - PTSv1)` (`tests-robot-smarttests-pts-v1-quick.yml`)
**Branch:** `patch-robot-demo-quick`

1. In the **Actions** sidebar, click **Robot Framework Tests (Quick - PTSv1)**
2. Click **Run workflow**
3. Set the following inputs:
   - **Branch:** `patch-robot-demo-quick`
   - **mode:** `observation`
   - **target:** `--target 75%`
4. Click **Run workflow** — completes in ~1-2 minutes
5. Make a small code change to generate a new commit diff (e.g., add a blank line to `app/main.py`), commit it, and push to `patch-robot-demo-quick`. This gives the model varied training data. Each push triggers the workflow automatically, or trigger it manually with **Run workflow**.
6. Repeat steps 2-5 a total of **5-6 times**

**What to check in Unify during the first 3-5 runs:**
```
Session status    : Observation mode
Tests executed    : 40
Subset            : (none — model building history)
Remainder         : (none)
```
"No subset requests" means the model is still collecting data. This is expected — keep running.

**What to check in Unify after 5-6 runs:**
```
Session status    : Session passed
Tests executed    : 40
Subset            : 30 testcases
Remainder         : 10 testcases
```
Subset and Remainder counts appearing means the ML model has enough history and is ready. Move to Phase 2.

> **Note:** The history built on `patch-robot-demo-quick` carries over to the full branch. You do not need to re-warm the model when you switch to `patch-robot-demo-ptsv1`.

**Phase 2 — Full suite observation run**

**Workflow:** `Robot Framework Tests (PTSv1)` (`tests-robot-smarttests-pts-v1.yml`)
**Branch:** `patch-robot-demo-ptsv1`

1. In the **Actions** sidebar, click **Robot Framework Tests (PTSv1)**
2. Click **Run workflow**
3. Set the following inputs:
   - **Branch:** `patch-robot-demo-ptsv1`
   - **mode:** `observation`
   - **target:** `--target 75%`
4. Click **Run workflow**

Wait ~31 minutes for completion.

**After the run — check Unify (Smart Tests > Sessions):**
```
Session status    : Observation mode
Tests executed    : 451
Projected subset  : ~340 tests at 75% target
```
All 451 tests ran. Unify now shows the projected subset and estimated savings. Savings are still projected — not yet realized.

**Phase 3 — Production run (realize actual savings)**

1. Click **Robot Framework Tests (PTSv1)** > **Run workflow**
2. Set the following inputs:
   - **Branch:** `patch-robot-demo-ptsv1`
   - **mode:** `production`
   - **target:** `--target 75%`
3. Click **Run workflow**

Wait ~23 minutes.

**After the run:** Only ~340 tests ran instead of 451. Actual runtime dropped from ~31 minutes to ~23 minutes — 25% time saved.

---

##### Scenario C: Quick Branch — Fast Demo (~1-2 minutes per run)

Use `patch-robot-demo-quick` when you want to demonstrate Smart Tests in under 2 minutes. Both PTSv1 and PTSv2 are available on this branch (40 tests, 0ms latency). Skip Step 1 — there is no meaningful full-suite baseline on this branch.

**PTSv2 Quick:**

**Workflow:** `Robot Framework Tests (Quick - PTSv2)` (`tests-robot-smarttests-pts-v2-quick.yml`)
**Branch:** `patch-robot-demo-quick`

1. In the **Actions** sidebar, click **Robot Framework Tests (Quick - PTSv2)**
2. Click **Run workflow**
3. Set the following inputs:
   - **Branch:** `patch-robot-demo-quick`
   - **mode:** `observation`
   - **target:** `--target 75%`
4. Click **Run workflow** — completes in ~1-2 minutes

**After the run — check Unify:**
```
Session status    : Observation mode
Tests executed    : 40
Projected subset  : ~30 tests at 75% target
```
PTSv2 predictions appear immediately. Now run in production to realize savings:

5. Click **Run workflow** again with **mode:** `production` and **branch:** `patch-robot-demo-quick`

Only ~30 of the 40 tests run. You have just demonstrated predictive test selection in under 2 minutes.

---

**PTSv1 Quick:**

**Workflow:** `Robot Framework Tests (Quick - PTSv1)` (`tests-robot-smarttests-pts-v1-quick.yml`)
**Branch:** `patch-robot-demo-quick`

Follow the same warm-up process described in Scenario B Phase 1 (5-6 observation runs with small commits). Once predictions appear in Unify:

1. Click **Run workflow** with **mode:** `production` and **branch:** `patch-robot-demo-quick`

Only ~30 of the 40 tests run.

> **Note:** If you have already completed the PTSv1 warm-up as part of Scenario B, the model is already trained — you can go straight to production mode here.

---

#### Step 3 — View Test Sessions in CloudBees Unify

After every run, open https://cloudbees.io and navigate to **Smart Tests > Sessions** to review the results.

| Field | What it means |
|---|---|
| **Session status** | `Observation mode` — all tests ran, savings are projected. `Session passed/failed` — production mode ran, savings are realized. |
| **Tests executed** | How many tests actually ran in this session |
| **Projected subset** | How many tests Smart Tests *would have* selected — visible in observation mode |
| **Subset** | How many tests Smart Tests actually selected to run — visible in production mode |
| **Remainder** | How many tests Smart Tests deferred (skipped) — visible in production mode |
| **Accuracy** | Did the subset catch all failing tests? Look for >90% |

> **The key distinction to explain to stakeholders:** In observation mode, Unify tells you how much time you *could* save. In production mode, that time is actually saved. The observation phase is where you validate predictions are accurate before committing to skipping tests.

---

#### Step 4 — Try Different Targets

Once you have run in production at least once, try changing the `target` parameter to see how it affects the subset size and savings:

**Full suite branches (`patch-robot-demo-ptsv2` / `patch-robot-demo-ptsv1`, 451 tests, ~31 min baseline):**

| Target | What it means | Tests run | Runtime | Savings |
|---|---|---|---|---|
| `--target 75%` | Run 75% of expected duration | ~340 | ~23 min | ~25% |
| `--target 70%` | Run 70% of expected duration | ~315 | ~21 min | ~32% |
| `--target 50%` | Run 50% of expected duration | ~225 | ~15 min | ~50% |
| `--target 30%` | Run 30% of expected duration | ~135 | ~9 min | ~70% — higher risk |

**Quick branch (`patch-robot-demo-quick`, 40 tests, ~1-2 min baseline):**

| Target | Tests run | Savings |
|---|---|---|
| `--target 75%` | ~30 tests | ~25% |
| `--target 50%` | ~20 tests | ~50% |
| `--target 30%` | ~12 tests | ~70% — higher risk |

> **Warning:** Lower targets skip more tests and save more time, but increase the chance of missing a failure. Start at `--target 75%` and only reduce after you have validated prediction accuracy across multiple sessions.

**Other target types (for reference):**

| Type | Example | When to use |
|---|---|---|
| `--target %` | `--target 75%` | Most flexible — used in this demo |
| `--confidence %` | `--confidence 90%` | When you want to target a specific probability of catching failures |
| `--time` | `--time 10m` | When you have a hard time constraint (e.g., "max 10 minutes") |

---

> **Note — What Smart Tests is doing behind the scenes during every run:**
>
> 1. **Record commit history:** `smart-tests record commit` pre-populates 90 days of git history so the prediction engine understands your codebase evolution
> 2. **Record build:** `smart-tests record build` registers this CI run in CloudBees
> 3. **Record session:** `smart-tests record session` creates a test session and writes the session ID to `session.txt` automatically via the `> session.txt` redirect. In observation mode, `--observation` flag is added.
> 4. **Dry-run test discovery:** `robot --dryrun --outputdir /tmp/robot-dryrun` enumerates all tests in scope (451 on full branches, 40 on quick) and writes the test list to `/tmp/robot-dryrun/output.xml`
> 5. **Generate subset:** `smart-tests subset robot --session @session.txt ... /tmp/robot-dryrun/output.xml` predicts which tests are relevant to the current code change and outputs Robot Framework CLI arguments
> 6. **Run tests:** In observation mode, all tests run regardless of the subset. In production mode, only the subset runs. Results are written to `test-results/output.xml` automatically by Robot Framework.
> 7. **Record results:** `smart-tests record tests robot --session @session.txt test-results/output.xml` uploads results to CloudBees. This step runs with `if: always()` — Smart Tests needs results from both passing and failing runs to improve accuracy.

---

## Understanding the CI Integration

All four Smart Tests workflows (`tests-robot-smarttests-pts-v2.yml`, `tests-robot-smarttests-pts-v1.yml`, `tests-robot-smarttests-pts-v2-quick.yml`, `tests-robot-smarttests-pts-v1-quick.yml`) follow the same seven-step pattern using `smart-tests-cli==2.11.2`. Open any file in the repository to see the complete integration.

### The Seven-Step Integration Pattern

| Step | Command | Purpose |
|---|---|---|
| 1 | `smart-tests record commit` | Pre-populates commit history for the prediction engine |
| 2 | `smart-tests record build` | Registers the build in CloudBees |
| 3 | `smart-tests record session` | Creates test session, writes session ID to `session.txt` |
| 4 | `robot --dryrun --outputdir /tmp/robot-dryrun` | Enumerates all available Robot Framework tests |
| 5 | `smart-tests subset robot --session @session.txt ... /tmp/robot-dryrun/output.xml` | Generates predicted test subset |
| 6 | `eval robot ... $SUBSET_CONTENT tests/robot/` | Runs tests (all in observation mode, subset in production) |
| 7 | `smart-tests record tests robot --session @session.txt test-results/output.xml` | Uploads results to CloudBees |

### Step-by-Step Breakdown

**1. Record Commits (`smart-tests record commit`)**

```bash
smart-tests record commit \
  --name ${{ github.repository }} \
  --source ${{ github.workspace }} \
  --max-days 90
```

Pre-populates 90 days of git history. Required for both PTSv1 and PTSv2 — without this, only the latest commit is available to the prediction engine.

**2. Record Build (`smart-tests record build`)**

```bash
smart-tests record build \
  --build ${{ github.run_id }} \
  --source ${{ github.workspace }}
```

Groups related test sessions together under this CI run.

**3. Record Session (`smart-tests record session`)**

```bash
smart-tests record session \
  --build ${{ github.run_id }} \
  $OBSERVATION_FLAG \
  --test-suite robot-api > session.txt
```

Creates a test session in CloudBees. The `$OBSERVATION_FLAG` is `--observation` in observation mode and a single space `' '` in production mode (GitHub Actions ternary requires a non-empty value). The session ID is written to `session.txt` automatically via the `> session.txt` redirect. All subsequent steps reference this file as `@session.txt`.

**4. Collect Tests (`robot --dryrun`)**

```bash
mkdir -p /tmp/robot-dryrun
robot --dryrun \
  --outputdir /tmp/robot-dryrun \
  tests/robot/ \
  2>/dev/null || true
```

Enumerates all available tests without executing them. Produces `/tmp/robot-dryrun/output.xml`, which is passed to the subset step.

**5. Generate Subset (`smart-tests subset robot`)**

```bash
smart-tests subset robot \
  --session @session.txt \
  $TARGET_FLAG \
  /tmp/robot-dryrun/output.xml \
  > smart-tests-subset.txt \
  2>/tmp/subset-status.txt

cat /tmp/subset-status.txt || true
```

Analyzes commits and returns Robot Framework CLI arguments for the predicted subset (e.g., `-s 'Auth Edge Cases' -t 'Auth Edge Case User 001'`). The full path to the dry-run XML must be passed — not a `.robot` source file.

**PTSv1:** On early runs, `smart-tests-subset.txt` is empty and status shows "No subset requests." The workflow falls back to all tests automatically.

**PTSv2:** Predictions are generated from the first run.

**6. Run Tests (`robot` with subset)**

```bash
SUBSET_CONTENT=$(cat smart-tests-subset.txt)

if [ -s smart-tests-subset.txt ] && [ "$SUBSET_CONTENT" != "ALL" ]; then
  eval robot \
    --outputdir test-results --output output.xml \
    --xunit junit.xml --loglevel INFO \
    $SUBSET_CONTENT \
    tests/robot/ || true
else
  robot \
    --outputdir test-results --output output.xml \
    --xunit junit.xml --loglevel INFO \
    tests/robot/ || true
fi
```

**7. Record Results (`smart-tests record tests`)**

```bash
smart-tests record tests robot \
  --session @session.txt \
  test-results/output.xml
```

Uploads test results to CloudBees. **This step must run with `if: always()`** — Smart Tests needs results from both passing and failing runs. For PTSv1, recording consistently in every run is what accelerates ML model accuracy.

### Why `eval` is Required

The `smart-tests subset robot` output contains Robot Framework CLI arguments with single-quoted test names:

```
-s 'Auth Edge Cases' -t 'Auth Edge Case User 001' -t 'Auth Edge Case User 002'
```

Without `eval`, the shell word-splits on spaces inside single quotes:

```bash
# WRONG — word-splits, breaks test names with spaces
robot $SUBSET_CONTENT tests/robot/

# CORRECT — eval preserves quoted tokens
eval robot $SUBSET_CONTENT tests/robot/
```

### Key Configuration Points

- **Token:** Add your token to GitHub secrets as `PTSv2_TOKEN` (PTSv2) or `PTSv1_TOKEN` (PTSv1). The workflow maps it to the `SMART_TESTS_TOKEN` environment variable, which is what the CLI reads at runtime.
- **Session reference:** Always use `@session.txt`. This is the Smart Tests CLI syntax for file references.
- **Dry-run XML:** Always pass the full path to the `--outputdir` output (`/tmp/robot-dryrun/output.xml`). Never pass `.robot` source files.
- **`eval`:** Always required when running Robot Framework with Smart Tests subset output.
- **`if: always()`:** Required on the record tests step.

> **Warning — COMMON MISCONCEPTIONS: Technical Integration**
>
> **Misconception #1:** "PTSv1 and PTSv2 need different CLI tools."
>
> **Reality:** `smart-tests-cli==2.11.2` handles both. Install once, use for either version. The token determines which prediction engine runs — not the CLI.
>
> **Misconception #2:** "No subset requests means something is broken."
>
> **Reality:** For PTSv1 this is expected on the first 3-5 runs. The ML model needs historical data. The workflow handles this by running all tests as a fallback. For PTSv2, if this appears beyond the first run, verify the token is a PTSv2 token and the workspace is enabled.
>
> **Misconception #3:** "I need to modify my Robot Framework tests to work with Smart Tests."
>
> **Reality:** Zero test code changes required. Smart Tests uses the standard `robot --dryrun` command and `output.xml` that Robot Framework already produces natively.
>
> **Misconception #4:** "I can pass the `.robot` source file to `smart-tests subset robot`."
>
> **Reality:** `smart-tests subset robot` requires the dry-run XML output. Passing a `.robot` source file causes "ParseError: not well-formed XML."
>
> **Misconception #5:** "I don't need `eval` if my test names don't have spaces."
>
> **Reality:** The subset output contains suite names in single quotes. `eval` is always required for correct parsing, regardless of whether individual test names contain spaces.

---

## Deep Dive: Core Concepts

### Predictive Test Selection Fundamentals

**The Problem:**
- Hundreds of tests taking 15+ minutes to execute
- Most code changes only affect a small subset of tests
- Developers wait for results even when changes are localized
- CI infrastructure costs scale with test suite size

**The Smart Tests Solution:**

Instead of running all tests, Smart Tests predicts which tests are relevant to specific code changes:

| | PTSv1 (ML-based) | PTSv2 (AI-based) |
|---|---|---|
| **How it works** | Learns historical relationship between code changes and test failures | Analyzes the code change directly using OpenAI |
| **Input** | Past test run history | `git diff` content |
| **Warm-up** | 3-5 runs minimum | None — predictions from first run |
| **Improves over time** | Yes — more runs = better predictions | Yes — model is continuously updated by CloudBees |

**Key Benefits (both versions):**

| Benefit | Customer Impact |
|---|---|
| **50-80% Faster Feedback** | Developers get test results in minutes instead of 30+ minutes |
| **Cost Reduction** | Lower CI compute costs by running fewer tests |
| **Maintained Quality** | High accuracy (>90%) ensures regressions are caught |
| **Scalability** | Test suite can grow without proportional time increase |
| **Developer Experience** | Less waiting, faster iteration cycles |

### Observation Mode: Risk-Free Validation

**Concept:** Run all tests while Smart Tests creates predictions in parallel, allowing validation without risk.

| What Happens in Your CI | What Smart Tests Does |
|---|---|
| All tests run normally | Creates predicted subset based on code changes |
| Test results recorded | Uploads actual results to CloudBees |
| Build succeeds/fails as usual | Compares predictions vs. actual failures |
| No behavior change | Shows "what-if" analysis in UI |

**Why This Matters:**
- **Zero Risk:** Your CI pipeline continues unchanged
- **Proof of Value:** See actual time savings before committing
- **Accuracy Validation:** Verify predictions match your codebase patterns
- **Stakeholder Buy-In:** Show concrete data to management

> **Warning — COMMON MISCONCEPTIONS: Observation Mode**
>
> **Misconception #1:** "Observation mode is just for demo purposes."
>
> **Reality:** Observation mode is a critical production phase. Most successful deployments run observation mode for 1-2 weeks before enabling test selection.
>
> **Misconception #2:** "In observation mode, Smart Tests doesn't do anything."
>
> **Reality:** Smart Tests actively records test results and builds or refines its prediction model. You're accumulating history while maintaining zero risk.
>
> **Misconception #3:** "For PTSv1, after 3 runs I can switch to production mode."
>
> **Reality:** 3-5 runs is the minimum for predictions to appear. For reliable production use, wait for consistent >85% accuracy across 50+ sessions covering diverse commit types.
>
> **Misconception #4:** "Observation mode slows down my CI."
>
> **Reality:** Smart Tests operations (recording metadata, generating predictions) add negligible overhead (<5 seconds). Tests run at normal speed.

### Production Mode: Enabling Test Selection

| Observation Mode | Production Mode |
|---|---|
| `--observation` flag used | `--observation` flag removed |
| All tests run | Only predicted subset runs |
| Time savings are **projected** | Time savings are **realized** |
| Zero risk (all tests execute) | Minimal risk (high accuracy validated) |
| Used during validation | Used for daily development |

**Demo App Scenario:**

```
Observation Mode (validation phase):
  All tests collected: 451 Robot Framework tests
  Predicted subset: ~340 tests (75%)
  Tests executed: ALL 451 tests  ~31 minutes
  Result: Validates predicted ~340 would catch all failures

Production Mode (after validation):
  All tests collected: 451 tests
  Predicted subset: ~340 tests (75%)
  Tests executed: ONLY ~340 tests  ~23 minutes
  Result: 25% time savings realized
```

**When to Transition to Production Mode:**

| Criterion | PTSv1 | PTSv2 |
|---|---|---|
| **Predictions appearing** | Must see Subset/Remainder counts (not "No subset requests") | Appears from first run |
| **Accuracy** | Consistently >85-95% over 1-2 weeks | Verify 1-2 observation sessions look correct |
| **Observation sessions** | 50-100+ recommended | 5-10 sufficient |
| **False negatives** | Minimal or zero missed failures | Minimal or zero missed failures |
| **Rollout** | Gradual — feature branches first | Can roll out faster given no warm-up |

> **Tip — Gradual Production Rollout**
>
> 1. **Week 1-2:** All branches in observation mode
> 2. **Week 3:** Enable production mode for feature branches only
> 3. **Week 4:** Enable for pull request validation builds
> 4. **Week 5:** Enable for develop/staging branches
> 5. **Week 6+:** Enable for main/production branches
>
> Monitor the Unify dashboard after each stage. Revert to observation mode on any branch where subset predictions miss failures.

> **Warning — Fallback Options**
>
> Always maintain the ability to run the full test suite:
> - Keep the full suite workflow (`tests-robot-no-smarttests.yml`) available for critical changes
> - Add a manual trigger to bypass subsetting for release builds
> - Monitor accuracy continuously and revert to observation mode if it degrades
> - Document the process for disabling predictions in emergencies

---

## Knowledge Check: Core Concepts

1. **What determines whether Smart Tests uses PTSv1 (ML) or PTSv2 (AI) prediction?**
   - [ ] The CLI version installed
   - [ ] A flag passed to `smart-tests subset`
   - [x] The token you create in CloudBees Unify — the org is enabled for one version, and the token connects to that engine
   - [ ] Whether you pass `--observation` or not

2. **What does "No subset requests" mean in a PTSv1 workflow?**
   - [ ] Something is broken
   - [ ] The token is invalid
   - [x] The ML model doesn't have enough history yet — expected for first 3-5 runs
   - [ ] All tests will be skipped

3. **For PTSv2, when do predictions first appear?**
   - [ ] After 3-5 runs
   - [ ] After 50 sessions
   - [x] From the first run — no warm-up required
   - [ ] Only after switching to production mode

4. **Which CLI is used for both PTSv1 and PTSv2?**
   - [ ] A different CLI per version — `smart-tests-cli` for PTSv2, `launchable` for PTSv1
   - [x] `smart-tests-cli==2.11.2` for both — the token determines which engine runs
   - [ ] PTSv2 uses a REST API directly, no CLI needed
   - [ ] No CLI is needed

5. **What must you pass to `smart-tests subset robot`?**
   - [ ] The `.robot` source file
   - [ ] The `output.xml` from a real test run
   - [x] The `output.xml` produced by `robot --dryrun --outputdir`
   - [ ] A plain text list of test names

6. **Why is `eval` required when running Robot Framework with Smart Tests subset output?**
   - [ ] To speed up execution
   - [x] Because subset output contains single-quoted arguments that word-split without eval
   - [ ] To enable parallel execution
   - [ ] It is not actually required

---

## Implementation Best Practices

### Organizing Robot Framework Tests for Smart Tests

| Pattern | Rationale |
|---|---|
| Separate test suites | API, data-driven, integration as different sessions |
| Clear naming | Helps the prediction engine map code changes to test files |
| Logical grouping | By feature, endpoint, or functional area |
| Consistent tags | Enable selective execution and reporting |

**Demo App Structure:**

```
tests/robot/
  api/                   -> robot-api session
    auth_tests.robot
    projects_tests.robot
    issues_tests.robot
  data_driven/           -> separate subsuite
    auth_edge_cases.robot
  resources/
    api_keywords.robot
    variables.robot
    setup_teardown.robot
```

### Observation Mode Strategy

**Phase 1: Initial Data Collection (Weeks 1-2)**

Goal: Establish baseline patterns (PTSv2) or accumulate enough history for predictions to appear (PTSv1)

```
Actions:
[ ] Enable observation mode in CI
[ ] Run on all branches with real code changes
[ ] Include both passing and failing builds
[ ] PTSv1: collect at least 20-30 test sessions
[ ] PTSv2: collect at least 5-10 sessions to validate accuracy

Monitoring:
- PTSv1: Watch for "No subset requests" to disappear
- PTSv2: Verify predictions appear on first run
- Verify session ID is written to session.txt in logs
- Ensure output.xml upload succeeds in record tests step
```

**Phase 2: Accuracy Evaluation (Weeks 3-4)**

Goal: Validate prediction quality before switching to production

```
Analysis:
[ ] Review accuracy metrics per change type
[ ] Identify patterns of high/low accuracy
[ ] Check if false negatives are acceptable
[ ] Calculate potential time savings

Metrics to Track:
- Subset vs. Remainder counts
- Whether failing tests appear in Subset (not Remainder)
- Accuracy by change size (small vs. large commits)
```

**Phase 3: Production Readiness (Week 5+)**

Goal: Make go/no-go decision

```
Evaluation Criteria:
[ ] Predictions appearing consistently
[ ] Accuracy > 90% consistently
[ ] Time savings > 30%
[ ] Team understands fallback process
[ ] Stakeholder approval

Decision Matrix:
High accuracy + High savings  = ENABLE
High accuracy + Low savings   = ENABLE (low risk)
Low accuracy  + High savings  = WAIT (collect more data)
Low accuracy  + Low savings   = INVESTIGATE
```

### Continuous Monitoring

| Metric | Action If Degraded |
|---|---|
| Accuracy trends | Investigate if drops below 85% |
| False negative rate | Alert if critical tests appear in Remainder |
| Time savings realization | Verify actual vs projected savings |
| PTSv1: "No subset requests" reappearing | May indicate model needs more data for new test areas |

---

## Knowledge Check: Implementation Best Practices

1. **What is the minimum number of observation runs before PTSv1 predictions appear?**
   - [ ] 1 run
   - [x] 3-5 runs with varied commit diffs
   - [ ] 50 runs
   - [ ] Predictions appear immediately

2. **For PTSv1, what is the correct observation mode duration before production?**
   - [ ] 3-5 runs is sufficient
   - [ ] 1 run
   - [x] 1-2 weeks minimum with >50 sessions and consistent accuracy
   - [ ] No minimum

3. **For PTSv2, when is it safe to enable production mode?**
   - [ ] Never — PTSv2 cannot use production mode
   - [ ] Only after 50 sessions
   - [x] After verifying a few observation sessions show correct predictions with no missed failures
   - [ ] Only after 1-2 weeks

---

## Calculating Your Business Value

### ROI Framework

**Three Value Streams:**
1. **Time Savings:** Faster feedback loops
2. **Cost Reduction:** Lower CI infrastructure spend
3. **Productivity Gains:** Developers wait less

### ROI Calculation Worksheet

**Current State Analysis:**

```
Your Test Suite Profile:

1. Test Execution Time
   Full suite runtime: _____ minutes

2. Execution Frequency
   Commits per day: _____
   Developers: _____
   Runs per day: _____ (commits × team size)

3. Annual Execution Time
   Daily: _____ min × _____ runs = _____ minutes
   Annual: _____ min × 250 days = _____ hours
```

**Smart Tests Impact Projection:**

```
Assumptions (adjust based on observation mode data):
  Prediction accuracy: 90% (typical)
  Time savings: 50% (varies by change patterns)
  Adoption rate: 80% of commits

Projected Savings:
  New runtime: _____ minutes (50% of current)
  Time saved per run: _____ minutes
  Daily savings: _____ min × _____ runs × 80% = _____ min
  Annual savings: _____ hours
```

### Reference Project Measurements

| Metric | Value |
|---|---|
| Total Robot Framework tests (full suite) | 451 |
| Quick debug branch tests (`patch-robot-demo-quick`) | 40 |
| Simulated API latency per request | 500ms (full suite), 0ms (quick branch) |
| PTSv1: observation runs before first predictions | ~6 runs on `patch-robot-demo-quick` |
| PTSv1: first prediction result (75% target, 40 tests) | Subset: 30, Remainder: 10 |
| Estimated full-suite baseline runtime | ~31 minutes |
| Estimated full-suite at 75% target (after model ready) | ~23 minutes (~25% savings) |
| Estimated full-suite at 50% target | ~15 minutes (~50% savings) |

| Variable | Impact on ROI |
|---|---|
| Test Suite Size | Larger suites = more savings potential |
| Execution Time | Longer suites = more impactful reductions |
| Commit Frequency | More commits = savings compound faster |
| Team Size | Larger teams = more concurrent runs = more savings |
| CI Costs | Higher compute costs = infrastructure savings matter more |
| Accuracy | Higher accuracy = less risk, faster adoption |

---

## Summary

### What You Learned

**Core Concepts:**
1. **One CLI, Two Engines:** `smart-tests-cli==2.11.2` handles both PTSv1 (ML) and PTSv2 (AI). The token determines which engine runs.
2. **Org-Level Versioning:** A CloudBees org is enabled for PTSv1 OR PTSv2 — not both simultaneously.
3. **Warm-up Difference:** PTSv1 requires 3-5 observation runs; PTSv2 predicts from the first run.
4. **Observation Mode:** Risk-free validation; all tests run while predictions are generated and validated.
5. **Robot Framework Integration:** Standard `robot --dryrun` and `output.xml` — no test code changes required for either version.

**Integration Patterns (identical for PTSv1 and PTSv2):**
- Session reference: `@session.txt`
- Dry-run: `robot --dryrun --outputdir /tmp/robot-dryrun`
- Subset input: always pass `/tmp/robot-dryrun/output.xml` (not `.robot` source files)
- `eval` required for single-quoted subset arguments
- `if: always()` required on record tests step

**Business Value:**
- 25-50% time savings typical at 75-50% targets
- Lower CI infrastructure costs
- Faster developer feedback loops
- Measured with observation mode first

### Critical Success Factors

1. **Correct Version Enabled:** Confirm with CloudBees whether your org has PTSv1 or PTSv2 — request the matching token type
2. **output.xml Output:** Required for result recording — Robot Framework produces this natively
3. **Dry-run XML:** `robot --dryrun --outputdir /tmp/robot-dryrun` must complete successfully
4. **Observation Mode First:** Never skip the validation phase, especially for PTSv1
5. **Metric-Driven Decisions:** Use actual data from CloudBees dashboard, not assumptions
6. **Gradual Rollout:** Start small, expand with confidence

---

## Additional Resources

- Demo repository: https://github.com/cloudbees-ps/smart-tests-robot-demo
- PTSv2 demo branch: `patch-robot-demo-ptsv2` — workflow: `tests-robot-smarttests-pts-v2.yml`
- PTSv1 demo branch: `patch-robot-demo-ptsv1` — workflow: `tests-robot-smarttests-pts-v1.yml`
- Quick branch (40 tests, 0ms latency, both PTSv1 and PTSv2): `patch-robot-demo-quick` — workflows: `tests-robot-smarttests-pts-v1-quick.yml` / `tests-robot-smarttests-pts-v2-quick.yml`
- Baseline workflow (no Smart Tests): `tests-robot-no-smarttests.yml`
- GitHub OIDC auth workflow: `tests-robot-github-app-integration-oidc.yml`
- CLI command reference and workflow examples: [SMART_TESTS_CLI_REFERENCE.md](./SMART_TESTS_CLI_REFERENCE.md)
- CloudBees Smart Tests documentation: https://docs.cloudbees.com/docs/cloudbees-smart-tests/latest/
- GitHub OIDC migration guide: https://docs.cloudbees.com/docs/cloudbees-smart-tests/latest/send-data-to-smart-tests/set-up-smart-tests/migration-to-github-oidc-auth

---

## GitHub App + OIDC Authentication

> **Scope note:** This section covers GitHub OIDC for Smart Tests CLI authentication on GitHub Actions — specifically the `EXPERIMENTAL_GITHUB_OIDC_TOKEN_AUTH` flag in `smart-tests-cli`. This is different from the OIDC configuration used with CloudBees CI or AWS-based workflows, where OIDC is the only supported authentication method for the runner itself. The two are unrelated — this is purely about how the Smart Tests CLI proves its identity to the Smart Tests backend.

The demo repository includes per-version OIDC workflows that authenticate using GitHub OIDC instead of a static API token secret. This is the recommended approach for production use — it eliminates long-lived secrets and uses short-lived, verifiable tokens issued by GitHub.

### OIDC Workflows in This Repository

| Workflow | Branch | Tests | Latency |
|---|---|---|---|
| `tests-robot-github-app-integration-oidc-v2.yml` | `patch-robot-demo-ptsv2` | 451 | 500ms |
| `tests-robot-github-app-integration-oidc-v1.yml` | `patch-robot-demo-ptsv1` | 451 | 500ms |
| `tests-robot-github-app-integration-oidc-v2-quick.yml` | `patch-robot-demo-quick` | 40 | 0ms |
| `tests-robot-github-app-integration-oidc-v1-quick.yml` | `patch-robot-demo-quick` | 40 | 0ms |

Always select the matching branch when triggering manually from the GitHub Actions UI.

**How authentication works in each approach:**

In the token-based workflow, every `smart-tests` CLI call reads the `SMART_TESTS_TOKEN` environment variable and sends it as a bearer token with each API request to the Smart Tests backend. The token is a long-lived credential stored as a GitHub secret.

With OIDC, setting `EXPERIMENTAL_GITHUB_OIDC_TOKEN_AUTH: 1` tells the CLI to skip the token entirely. Instead, GitHub issues a short-lived OIDC JWT for the job (via the `id-token: write` permission), and the CLI presents that to the Smart Tests backend to prove it is running in a trusted GitHub Actions context. No secret is stored anywhere — the token exists only for the duration of the job.

### What Changes vs. Token-Based Auth

| | Token-based (`SMART_TESTS_TOKEN`) | GitHub OIDC |
|---|---|---|
| **Secret required** | Yes — `PTSv1_TOKEN` or `PTSv2_TOKEN` | No |
| **Auth mechanism** | Static API key sent with every CLI call | Short-lived OIDC token signed by GitHub, valid for one job |
| **Workflow files** | `tests-robot-smarttests-pts-v1.yml` / `pts-v2.yml` etc. | `tests-robot-github-app-integration-oidc-v1.yml` / `v2.yml` etc. |

### Required Workflow Changes

Three additions to the standard workflow:

**1. Job-level permissions block** (allows GitHub to issue an OIDC token for this job):
```yaml
permissions:
  id-token: write
  contents: read
```

**2. Environment variables** (replace the token secret):

For PTSv2 workflows:
```yaml
env:
  EXPERIMENTAL_GITHUB_OIDC_TOKEN_AUTH: 1
  SMART_TESTS_ORGANIZATION: ${{ vars.SMART_TESTS_ORGANIZATION_v2 }}
  SMART_TESTS_WORKSPACE: ${{ vars.SMART_TESTS_WORKSPACE_v2 }}
```

For PTSv1 workflows:
```yaml
env:
  EXPERIMENTAL_GITHUB_OIDC_TOKEN_AUTH: 1
  SMART_TESTS_ORGANIZATION: ${{ vars.SMART_TESTS_ORGANIZATION_v1 }}
  SMART_TESTS_WORKSPACE: ${{ vars.SMART_TESTS_WORKSPACE_v1 }}
```

The `_v1` and `_v2` suffix allows both PTSv1 and PTSv2 workspaces to coexist in the same repository without conflicting. Set these as **repository variables** (not secrets) under **Settings > Secrets and variables > Actions > Variables**.

> **Important:** The variable values must be **UUIDs**, not display names. The Smart Tests API resolves identity by UUID. Using display names (e.g. `ps-lab` or `anudeep`) returns `401 Unauthorized`. Find the UUIDs in CloudBees Unify under **Admin Settings > Organization Profile** (Organization ID field) and the sub-org settings page.

**3. GitHub App action** (uploads test result artifacts for the GitHub App to process):
```yaml
- name: Store Test Results for Smart Tests (GitHub App)
  if: always()
  uses: cloudbees-oss/smart-tests-results-upload-action@v1
```

> **What this action does:** It is NOT a replacement for `smart-tests record tests`. It uploads test result files (XML, JSON, etc.) as GitHub Actions artifacts so the Smart Tests GitHub App can read them independently. The `smart-tests record tests robot` CLI step still runs separately and is still required — the two serve different purposes. The action requires no parameters; it auto-discovers result files by common patterns (`**/*.xml`, `**/test-results/**`, etc.).

All `smart-tests record` and `smart-tests subset` CLI steps are identical to the token-based workflows — only the authentication mechanism changes.

### Prerequisites

- **GitHub App installed:** Install `cloudbees-oss/smart-tests-results-upload-action` on the repository via GitHub Apps settings
- **OIDC enabled for your workspace:** Contact the CloudBees Smart Tests team to enable OIDC tokenless auth for your org/workspace UUIDs. This is a backend enablement — the workflow will return `401 Unauthorized` until it is activated.
- **Repository variables set:** Add `SMART_TESTS_ORGANIZATION_v1`, `SMART_TESTS_WORKSPACE_v1`, `SMART_TESTS_ORGANIZATION_v2`, `SMART_TESTS_WORKSPACE_v2` as repository variables with UUID values
- **No `SMART_TESTS_TOKEN` secret needed:** Remove it or leave it unused — the OIDC token replaces it entirely
