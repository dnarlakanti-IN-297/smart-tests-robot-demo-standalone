# Smart Tests Demo: Robot Framework — PTSv1 Quick Warm-up Branch

![Python](https://img.shields.io/badge/python-3.13+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)
![Robot Framework](https://img.shields.io/badge/Robot%20Framework-7.0+-orange.svg)
![Smart Tests](https://img.shields.io/badge/Smart%20Tests-PTSv1%20Warm--up-blue.svg)

> **You are on `patch-launchable-quick` — the PTSv1 ML model warm-up branch.**
>
> This branch has 40 tests and 0ms API latency. Use it to build the PTSv1 prediction history quickly before switching to the full 451-test branch.

**Adoption Journey Guide:** [ISP_SMART_TESTS_ROBOT.md](./ISP_SMART_TESTS_ROBOT.md)

---

## This Branch

| Property | Value |
|---|---|
| Version | PTSv1 (ML-based) |
| Tests | 40 Robot Framework tests |
| Simulated latency | 0ms |
| Run time | ~1-2 minutes |
| Purpose | Build PTSv1 prediction history fast |
| GitHub secret | `LAUNCHABLE_TOKEN` (mapped to `SMART_TESTS_TOKEN` in workflow) |
| Workflow | `tests-robot-launchable-pts-v1.yml` |

---

## Why This Branch Exists

PTSv1 needs historical test run data before it can make predictions. Running all 451 tests with 500ms latency (~31 min per run) 5-7 times to warm up the model would take hours. This branch reduces that to ~1-2 minutes per run by using 40 tests with no simulated latency.

**Warm-up strategy:**

1. Run `tests-robot-launchable-pts-v1.yml` on this branch in observation mode
2. Make a small commit (add a blank line to any source file, e.g. `app/main.py`), push, run again
3. Repeat 5-7 times — the session view in CloudBees Unify will show "No subset requests" until the model has enough history
4. Once predictions appear, switch to `patch-robot-demo-v1-launchable` for the full 451-test demo

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

### 3. Run in observation mode and iterate

1. Go to **Actions > Robot Framework Tests (Launchable)** (`tests-robot-launchable-pts-v1.yml`)
2. Set **mode:** `observation`, **target:** `--target 75%`
3. View sessions at https://cloudbees.io > Smart Tests > Sessions
4. Make a small commit, push to `patch-launchable-quick`, run again
5. Repeat until predictions appear (~6 runs)

### 4. Move to the full demo branch

Once predictions are working, run the full 451-test suite on `patch-robot-demo-v1-launchable` to demonstrate real time savings.

---

## Application

FastAPI issue tracker (Python 3.13, SQLAlchemy, SQLite). No simulated latency on this branch — tests run at full speed.

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

# Run all tests (40 on this branch)
robot --outputdir test-results tests/robot/

# Dry-run (enumerate without executing)
robot --dryrun --outputdir /tmp/robot-dryrun tests/robot/
```

---

## Expected Results After Warm-up

| Metric | Value |
|---|---|
| Warm-up runs needed | ~6 runs on this branch |
| First prediction (40 tests, 75%) | Subset: ~30, Remainder: ~10 |
| Full suite (451 tests) at 75% | ~23 minutes (~25% savings from ~31 min baseline) |

---

## Other Branches

| Branch | Version | Purpose |
|---|---|---|
| `main` | — | Stable base, docs, workflows |
| `patch-robot-demo` | PTSv2 (AI-based) | Full 451-test PTSv2 demo (no warm-up needed) |
| `patch-robot-demo-v1-launchable` | PTSv1 (ML-based) | Full 451-test PTSv1 demo (use this after warm-up) |

---

## Additional Resources

- Adoption Journey Guide: [ISP_SMART_TESTS_ROBOT.md](./ISP_SMART_TESTS_ROBOT.md)
- CloudBees Smart Tests documentation: https://docs.cloudbees.com/docs/cloudbees-smart-tests/latest/
