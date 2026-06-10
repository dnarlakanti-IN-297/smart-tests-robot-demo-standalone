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

The repository includes two demo branches, one for each version:

| Version | Branch | Workflow | Tests | Latency |
|---|---|---|---|---|
| PTSv2 (AI-based) | `patch-robot-demo-ptsv2` | `tests-robot-smarttests-pts-v2.yml` | 451 | 500ms simulated |
| PTSv1 (ML-based) | `patch-robot-demo-ptsv1` | `tests-robot-smarttests-pts-v1.yml` | 451 | 500ms simulated |
| PTSv1 quick | `patch-robot-demo-quick` | `tests-robot-smarttests-pts-v1.yml` | 40 | 0ms |
| PTSv2 quick | `patch-robot-demo-quick` | `tests-robot-smarttests-pts-v2.yml` | 40 | 0ms |

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
| **Time commitment** | 30-60 minutes depending on version |

### Parameterized Values

| Placeholder | Description | Where to Find |
|---|---|---|
| `<YOUR_TOKEN>` | One CloudBees API token, created from the org/workspace where your version is enabled. PTSv1 token routes to the ML engine; PTSv2 token routes to OpenAI. | CloudBees UI: Smart Tests > Settings > Create a Workspace API Key |

> **Note:** You only need one token. Create it in the org/workspace that has your version enabled (PTSv1 or PTSv2). Add it to GitHub secrets as `PTSv1_TOKEN` (for PTSv1) or `PTSv2_TOKEN` (for PTSv2).

---

## Implementation

### Initial Setup

#### Fork the Repository

1. Navigate to: https://github.com/cloudbees-ps/smart-tests-robot-demo
2. Click **Fork** button (top right)
3. Select your GitHub account
4. Wait for fork to complete

**Result:** Personal copy of repository under your GitHub account

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

#### Choose Your Demo Branch

Use the branch that matches your org's enabled version:

| Your org version | Branch to use | Workflow to use |
|---|---|---|
| PTSv2 | `patch-robot-demo-ptsv2` | Robot Framework Tests (PTSv2) |
| PTSv1 | `patch-robot-demo-ptsv1` | Robot Framework Tests (PTSv1) |
| PTSv1 quick (40 tests, 0ms) | `patch-robot-demo-quick` | Robot Framework Tests (Quick - PTSv1) |
| PTSv2 quick (40 tests, 0ms) | `patch-robot-demo-quick` | Robot Framework Tests (Quick - PTSv2) |

The demo workflows are pre-configured to trigger on these branches. You can also create your own branch and update the workflow trigger.

#### Establish Baseline

1. Navigate to **Actions** tab
2. Click **Robot Framework Tests (No Smart Tests - Baseline)** workflow
3. Click **Run workflow**
4. Configure:
   - Branch: your chosen branch from the table above
5. Click **Run workflow**

Wait for the workflow to complete (~31 minutes with 500ms simulated latency).

> **Note — What just happened:**
>
> This established your baseline — a full test run with all 451 tests and no Smart Tests optimization. This is your reference runtime. Every subsequent Smart Tests run will be compared against this number.

#### Run Tests with Smart Tests (Observation Mode)

1. Navigate to **Actions** tab
2. Click the appropriate workflow for your version (see table above)
3. Click **Run workflow**
4. Configure:
   - Branch: your chosen branch
   - **mode:** `observation` (default — keep as-is)
   - **target:** `--target 75%` (default — keep as-is)
5. Click **Run workflow**

Wait for the workflow to complete.

> **PTSv1 only — Repeat this step 5-7 times before expecting predictions.** PTSv1 needs a history of test results to train its ML model. Use `patch-robot-demo-quick` (40 tests, 0ms) to build history faster — each run takes ~1-2 minutes instead of ~31 minutes. To generate varied commit diffs, make a small change to any source file (e.g., add a blank line to `app/main.py`), commit it, and push. Each push triggers the workflow automatically. Alternatively, use the **Run workflow** button to trigger runs manually — but varied commits produce better predictions.

> **Note — What Smart Tests is doing behind the scenes:**
>
> 1. **Record commit history:** `smart-tests record commit` pre-populates 90 days of git history so the prediction engine understands your codebase evolution
> 2. **Record build:** `smart-tests record build` registers this CI run in CloudBees
> 3. **Record session:** `smart-tests record session --observation` creates a test session and writes the session ID to `session.txt` automatically via the `> session.txt` redirect
> 4. **Dry-run test discovery:** `robot --dryrun --outputdir /tmp/robot-dryrun` enumerates all 451 tests and writes the test list to `/tmp/robot-dryrun/output.xml`
> 5. **Generate subset:** `smart-tests subset robot --session @session.txt ... /tmp/robot-dryrun/output.xml` analyzes commits and predicts which tests are affected; output is Robot Framework CLI arguments
> 6. **Run ALL tests:** In observation mode, all 451 tests execute even if a subset was returned; results are written to `test-results/output.xml` automatically by Robot Framework
> 7. **Record results:** `smart-tests record tests robot --session @session.txt test-results/output.xml` uploads results to CloudBees
>
> **PTSv2:** Predictions appear from the first run — the AI model analyzes the code change directly.
>
> **PTSv1:** On the first 3-5 runs, the subset step returns an empty file and status shows "No subset requests." The workflow automatically falls back to running all tests. This is expected behavior, not an error. The ML model needs accumulated history before it can generate predictions.

