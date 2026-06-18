# Smart Tests CLI Reference

Reference for `smart-tests-cli` as used in this Robot Framework demo repository. Covers all CLI commands, flags, observation vs production mode, optimization targets, and complete GitHub Actions workflow examples for both token-based and OIDC authentication.

Official documentation: https://docs.cloudbees.com/docs/cloudbees-smart-tests/latest/

---

## Commands at a Glance

| Command | Purpose | When to Run |
|---|---|---|
| `smart-tests verify` | Check CLI connectivity and authentication | Start of every CI job (optional but recommended) |
| `smart-tests record commit` | Send git commit history to the backend | Once per new workspace setup, or when history is needed |
| `smart-tests record build` | Create a build record, link sessions to a build | Before `record session`, once per CI run |
| `smart-tests record session` | Open a test session, get a session ID | After `record build`, before any `subset` call |
| `smart-tests subset robot` | Generate the predicted test subset for Robot Framework | After `record session`, before running tests |
| `smart-tests record tests robot` | Upload Robot Framework results to the backend | After tests finish, always — even on failure |
| `smart-tests record attachment` | Attach log files to a session in the Unify UI | After tests finish, for additional debugging artifacts |
| `smart-tests inspect subset` | Show details of a past subset request | For debugging predictions — what was included and why |
| `smart-tests stats test-sessions` | Show statistics about recent test sessions | For reviewing savings and session counts over time |

---

## Installation

```bash
# Install a specific version (used in this repo)
pip3 install --no-cache-dir smart-tests-cli==2.11.2

# Install latest
pip3 install --user --upgrade smart-tests
```

**Requirements:**
- Python 3.7 or later
- Java runtime environment (used internally for commit ingestion)

---

## Authentication

Every `smart-tests` CLI call must be able to identify the organization and workspace it is sending data to. There are two ways to provide this.

### Option 1 — API Token (default)

Set `SMART_TESTS_TOKEN` in the environment. The CLI reads this variable on every call and sends it as a bearer token to the Smart Tests backend. The token encodes your org and workspace identity.

```yaml
# GitHub Actions — add as a repository secret
env:
  SMART_TESTS_TOKEN: ${{ secrets.PTSv2_TOKEN }}
```

Obtain the token from **CloudBees Unify > Smart Tests > Settings > Create a Workspace API Key**.

### Option 2 — GitHub OIDC (no secret required)

