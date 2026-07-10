# Smart Tests Demo: Robot Framework

![Python](https://img.shields.io/badge/python-3.13+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)
![Robot Framework](https://img.shields.io/badge/Robot%20Framework-7.0+-orange.svg)
![Smart Tests](https://img.shields.io/badge/Smart%20Tests-PTSv1%20%7C%20PTSv2-brightgreen.svg)

Demo repository for **CloudBees Smart Tests** predictive test selection with Robot Framework. Uses `smart-tests-cli==2.11.2` for both PTSv1 (ML-based) and PTSv2 (AI-based) — the CLI is identical for both versions; the token determines which prediction engine runs.

**Adoption Journey Guide:** [ISP_SMART_TESTS_ROBOT.md](./ISP_SMART_TESTS_ROBOT.md)
**Multi-Repo Guide:** [ISP_SMART_TESTS_MULTI_REPO.md](./ISP_SMART_TESTS_MULTI_REPO.md)

---

## What This Repository Demonstrates

- **PTSv1 (ML-based):** Builds predictions from historical test run data. Requires 3-5 observation runs before predictions appear.
- **PTSv2 (AI-based):** Uses OpenAI to predict affected tests from the first run. No warm-up required.
- **Identical CLI for both:** `smart-tests-cli==2.11.2` — only the token changes.
- **451 Robot Framework tests** with 500ms simulated API latency (~31 min baseline) to demonstrate realistic enterprise test suite savings.
- **Side-by-side comparison:** Baseline workflow (no Smart Tests) runs in parallel for direct runtime comparison.

---

## Demo Branches

| Branch | Version | Tests | Latency | Workflow |
|---|---|---|---|---|
| `patch-robot-demo-ptsv2` | PTSv2 (AI-based) | 451 | 500ms simulated | `tests-robot-smarttests-pts-v2.yml` |
| `patch-robot-demo-ptsv1` | PTSv1 (ML-based) | 451 | 500ms simulated | `tests-robot-smarttests-pts-v1.yml` |
| `patch-robot-demo-quick` | PTSv1 quick (40 tests, 0ms) | 40 | 0ms | `tests-robot-smarttests-pts-v1-quick.yml` |
| `patch-robot-demo-quick` | PTSv2 quick (40 tests, 0ms) | 40 | 0ms | `tests-robot-smarttests-pts-v2-quick.yml` |

Use `patch-robot-demo-quick` for fast demos and PTSv1 warm-up — 40 tests with no latency gives ~1-2 minute runs. Supports both PTSv1 and PTSv2.

---

## Quick Start

### 1. Fork and enable GitHub Actions

1. Fork this repository to your GitHub account
2. Go to **Actions** tab and enable workflows if prompted

### 2. Add your Smart Tests token as a GitHub secret

You need one token, created from the org/workspace where your version is enabled:

| Your org version | Secret name | Token source |
|---|---|---|
| PTSv2 | `PTSv2_TOKEN` | PTSv2-enabled org/workspace |
| PTSv1 | `PTSv1_TOKEN` | PTSv1-enabled org/workspace |

Go to **Settings > Secrets and variables > Actions > New repository secret**.

### 3. Run the baseline workflow

1. Go to **Actions > Robot Framework Tests (No Smart Tests - Baseline)**
2. Run workflow on your chosen branch
3. Note the runtime (~31 minutes on full branches, ~1-2 minutes on `patch-robot-demo-quick`) — this is your reference

### 4. Run Smart Tests in observation mode

1. Go to **Actions** and select the workflow matching your version
2. Run with **mode:** `observation`, **target:** `--target 75%`
3. View results at https://cloudbees.io > Smart Tests > Sessions

**PTSv1:** Repeat 5-7 times with small commits to warm up the ML model. Status will show "No subset requests" until the model has enough history — this is expected.

**PTSv2:** Predictions appear from the first run.

---

## Application

FastAPI issue tracker application (Python 3.13, SQLAlchemy, SQLite). The 500ms simulated API latency on the demo branches brings the 451-test Robot Framework suite to ~31 minutes, simulating a realistic enterprise test suite.

```bash
# Local setup
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python -m app.db.init_db && python -m app.db.seed_data
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Test users: `admin/admin123`, `john/password123`, `jane/password123`

---

## Robot Framework Tests

```bash
pip install -r requirements-robot.txt

# Run all tests
robot --outputdir test-results tests/robot/

# Run specific suite
robot --outputdir test-results tests/robot/api/

# Dry-run (enumerate tests without executing)
robot --dryrun --outputdir /tmp/robot-dryrun tests/robot/
```

Test structure:

```
tests/robot/
  api/                   # API endpoint tests
    auth_tests.robot
    projects_tests.robot
    issues_tests.robot
  data_driven/           # Data-driven edge case tests
    auth_edge_cases.robot
  resources/             # Shared keywords and variables
```

---

## CI Workflows

| Workflow | Trigger | Purpose |
|---|---|---|
| `tests-robot-smarttests-pts-v2.yml` | `patch-robot-demo-ptsv2` | PTSv2 full — 451 tests, 500ms latency |
| `tests-robot-smarttests-pts-v1.yml` | `patch-robot-demo-ptsv1` | PTSv1 full — 451 tests, 500ms latency |
| `tests-robot-smarttests-pts-v2-quick.yml` | `patch-robot-demo-quick` | PTSv2 quick — 40 tests, 0ms |
| `tests-robot-smarttests-pts-v1-quick.yml` | `patch-robot-demo-quick` | PTSv1 quick — 40 tests, 0ms |
| `tests-robot-no-smarttests.yml` | Manual / any branch | Baseline — full suite, no Smart Tests |

All four Smart Tests workflows use the same seven-step pattern:

```
smart-tests record commit
smart-tests record build
smart-tests record session  →  session.txt
robot --dryrun --outputdir /tmp/robot-dryrun  →  output.xml
smart-tests subset robot --session @session.txt ... /tmp/robot-dryrun/output.xml
eval robot ... $SUBSET_CONTENT tests/robot/
smart-tests record tests robot --session @session.txt test-results/output.xml
```

---

## Multi-Repo Testing (Recording Scenario 2)

This repository also acts as a **centralized orchestrator** for a multi-repository Smart Tests demo. The tests exercise an application that lives in a *separate* repository — [smart-tests-multi-repo-demo](https://github.com/cloudbees-ps/smart-tests-multi-repo-demo), a Book Library FastAPI app. A single workflow checks out both repositories, records commits for **both**, and records **one build tagged with both repositories' commit SHAs**. This is the CloudBees "record builds from multiple repositories" **Scenario 2** pattern (repositories built/deployed separately, then tested together).

**Use case:** teams whose application code and test assets live in different Git repositories, where a change in either repo should map to the right subset of tests and the build must be correlated to the versions of both repos.

**Multi-repo branches and workflows** (all run on the self-hosted ARC runner; Actions display names are prefixed `[Multi-Repo Scenario 2]`):

| Framework | Profile | Branch | Workflows (v1 / v2) |
|---|---|---|---|
| Playwright | raw | `patch-playwright-multi-repo-raw` | `tests-playwright-github-app-integration-oidc-multi-repo-s2-raw-v1.yml` / `-v2.yml` |
| Playwright | file | `patch-playwright-multi-repo-file` | `tests-playwright-github-app-integration-oidc-multi-repo-s2-file-v1.yml` / `-v2.yml` |
| Robot | raw | `patch-multi-repo-raw` | `tests-robot-github-app-integration-oidc-multi-repo-s2-raw-v1.yml` / `-v2.yml` |
| Robot | file | `patch-multi-repo-file` | `tests-robot-github-app-integration-oidc-multi-repo-s2-file-v1.yml` / `-v2.yml` |

The core recording pattern (per workflow):

```
smart-tests record commit --name <orchestrator> --source .              # this repo's commits
smart-tests record commit --name <app-repo> --source ./multi-repo-app   # app repo's commits
smart-tests record build --no-commit-collection \
  --commit <orchestrator>=<sha> --commit <app-repo>=<sha>               # one build, both repos tagged
```

Full walkthrough, prerequisites, and profile mechanics: [ISP_SMART_TESTS_MULTI_REPO.md](./ISP_SMART_TESTS_MULTI_REPO.md). Scenario 1 (single `record build --source`) and Scenario 3 (incremental / cached artifacts) are planned.

---

## Expected Results (Reference)

| Metric | Value |
|---|---|
| Full suite baseline | ~31 minutes (451 tests, 500ms latency) |
| Smart Tests at 75% target | ~23 minutes (~25% savings) |
| Smart Tests at 50% target | ~15 minutes (~50% savings) |
| PTSv1 warm-up runs needed | ~6 runs on `patch-robot-demo-quick` (40 tests) |
| PTSv1 first prediction (40 tests, 75%) | Subset: 30, Remainder: 10 |

---

## Additional Resources

- Adoption Journey Guide: [ISP_SMART_TESTS_ROBOT.md](./ISP_SMART_TESTS_ROBOT.md)
- Multi-Repo Guide: [ISP_SMART_TESTS_MULTI_REPO.md](./ISP_SMART_TESTS_MULTI_REPO.md)
- Application-under-test repository: https://github.com/cloudbees-ps/smart-tests-multi-repo-demo
- CloudBees Smart Tests documentation: https://docs.cloudbees.com/docs/cloudbees-smart-tests/latest/
