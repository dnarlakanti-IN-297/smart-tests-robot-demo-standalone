# Smart Tests Demo: Robot Framework

![Python](https://img.shields.io/badge/python-3.13+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)
![Robot Framework](https://img.shields.io/badge/Robot%20Framework-7.0+-orange.svg)
![Smart Tests](https://img.shields.io/badge/Smart%20Tests-PTSv1%20%7C%20PTSv2-brightgreen.svg)

Demo repository for **CloudBees Smart Tests** predictive test selection with Robot Framework. Uses `smart-tests-cli==2.11.2` for both PTSv1 (ML-based) and PTSv2 (AI-based) — the CLI is identical for both versions; the token determines which prediction engine runs.

**Adoption Journey Guide:** [ISP_SMART_TESTS_ROBOT.md](./ISP_SMART_TESTS_ROBOT.md)

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
| `patch-robot-demo-quick` | PTSv1 quick debug | 40 | 0ms | `tests-robot-smarttests-pts-v1.yml` |

Use `patch-robot-demo-quick` during initial PTSv1 setup — 40 tests with no latency gives fast feedback while warming up the ML model.

---

## Quick Start

### 1. Fork and enable GitHub Actions

1. Fork this repository to your GitHub account
2. Go to **Actions** tab and enable workflows if prompted

### 2. Add your Smart Tests token as a GitHub secret

You need one token, created from the org/workspace where your version is enabled:

| Your org version | Secret name | Token source |
|---|---|---|
| PTSv2 | `SMART_TESTS_TOKEN` | PTSv2-enabled org/workspace |
| PTSv1 | `SMART_TESTS_TOKEN` | PTSv1-enabled org/workspace |

Go to **Settings > Secrets and variables > Actions > New repository secret**.

### 3. Run the baseline workflow

1. Go to **Actions > Robot Framework Tests (No Smart Tests - Baseline)**
2. Run workflow on your chosen branch
3. Note the runtime (~31 minutes) — this is your reference

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
| `tests-robot-smarttests-pts-v2.yml` | `patch-robot-demo-ptsv2` | PTSv2 Smart Tests — 451 tests, 500ms latency |
| `tests-robot-smarttests-pts-v2-quick.yml` | `patch-robot-demo-quick` | PTSv2 Smart Tests — 40 tests, 0ms latency |
| `tests-robot-smarttests-pts-v1.yml` | `patch-robot-demo-ptsv1`, `patch-robot-demo-quick` | PTSv1 Smart Tests integration |
| `tests-robot-no-smarttests.yml` | Manual / any branch | Baseline — full suite, no Smart Tests |

Both Smart Tests workflows use the same seven-step pattern:

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
- CloudBees Smart Tests documentation: https://docs.cloudbees.com/docs/cloudbees-smart-tests/latest/