For GitHub Actions only. Set the flag below and provide your org/workspace UUIDs. GitHub issues a short-lived token for the job instead. See the [GitHub OIDC workflow example](#example-workflow-github-oidc-auth) for the full setup.

```yaml
env:
  EXPERIMENTAL_GITHUB_OIDC_TOKEN_AUTH: 1
  SMART_TESTS_ORGANIZATION: <YOUR_ORG_UUID>
  SMART_TESTS_WORKSPACE: <YOUR_WORKSPACE_UUID>
```

> **UUID vs display name:** `SMART_TESTS_ORGANIZATION` and `SMART_TESTS_WORKSPACE` must be the UUID values, not display names. Find them in CloudBees Unify under **Admin Settings > Organization Profile**. Using display names returns `401 Unauthorized`.

---

## Required Command Sequence

Every CI run must follow this order:

```
1. smart-tests record build
2. smart-tests record session       →  writes session ID to session.txt
3. smart-tests subset robot         →  reads session.txt, writes subset args
4. [run tests]
5. smart-tests record tests robot   →  reads session.txt, uploads results
```

`record session` must run after `record build`. `subset` and `record tests` both require a valid session ID.

---

## Observation Mode vs Production Mode

Before relying on Smart Tests to skip tests in CI, run in **observation mode** to validate prediction accuracy with zero risk.

### Observation mode

Enable with the `--observation` flag on `record session`:

```bash
smart-tests record session --build $BUILD_ID --observation --test-suite my-suite > session.txt
```

**What happens:**
- All tests run as normal — nothing is skipped
- Smart Tests records which tests were predicted and which actually ran
- The CloudBees Unify UI shows **projected savings**: how many tests would have run in production mode, and whether the predicted subset would have caught all failures
- No actual time is saved yet — this is your validation phase

**When to move to production:**
- PTSv2: one observation run is sufficient — predictions are available immediately
- PTSv1: run 5-6 observation runs (use the quick branch with 40 tests to build history faster); move to production once the Unify UI shows a Subset and Remainder count

### Production mode

Omit `--observation` from `record session`:

```bash
smart-tests record session --build $BUILD_ID --test-suite my-suite > session.txt
```

**What happens:**
- Smart Tests returns a predicted subset of tests to run
- Only that subset runs — actual time savings are realized
- The Unify UI shows **actual savings** and prediction accuracy

> **PTSv1 warm-up note:** On the first 3-5 runs (even in production mode), the `subset` command returns an empty file and the status shows "No subset requests." The workflow falls back to running all tests automatically. This is expected — the ML model needs historical data. Keep running until Subset and Remainder counts appear in the Unify UI.

---

## Commands

### `smart-tests verify`

Confirms CLI connectivity and authentication. Run this first to catch auth or network issues before the build starts.

```bash
smart-tests verify
```

Outputs platform, Python version, Java command, CLI version, and a success or failure message. In CI, run with `|| true` so a connectivity warning does not fail the build.

```bash
smart-tests verify || true
```

---

### `smart-tests record commit`

Sends commit history to the Smart Tests backend. Needed for new workspaces — without it, only the latest commit is available to the prediction engine, which limits prediction quality.

```bash
smart-tests record commit [OPTIONS]
```

| Flag | Required | Description |
|---|---|---|
| `--name NAME` | No | Repository name (e.g. `org/repo`) |
| `--source DIR` | No | Path to the local git repository root |
| `--max-days DAYS` | No | How many days of history to send (recommended: 90) |
| `--import-git-log-output FILE` | No | Import from a pre-generated git log file |

> In most setups, commit collection runs automatically inside `record build`. Run `record commit` separately only if you need finer control over what history is sent or if `record build` does not collect commits in your environment.

**In GitHub Actions:**
```bash
smart-tests record commit \
  --name ${{ github.repository }} \
  --source ${{ github.workspace }} \
  --max-days 90
```

---

### `smart-tests record build`

Creates a build record in Smart Tests and ties related test sessions together under one build ID. Also collects commit history by default.

```bash
smart-tests record build --build BUILD_NAME [OPTIONS]
```

| Flag | Required | Description |
|---|---|---|
| `--build NAME` | **Yes** | Unique build identifier (e.g. the CI run ID) |
| `--source DIR` | No | Path to the local git repository root |
| `--branch NAME` | No | Branch name |
| `--max-days DAYS` | No | Max days of commit history to collect |
| `--no-commit-collection` | No | Skip commit data collection |
| `--no-submodules` | No | Skip Git submodule info |
| `--commit REPO=HASH` | No | Explicit repo name + commit hash (repeatable) |
| `--component NAME=BUILDNAME` | No | Include another build as a component (repeatable) |
| `--timestamp TIMESTAMP` | No | Override build time (`YYYY-MM-DDThh:mm:ssTZD`) |
| `--link TITLE=URL` | No | Attach an external link to the build (repeatable) |
| `--repo-branch-map REPO=BRANCH` | No | Repo + branch mapping when using `--no-commit-collection` |

**In GitHub Actions:**
```bash
smart-tests record build \
  --build ${{ github.run_id }} \
  --source ${{ github.workspace }}
```

---

### `smart-tests record session`

Creates a test session in Smart Tests. Must run after `record build` and before `subset` or `record tests`. Writes the session ID to stdout — redirect it to a file so subsequent commands can reference it.

```bash
smart-tests record session [OPTIONS] > session.txt
```

| Flag | Required | Description |
|---|---|---|
| `--test-suite NAME` | **Yes** | Logical name for this test suite in the Unify UI |
| `--build NAME` | No | Build ID to attach this session to |
| `--observation` | No | Enable observation mode (all tests run, savings projected) |
| `--flavor KEY=VALUE` | No | Tag the session with metadata (repeatable) |
| `--no-build` | No | Use when sending test reports without a build |
| `--link TITLE=URL` | No | Attach an external link to the session (repeatable) |
| `--timestamp TIMESTAMP` | No | Override session time |

The `> session.txt` redirect captures the session ID. All subsequent commands reference it as `@session.txt`.

**Observation mode** (all tests run, savings projected):
```bash
smart-tests record session \
  --build ${{ github.run_id }} \
  --observation \
  --test-suite robot-api > session.txt
```

**Production mode** (only predicted subset runs):
```bash
smart-tests record session \
  --build ${{ github.run_id }} \
  --test-suite robot-api > session.txt
```

---

### `smart-tests subset robot`

Analyzes the current code changes and generates a predicted subset of Robot Framework tests. Returns Robot Framework CLI arguments (e.g. `-s Api -t 'Test Name'`) ready to pass directly to the `robot` command.

Before calling this command, run `robot --dryrun` to enumerate all available tests and produce the `output.xml` that the subset command reads.

```bash
# Step 1 — enumerate tests without running them
mkdir -p /tmp/robot-dryrun
robot --dryrun --outputdir /tmp/robot-dryrun tests/robot/ 2>/dev/null || true

# Step 2 — generate subset
smart-tests subset robot \
  --session @session.txt \
  [--target 75% | --confidence 90% | --time 10m] \
  /tmp/robot-dryrun/output.xml \
  > smart-tests-subset.txt \
  2>/tmp/subset-status.txt
```

| Flag | Required | Description |
|---|---|---|
| `--session SESSION` | **Yes** | Session ID file, prefixed with `@` (e.g. `@session.txt`) |
| `--target PERCENTAGE` | No | Run this percentage of expected test duration (e.g. `--target 75%`) |
| `--confidence PERCENTAGE` | No | Target probability of catching failures (e.g. `--confidence 90%`) |
| `--time TIME` | No | Maximum runtime (e.g. `--time 10m` or `--time 300`) |
| `--bin INDEX/COUNT` | No | Split subset into parallel bins (e.g. `--bin 1/4`) |
| `--rest FILE` | No | Write remainder (non-subset) tests to a separate file |
| `--ignore-new-tests` | No | Exclude recently added tests from the subset |
| `--ignore-flaky-tests-above N` | No | Exclude tests above a flakiness score threshold |
| `--prioritize-tests-failed-within-hours N` | No | Prioritize tests that failed recently (max 720h) |
| `--get-tests-from-previous-sessions` | No | Pull subset from prior full runs |
| `--base DIR` | No | Base directory for generating portable test names |
| `--no-base-path-inference` | No | Disable automatic base path detection |
| positional arg | **Yes** | Path to the Robot Framework dry-run `output.xml` |

**stdout** contains the Robot Framework CLI arguments for the subset.
**stderr** contains the human-readable status table (show in CI logs with `cat /tmp/subset-status.txt`).

If no sizing flag is provided (`--target`, `--confidence`, or `--time`), Smart Tests automatically selects a target based on historical data.

**In GitHub Actions (with fallback to all tests):**
```bash
smart-tests subset robot \
  --session @session.txt \
  --target 75% \
  /tmp/robot-dryrun/output.xml \
  > smart-tests-subset.txt 2>/tmp/subset-status.txt || echo "ALL" > smart-tests-subset.txt

cat /tmp/subset-status.txt || true
```

Then run Robot Framework using the subset:
```bash
SUBSET=$(cat smart-tests-subset.txt)
if [ -s smart-tests-subset.txt ] && [ "$SUBSET" != "ALL" ]; then
  eval robot --outputdir test-results --output output.xml $SUBSET tests/robot/
else
  robot --outputdir test-results --output output.xml tests/robot/
fi
```

> `eval` is required because the subset output is a string of Robot CLI arguments (e.g. `-s Api -t 'Login test'`) that must be word-split by the shell before being passed to `robot`.

---

### `smart-tests record tests robot`

Uploads Robot Framework test results to Smart Tests. Must run with `if: always()` in GitHub Actions — Smart Tests needs results from both passing and failing runs to improve prediction accuracy over time.

```bash
smart-tests record tests robot \
  --session @session.txt \
  test-results/output.xml
```

| Argument | Required | Description |
|---|---|---|
| `--session SESSION` | **Yes** | Session ID file, prefixed with `@` |
| `--group NAME` | No | Group name for results in the Unify UI |
| `--base CONVERT` | No | Base directory for generating portable test names |
| `--no-base-path-inference` | No | Disable automatic base path detection |
| positional arg | **Yes** | Path to Robot Framework `output.xml` results file |

Robot Framework writes `output.xml` to the directory specified in `--outputdir` automatically — no extra flags needed.

**In GitHub Actions:**
```bash
- name: Record test results
  if: always()
  run: |
    smart-tests record tests robot \
      --session @session.txt \
      test-results/output.xml
```

---

### `smart-tests record attachment`

Attaches log files or other artifacts to a test session in the Unify UI.

```bash
smart-tests record attachment \
  --session @session.txt \
  path/to/logfile.log
```

| Flag | Required | Description |
|---|---|---|
| `--session SESSION` | **Yes** | Session ID file, prefixed with `@` |
| `--include GLOB` | No | File glob filter, e.g. `"*.log"` (repeatable) |
| positional args | **Yes** | Files to attach |

---

### `smart-tests inspect subset`

Displays detailed information about a specific subset request — useful for debugging why a particular test was included or excluded.

```bash
smart-tests inspect subset --subset-id <ID>
smart-tests inspect subset --subset-id <ID> --json
```

| Flag | Required | Description |
|---|---|---|
| `--subset-id INT` | **Yes** | Subset ID (visible in the Unify UI) |
| `--json` | No | Output in JSON format |

Output includes rank, test identifier, inclusion status, and estimated duration per test.

---

### `smart-tests stats test-sessions`

Retrieves statistics about recent test sessions for your workspace.

```bash
smart-tests stats test-sessions
smart-tests stats test-sessions --days 30
```

| Flag | Required | Description |
|---|---|---|
| `--days INT` | No | Number of past days to include |
| `--flavor KEY=VALUE` | No | Filter by session flavor (repeatable) |

Example output:
```json
{"averageDurationSeconds": 653.2, "count": 311, "days": 7}
```

---

## Optimization Target Reference

All three types are accepted by `smart-tests subset`. If none is provided, Smart Tests selects a target automatically.

| Type | Example | What it does | When to use |
|---|---|---|---|
| `--target %` | `--target 75%` | Run tests up to this percentage of the full suite's expected duration | Most flexible — good starting point for most teams. Used in this demo. |
| `--confidence %` | `--confidence 90%` | Run tests up to the duration that gives this probability of catching any failure | When your test list is consistent across runs and you want accuracy guarantees |
| `--time` | `--time 10m` | Run tests up to this hard time limit | When you have a strict pipeline time budget |

**Choosing a starting target:**

- Start at `--target 75%` in production mode. This gives 25% time savings with low risk.
- Review prediction accuracy in Unify (aim for >90% — meaning the subset caught all real failures).
- Reduce gradually: `75%` → `50%` → `30%` as confidence builds.
- Lower targets save more time but increase the chance of missing a failure.

---

## Global Options

These go immediately after `smart-tests`, before any subcommand:

| Option | Description |
|---|---|
| `--dry-run` | Simulate commands without sending data to the backend (GET requests may still occur) |
| `--log-level audit` | Show full API request and response payloads — useful for debugging |
| `--plugins DIR` | Path to custom profile or plugin files |
| `--skip-cert-verification` | Bypass SSL certificate verification (use with caution in restricted networks) |

```bash
# Debug a failing record build call
smart-tests --log-level audit record build --build 1234 --source .

# Simulate without sending data
smart-tests --dry-run record session --build 1234 --test-suite test
```

---

## Example Workflow: Token-Based Auth

Standard approach. Set `SMART_TESTS_TOKEN` as a repository secret. Used by all four main demo workflows in this repository (`tests-robot-smarttests-pts-v2.yml` etc.).

The Smart Tests steps are the same in every job — only the `env:` block changes between token and OIDC auth. Application setup (Python, Java, dependencies, database) is abbreviated below.

```yaml
jobs:
  robot-tests:
    runs-on: ubuntu-latest
    env:
      SMART_TESTS_TOKEN: ${{ secrets.PTSv2_TOKEN }}
      OBSERVATION_FLAG: ${{ github.event_name == 'workflow_dispatch' && inputs.mode == 'observation' && '--observation' || ' ' }}
      TARGET_FLAG: ${{ github.event_name == 'workflow_dispatch' && inputs.target || '--target 75%' }}

    steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0  # required — Smart Tests analyzes full git history

    # ... set up Python, Java, install dependencies, start app ...

    - name: Verify Smart Tests connectivity
      run: smart-tests verify || true

    - name: Record commit history
      run: |
        smart-tests record commit \
          --name ${{ github.repository }} \
          --source ${{ github.workspace }} \
          --max-days 90

    - name: Record build
      run: |
        smart-tests record build \
          --build ${{ github.run_id }} \
          --source ${{ github.workspace }}

    - name: Record session
      run: |
        smart-tests record session \
          --build ${{ github.run_id }} \
          $OBSERVATION_FLAG \
          --test-suite robot-api > session.txt

    - name: Enumerate tests (dry run)
      run: |
        mkdir -p /tmp/robot-dryrun
        robot --dryrun --outputdir /tmp/robot-dryrun tests/robot/ 2>/dev/null || true

    - name: Generate Smart Tests subset
      run: |
        set +e
        smart-tests subset robot \
          --session @session.txt \
          $TARGET_FLAG \
          /tmp/robot-dryrun/output.xml \
          > smart-tests-subset.txt 2>/tmp/subset-status.txt
        EXIT_CODE=$?
        cat /tmp/subset-status.txt || true
        set -e
        [ $EXIT_CODE -ne 0 ] && echo "ALL" > smart-tests-subset.txt || true

    - name: Run Robot tests (subset or all)
      run: |
        SUBSET=$(cat smart-tests-subset.txt)
        if [ -s smart-tests-subset.txt ] && [ "$SUBSET" != "ALL" ]; then
          eval robot --outputdir test-results --output output.xml $SUBSET tests/robot/
        else
          robot --outputdir test-results --output output.xml tests/robot/
        fi

    - name: Record test results
      if: always()
      run: |
        smart-tests record tests robot \
          --session @session.txt \
          test-results/output.xml
```

---

## Example Workflow: GitHub OIDC Auth

No `SMART_TESTS_TOKEN` secret required. Replace the `env:` block with the three lines below and add the `permissions` block. All Smart Tests CLI steps are identical to the token-based example.

> **Prerequisites:** Request OIDC activation from the CloudBees Smart Tests team for your org/workspace UUIDs before using this. The workflow returns `401 Unauthorized` until activation is complete.

```yaml
jobs:
  robot-tests:
    runs-on: ubuntu-latest

    # Allows GitHub to issue a short-lived OIDC token for this job — do not remove
    permissions:
      id-token: write
      contents: read

    env:
      # Tells the CLI to use GitHub's OIDC token instead of SMART_TESTS_TOKEN
      EXPERIMENTAL_GITHUB_OIDC_TOKEN_AUTH: 1
      # Must be UUID values — display names return 401 Unauthorized
      # Find UUIDs in CloudBees Unify > Admin Settings > Organization Profile
      SMART_TESTS_ORGANIZATION: <YOUR_ORG_UUID>
      SMART_TESTS_WORKSPACE: <YOUR_WORKSPACE_UUID>
      OBSERVATION_FLAG: ${{ github.event_name == 'workflow_dispatch' && inputs.mode == 'observation' && '--observation' || ' ' }}
      TARGET_FLAG: ${{ github.event_name == 'workflow_dispatch' && inputs.target || '--target 75%' }}

    steps:
    # ... same steps as token-based example above ...

    - name: Record test results
      if: always()
      run: |
        smart-tests record tests robot \
          --session @session.txt \
          test-results/output.xml
```

> **Note on `smart-tests verify`:** With OIDC, `verify` prints "Authentication failed. Please set SMART_TESTS_TOKEN" because it only checks for the token env var. This message is harmless — the `|| true` prevents it from failing the job, and the actual CLI calls (record build, record session, etc.) authenticate correctly via OIDC.

> **OIDC scope note:** `EXPERIMENTAL_GITHUB_OIDC_TOKEN_AUTH` is specific to the Smart Tests CLI authenticating to the Smart Tests backend. This is unrelated to OIDC used in CloudBees CI or AWS-based workflows.

---

## GitHub App Integration (Optional)

The `cloudbees-oss/smart-tests-results-upload-action` is a GitHub App that reads test results independently of the CLI. It is **optional and separate from both auth methods above** — you can use it with token auth or OIDC auth.

**What it does:** Uploads test result files (XML, etc.) as GitHub Actions artifacts so the Smart Tests GitHub App can process them through its own channel. It auto-discovers result files by common patterns — no parameters needed.

**It is NOT a replacement for `smart-tests record tests`.** Both steps serve different purposes and both are required if you are using the GitHub App integration.

**Installation:** Install the `cloudbees-oss/smart-tests-results-upload-action` GitHub App on your repository via GitHub Apps settings. No configuration is needed in the workflow beyond adding the step.

```yaml
- name: Store results for Smart Tests GitHub App
  if: always()
  uses: cloudbees-oss/smart-tests-results-upload-action@v1
```

Add this step after `smart-tests record tests robot` in either the token-based or OIDC workflow.
