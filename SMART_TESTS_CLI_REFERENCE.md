# Smart Tests CLI Reference

Reference for `smart-tests-cli==2.11.2` commands used in this repository, plus complete GitHub Actions workflow examples for both token-based and GitHub OIDC authentication.

---

## Installation

```bash
pip3 install --no-cache-dir smart-tests-cli==2.11.2
```

Requires Python 3.7+ and a Java runtime (used internally for commit ingestion).

---

## Commands

### `smart-tests verify`

Verifies connectivity to the Smart Tests backend and confirms the current authentication is valid.

```bash
smart-tests verify
```

Run this as the first step after installation to catch auth or network issues early. In CI it is typically run with `|| true` so a connectivity warning does not fail the build.

---

### `smart-tests record commit`

Pre-populates commit history in the Smart Tests backend. Required for new workspaces — without it, only the latest commit is available to the prediction engine.

```bash
smart-tests record commit \
  --name <repository-name> \
  --source <path-to-git-repo> \
  --max-days 90
```

| Flag | Required | Description |
|---|---|---|
| `--name` | Yes | Repository identifier, e.g. `org/repo` |
| `--source` | Yes | Path to the git repository root |
| `--max-days` | No | How many days of history to send (default: 30, recommended: 90) |

**In GitHub Actions:**
```bash
smart-tests record commit \
  --name ${{ github.repository }} \
  --source ${{ github.workspace }} \
  --max-days 90
```

---

### `smart-tests record build`

Registers the current CI build in Smart Tests. Groups related test sessions under one build ID.

```bash
smart-tests record build \
  --build <build-id> \
  --source <path-to-git-repo>
```

| Flag | Required | Description |
|---|---|---|
| `--build` | Yes | Unique build identifier |
| `--source` | Yes | Path to the git repository root |

**In GitHub Actions:**
```bash
smart-tests record build \
  --build ${{ github.run_id }} \
  --source ${{ github.workspace }}
```

---

### `smart-tests record session`

Creates a test session in Smart Tests and writes the session ID to stdout. The session ID is used by all subsequent commands.

```bash
smart-tests record session \
  --build <build-id> \
  [--observation] \
  --test-suite <suite-name> > session.txt
```

| Flag | Required | Description |
|---|---|---|
| `--build` | Yes | Build ID (must match the `record build` call) |
| `--observation` | No | Enables observation mode — all tests run, savings are projected |
| `--test-suite` | No | Logical name for this test suite in the UI |

The `> session.txt` redirect writes the session ID to a file. All subsequent commands reference it as `@session.txt`.

**Observation mode** (all tests run, predictions recorded but not acted on):
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

Analyzes the current code changes and returns a predicted subset of Robot Framework tests as CLI arguments ready to pass directly to the `robot` command.

```bash
smart-tests subset robot \
  --session @session.txt \
  [--target 75% | --confidence 90% | --time 10m] \
  /tmp/robot-dryrun/output.xml \
  > smart-tests-subset.txt \
  2>/tmp/subset-status.txt
```

| Flag | Required | Description |
|---|---|---|
| `--session` | Yes | Path to session file, prefixed with `@` |
| `--target %` | No | Run this percentage of expected test duration (e.g. `--target 75%`) |
| `--confidence %` | No | Target probability of catching failures (e.g. `--confidence 90%`) |
| `--time` | No | Maximum runtime (e.g. `--time 10m`) |
| positional arg | Yes | Path to the Robot Framework dry-run `output.xml` |

The dry-run `output.xml` is produced by running `robot --dryrun` first — this enumerates tests without executing them. The subset command reads this file to know which tests exist, then returns Robot CLI arguments (e.g. `-s Api -t 'Test Name'`) that select the predicted subset.

**stdout** contains the Robot Framework CLI arguments for the subset.
**stderr** contains the human-readable status table (pass to a log file or display with `cat`).

**In GitHub Actions:**
```bash
mkdir -p /tmp/robot-dryrun
robot --dryrun --outputdir /tmp/robot-dryrun tests/robot/ 2>/dev/null || true

smart-tests subset robot \
  --session @session.txt \
  --target 75% \
  /tmp/robot-dryrun/output.xml \
  > smart-tests-subset.txt \
  2>/tmp/subset-status.txt

cat /tmp/subset-status.txt  # show predictions table in CI log
```

