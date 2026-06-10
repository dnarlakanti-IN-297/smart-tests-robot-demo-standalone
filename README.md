# Smart Tests Demo: Robot Framework — PTSv1 Branch

![Python](https://img.shields.io/badge/python-3.13+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)
![Robot Framework](https://img.shields.io/badge/Robot%20Framework-7.0+-orange.svg)
![Smart Tests](https://img.shields.io/badge/Smart%20Tests-PTSv1%20ML--based-blue.svg)

> **You are on `patch-robot-demo-ptsv1` — the PTSv1 (ML-based) demo branch.**
>
> This branch uses `smart-tests-cli==2.11.2` with a PTSv1 token. Predictions are built from historical test run data. Run the suite 5-7 times before expecting predictions to appear.

**Adoption Journey Guide:** [ISP_SMART_TESTS_ROBOT.md](./ISP_SMART_TESTS_ROBOT.md)

---

## This Branch

| Property | Value |
|---|---|
| Version | PTSv1 (ML-based) |
| Tests | 451 Robot Framework tests |
| Simulated latency | 500ms per API call |
| Baseline runtime | ~31 minutes |
| Predictions available | After ~5-7 observation runs |
| GitHub secret | `LAUNCHABLE_TOKEN` (mapped to `SMART_TESTS_TOKEN` in workflow) |
| Workflow | `tests-robot-launchable-pts-v1.yml` |

---

## Quick Start

### 1. Fork and enable GitHub Actions

1. Fork `cloudbees-ps/smart-tests-robot-demo` to your GitHub account
2. Go to **Actions** tab and enable workflows if prompted

### 2. Add your PTSv1 token as a GitHub secret

Go to **Settings > Secrets and variables > Actions > New repository secret**:

| Secret name | Value |
|---|---|
| `LAUNCHABLE_TOKEN` | Token from your PTSv1-enabled org/workspace in CloudBees Unify |

The workflow maps `LAUNCHABLE_TOKEN` → `SMART_TESTS_TOKEN` internally so the CLI reads the same variable.

### 3. Run the baseline workflow

1. Go to **Actions > Robot Framework Tests (No Smart Tests - Baseline)**
2. Run workflow on this branch
3. Note the runtime (~31 minutes) — this is your before reference

### 4. Warm up the ML model (PTSv1)

PTSv1 needs historical run data before it can make predictions. Use `patch-robot-demo-quick` (40 tests, 0ms latency) to build history faster:

1. Check out `patch-robot-demo-quick` and run `tests-robot-launchable-pts-v1.yml` in **observation** mode
2. Make a small commit (add a blank line to any source file), push, and run again
3. Repeat 5-7 times — the session view in CloudBees Unify will show "No subset requests" until the model has enough history

### 5. Run on this branch with observation mode

Once the model has history from `patch-robot-demo-quick`, run this branch:

1. Go to **Actions > Robot Framework Tests (Launchable)** (`tests-robot-launchable-pts-v1.yml`)
2. Set **mode:** `observation`, **target:** `--target 75%`
3. View predictions at https://cloudbees.io > Smart Tests > Sessions

---

## Application

FastAPI issue tracker (Python 3.13, SQLAlchemy, SQLite). The 500ms simulated API latency brings the 451-test suite to ~31 minutes, representing a realistic enterprise test suite.

```bash
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

# Dry-run (enumerate without executing)
robot --dryrun --outputdir /tmp/robot-dryrun tests/robot/
```

---

## Expected Results

| Metric | Value |
|---|---|
| Full suite baseline | ~31 minutes |
| Smart Tests at 75% target | ~23 minutes (~25% savings) |
| Smart Tests at 50% target | ~15 minutes (~50% savings) |
| Warm-up runs needed | ~6 runs on `patch-robot-demo-quick` (40 tests) |
| First prediction (40 tests, 75%) | Subset: ~30, Remainder: ~10 |

---

## Other Branches

| Branch | Version | Purpose |
|---|---|---|
| `main` | — | Stable base, docs, workflows |
| `patch-robot-demo-ptsv2` | PTSv2 (AI-based) | Full suite PTSv2 demo |
| `patch-robot-demo-quick` | PTSv1 + PTSv2 quick | 40 tests, 0ms latency for fast demo/warm-up |

---

## Additional Resources

- Adoption Journey Guide: [ISP_SMART_TESTS_ROBOT.md](./ISP_SMART_TESTS_ROBOT.md)
- CloudBees Smart Tests documentation: https://docs.cloudbees.com/docs/cloudbees-smart-tests/latest/