#### View Test Sessions

1. Open https://cloudbees.io
2. Navigate to **Smart Tests > Sessions**
3. Find the sessions for your recent runs

**PTSv2 — from the first run:**
```
Session status    : Observation mode
Tests executed    : 451
Projected subset  : ~340 tests at 75% target
```

**PTSv1 — during warm-up (first 3-5 runs on `patch-robot-demo-quick`):**
```
Session status    : Observation mode
Tests executed    : 40
Subset            : (none — model building history)
Remainder         : (none)
```

**PTSv1 — after warm-up (6+ runs on `patch-robot-demo-quick`, actual result):**
```
Session status    : Session passed
Tests executed    : 40
Subset            : 30 testcases
Remainder         : 10 testcases
```

> **Tip — Key metrics to understand:**
>
> - **Session passed / Session failed:** Overall result
> - **Subset count:** Tests Smart Tests selected to run
> - **Remainder count:** Tests Smart Tests deferred
> - **Accuracy:** Did the subset include all failing tests? Look for >90%.

---

### Experiment with Workflow Options

Both workflows accept the same two input parameters:

| Parameter | Options | What It Controls |
|---|---|---|
| `mode` | `observation` (default), `production` | Whether all tests run or only the predicted subset |
| `target` | `--target 75%` (default), `--target 50%`, `--target 30%`, `--confidence 90%` | How Smart Tests selects the test subset |

#### Understanding Optimization Targets

Smart Tests offers three types of optimization targets, each suited for different scenarios:

**Percentage time target (`--target %`):**
- Returns a percentage of the expected test duration
- Best for test suites with variable duration
- Example: `--target 50%` runs 50% of expected duration (~15 min if full suite = 31 min)
- Used in this demo — most flexible option

**Confidence target (`--confidence %`):**
- Targets a probability of catching failing sessions
- Best for test suites with consistent test lists
- Example: `--confidence 90%` runs tests up to the duration that gives 90% confidence

**Fixed time target (`--time`):**
- Sets a maximum test runtime
- Best for test suites with stable run duration
- Example: `--time 10m` runs up to 10 minutes of most relevant tests

> **Note — Choosing the right optimization target:**
>
> Use `--target %` (percentage) when:
> - Your test sessions vary in duration
> - You want predictable subset size relative to full suite
> - (This demo uses percentage targets — most flexible option)
>
> Use `--confidence %` when:
> - Your test list is consistent across runs
> - You want to target a specific probability of catching failures
>
> Use `--time` (fixed duration) when:
> - Your test suite has stable total duration
> - You have hard time constraints (e.g., "max 10 minutes")

#### Try Production Mode

1. Go to **Actions** and click the appropriate workflow
2. Click **Run workflow**
3. Configure:
   - **mode:** `production`
   - **target:** `--target 75%`
4. Run workflow

> **Warning:** For PTSv1, only switch to production mode after the model has warmed up (3-5 observation runs with varied commits). For PTSv2, production mode is safe from the first run once you have verified one or two observation sessions look correct. In production mode, only the predicted subset runs — if no subset is available, the workflow falls back to all tests automatically.

#### Try Different Targets

- `--target 75%`: Conservative — ~23 min (~25% savings)
- `--target 70%`: Conservative — ~21 min, lower risk
- `--target 50%`: Balanced — ~15 min (~50% savings)
- `--target 30%`: Aggressive — ~9 min (~70% savings, higher risk)

> **Tip — What to observe:**
>
> **Observation mode:**
> - All 451 tests run every time
> - Predictions are created but not acted upon
> - Zero risk — validates accuracy
> - Time savings are projected, not realized
>
> **Production mode:**
> - Only predicted tests run
> - Actual time savings achieved
> - Small risk if predictions miss failures (PTSv1: higher early on; PTSv2: low from the start)
>
> **Warm-up indicator (PTSv1 only):** When "No subset requests" disappears and the session detail shows actual Subset and Remainder counts, the ML model is ready for production mode.

---

### Hands-On Demo Complete

You've completed:

- [x] Forked the repository and configured your Smart Tests token
- [x] Established baseline runtime with the No Smart Tests workflow (~31 min)
- [x] Ran Smart Tests in observation mode
- [x] Viewed session results in CloudBees Unify
- [x] Experimented with production mode and different targets

**Timing comparison at 75% target (after model is ready):**
- Baseline (no Smart Tests): ~31 minutes
- Smart Tests at 75%: ~23 minutes (~25% savings)
- Smart Tests at 50%: ~15 minutes (~50% savings)

---

## Understanding the CI Integration

Both `tests-robot-smarttests-pts-v2.yml` (PTSv2) and `tests-robot-smarttests-pts-v1.yml` (PTSv1) follow the same seven-step pattern using `smart-tests-cli==2.11.2`. Open either file in the repository to see the complete integration.

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
- PTSv1 quick debug branch (40 tests, 0ms latency): `patch-robot-demo-quick`
- Baseline workflow (no Smart Tests): `tests-robot-no-smarttests.yml`
- CloudBees Smart Tests documentation: https://docs.cloudbees.com/docs/cloudbees-smart-tests/latest/