> **PTSv1 warm-up:** On the first 3-5 runs the subset command returns an empty file and the status shows "No subset requests." The workflow falls back to running all tests. This is expected — the ML model needs accumulated history. PTSv2 returns predictions from the first run.

---

### `smart-tests record tests robot`

Uploads Robot Framework test results to Smart Tests. Must run with `if: always()` — Smart Tests needs results from both passing and failing runs to improve prediction accuracy.

```bash
smart-tests record tests robot \
  --session @session.txt \
  test-results/output.xml
```

| Argument | Required | Description |
|---|---|---|
| `--session` | Yes | Path to session file, prefixed with `@` |
| positional arg | Yes | Path to Robot Framework `output.xml` results file |

Robot Framework writes `output.xml` to the `--outputdir` automatically — no extra flags needed.

**In GitHub Actions:**
```bash
smart-tests record tests robot \
  --session @session.txt \
  test-results/output.xml
```

---

## Optimization Target Reference

All three target types are accepted by `smart-tests subset`:

| Type | Example | When to use |
|---|---|---|
| `--target %` | `--target 75%` | Run a percentage of expected duration. Most flexible — used in this demo. |
| `--confidence %` | `--confidence 90%` | Target a probability of catching failures. Best when test list is consistent. |
| `--time` | `--time 10m` | Hard time cap. Best when total suite duration is stable. |

---

## Authentication Reference

### Token-based (default)

Set `SMART_TESTS_TOKEN` in the environment. The CLI reads this variable on every command and sends it as a bearer token to the Smart Tests backend.

```yaml
env:
  SMART_TESTS_TOKEN: ${{ secrets.PTSv2_TOKEN }}  # or PTSv1_TOKEN
```

### GitHub OIDC (recommended for GitHub Actions)

No secret required. The CLI uses a short-lived OIDC JWT issued by GitHub for the job instead of a static token. See the [GitHub OIDC workflow example](#example-github-actions-workflow-github-oidc-auth) below.

Three requirements:
1. `permissions: id-token: write` on the job
2. `EXPERIMENTAL_GITHUB_OIDC_TOKEN_AUTH: 1` in env
3. `SMART_TESTS_ORGANIZATION` and `SMART_TESTS_WORKSPACE` set to **UUID values** (not display names)
4. OIDC tokenless auth enabled for your workspace by the CloudBees Smart Tests team (backend activation required)

---

## Example: GitHub Actions Workflow — Token-Based Auth

Standard workflow using `SMART_TESTS_TOKEN`. Used by all four main demo workflows in this repository.

```yaml
name: Robot Framework Tests (PTSv2)

on:
  workflow_dispatch:
    inputs:
      mode:
        description: 'Smart Tests mode'
        required: true
        type: choice
        default: 'observation'
        options: [observation, production]
      target:
        description: 'Optimization target'
        required: false
        default: '--target 75%'
        type: string

jobs:
  robot-tests:
    runs-on: ubuntu-latest
    env:
      SMART_TESTS_TOKEN: ${{ secrets.PTSv2_TOKEN }}
      OBSERVATION_FLAG: ${{ inputs.mode == 'observation' && '--observation' || ' ' }}
      TARGET_FLAG: ${{ inputs.target || '--target 75%' }}

    steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0

    - uses: actions/setup-python@v5
      with:
        python-version: '3.13.1'

    - uses: actions/setup-java@v4
      with:
        distribution: temurin
        java-version: '17'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt -r requirements-robot.txt
        pip3 install --no-cache-dir smart-tests-cli==2.11.2

    - name: Verify connectivity
      run: smart-tests verify || true

    - name: Record commits
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

    - name: Dry-run test discovery
      run: |
        mkdir -p /tmp/robot-dryrun
        robot --dryrun --outputdir /tmp/robot-dryrun tests/robot/ 2>/dev/null || true

    - name: Generate subset
      run: |
        smart-tests subset robot \
          --session @session.txt \
          $TARGET_FLAG \
          /tmp/robot-dryrun/output.xml \
          > smart-tests-subset.txt 2>/tmp/subset-status.txt || true
        cat /tmp/subset-status.txt || true

    - name: Run tests
      run: |
        mkdir -p test-results
        SUBSET=$(cat smart-tests-subset.txt)
        if [ -s smart-tests-subset.txt ] && [ "$SUBSET" != "ALL" ]; then
          eval robot --outputdir test-results --output output.xml \
            --log log.html --report report.html --xunit junit.xml \
            $SUBSET tests/robot/ || true
        else
          robot --outputdir test-results --output output.xml \
            --log log.html --report report.html --xunit junit.xml \
            tests/robot/ || true
        fi

    - name: Record results
      if: always()
      run: |
        smart-tests record tests robot \
          --session @session.txt \
          test-results/output.xml
```

---

## Example: GitHub Actions Workflow — GitHub OIDC Auth

No `SMART_TESTS_TOKEN` secret required. All seven CLI steps are identical to the token-based example — only the `permissions` block and `env` section differ.

```yaml
name: Robot Framework Tests (GitHub App - OIDC)

on:
  workflow_dispatch:
    inputs:
      mode:
        description: 'Smart Tests mode'
        required: true
        type: choice
        default: 'observation'
        options: [observation, production]
      target:
        description: 'Optimization target'
        required: false
        default: '--target 75%'
        type: string

jobs:
  robot-tests:
    runs-on: ubuntu-latest

    # Required: allows GitHub to issue an OIDC token for this job
    permissions:
      id-token: write
      contents: read

    env:
      # Enable OIDC auth — CLI uses GitHub-issued JWT instead of SMART_TESTS_TOKEN
      EXPERIMENTAL_GITHUB_OIDC_TOKEN_AUTH: 1
      # Must be UUID values, not display names
      SMART_TESTS_ORGANIZATION: <YOUR_ORG_UUID>
      SMART_TESTS_WORKSPACE: <YOUR_WORKSPACE_UUID>
      OBSERVATION_FLAG: ${{ inputs.mode == 'observation' && '--observation' || ' ' }}
      TARGET_FLAG: ${{ inputs.target || '--target 75%' }}

    steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0

    - uses: actions/setup-python@v5
      with:
        python-version: '3.13.1'

    - uses: actions/setup-java@v4
      with:
        distribution: temurin
        java-version: '17'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt -r requirements-robot.txt
        pip3 install --no-cache-dir smart-tests-cli==2.11.2

    - name: Verify connectivity
      run: smart-tests verify || true

    - name: Record commits
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

    - name: Dry-run test discovery
      run: |
        mkdir -p /tmp/robot-dryrun
        robot --dryrun --outputdir /tmp/robot-dryrun tests/robot/ 2>/dev/null || true

    - name: Generate subset
      run: |
        smart-tests subset robot \
          --session @session.txt \
          $TARGET_FLAG \
          /tmp/robot-dryrun/output.xml \
          > smart-tests-subset.txt 2>/tmp/subset-status.txt || true
        cat /tmp/subset-status.txt || true

    - name: Run tests
      run: |
        mkdir -p test-results
        SUBSET=$(cat smart-tests-subset.txt)
        if [ -s smart-tests-subset.txt ] && [ "$SUBSET" != "ALL" ]; then
          eval robot --outputdir test-results --output output.xml \
            --log log.html --report report.html --xunit junit.xml \
            $SUBSET tests/robot/ || true
        else
          robot --outputdir test-results --output output.xml \
            --log log.html --report report.html --xunit junit.xml \
            tests/robot/ || true
        fi

    - name: Record results
      if: always()
      run: |
        smart-tests record tests robot \
          --session @session.txt \
          test-results/output.xml

    # GitHub App action — uploads result artifacts for the GitHub App to read.
    # This is NOT a replacement for 'smart-tests record tests' above.
    # Both steps serve different purposes and both are required.
    - name: Store results for GitHub App
      if: always()
      uses: cloudbees-oss/smart-tests-results-upload-action@v1
```

> **OIDC scope note:** `EXPERIMENTAL_GITHUB_OIDC_TOKEN_AUTH` is specific to the Smart Tests CLI authenticating to the Smart Tests backend. It is unrelated to OIDC used in CloudBees CI or AWS-based workflows, where OIDC is the authentication method for the runner itself. The two use the same protocol but serve completely different purposes.

> **Backend activation required:** The workflow will return `401 Unauthorized` on all CLI calls until CloudBees enables OIDC tokenless auth for your specific workspace UUID. Contact the Smart Tests team with your `SMART_TESTS_ORGANIZATION` and `SMART_TESTS_WORKSPACE` UUIDs to request activation.
