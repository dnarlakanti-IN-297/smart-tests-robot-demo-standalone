# Smart Tests Demo: Robot Framework — Quick Branch

![Python](https://img.shields.io/badge/python-3.13+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)
![Robot Framework](https://img.shields.io/badge/Robot%20Framework-7.0+-orange.svg)
![Smart Tests](https://img.shields.io/badge/Smart%20Tests-PTSv1%20%7C%20PTSv2%20Quick-brightgreen.svg)

> **You are on `patch-robot-demo-quick` — fast demo for both PTSv1 and PTSv2.**
>
> 40 tests, 0ms latency, ~1-2 minute runs. Use this branch to demo either version quickly, or to warm up the PTSv1 ML model before switching to the full 451-test branch.

**Adoption Journey Guide:** [ISP_SMART_TESTS_ROBOT.md](./ISP_SMART_TESTS_ROBOT.md)

---

## This Branch

| Property | PTSv1 | PTSv2 |
|---|---|---|
| Tests | 40 (`auth_edge_cases.robot`) | 40 (`auth_edge_cases.robot`) |
| Simulated latency | 0ms | 0ms |
| Run time | ~1-2 minutes | ~1-2 minutes |
| GitHub secret | `LAUNCHABLE_TOKEN` | `SMART_TESTS_TOKEN` |
| Workflow | `tests-robot-launchable-pts-v1.yml` | `tests-robot-smarttests-pts-v2-quick.yml` |
| Predictions | After ~5-7 runs | From first run |

---

## Quick Start

### 1. Fork and enable GitHub Actions

1. Fork `cloudbees-ps/smart-tests-robot-demo` to your GitHub account
2. Go to **Actions** tab and enable workflows if prompted

### 2. Add your token as a GitHub secret

Add only the secret that matches your org's enabled version:

| Secret name | Value | For version |
|---|---|---|
| `SMART_TESTS_TOKEN` | Token from your PTSv2-enabled org/workspace | PTSv2 |
| `LAUNCHABLE_TOKEN` | Token from your PTSv1-enabled org/workspace | PTSv1 |

### 3. Run the appropriate workflow

**PTSv2:**
1. Go to **Actions > Robot Framework Tests PTSv2 (Quick)**
2. Set **mode:** `observation`, **target:** `--target 75%`
3. Predictions appear from the first run

**PTSv1:**
1. Go to **Actions > Robot Framework Tests (Launchable)**
2. Set **mode:** `observation`, **target:** `--target 75%`
3. Make a small commit, push, repeat 5-7 times until predictions appear

### 4. Move to the full demo branch (when ready)

Once you have seen predictions, switch to the full 451-test branch for the complete demo:

| Version | Full demo branch |
|---|---|
| PTSv2 | `patch-robot-demo-ptsv2` |
| PTSv1 | `patch-robot-demo-ptsv1` |

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

## Expected Results

| Metric | Value |
|---|---|
| PTSv1 warm-up runs needed | ~6 runs on this branch |
| PTSv1 first prediction (40 tests, 75%) | Subset: ~30, Remainder: ~10 |
| PTSv2 first prediction | Available immediately |
| Full suite (451 tests) at 75% after warm-up | ~23 minutes (~25% savings from ~31 min baseline) |

---

## Other Branches

| Branch | Version | Purpose |
|---|---|---|
| `main` | — | Stable base, docs, workflows |
| `patch-robot-demo-ptsv2` | PTSv2 (AI-based) | Full 451-test PTSv2 demo |
| `patch-robot-demo-ptsv1` | PTSv1 (ML-based) | Full 451-test PTSv1 demo |

---

## Additional Resources

- Adoption Journey Guide: [ISP_SMART_TESTS_ROBOT.md](./ISP_SMART_TESTS_ROBOT.md)
- CloudBees Smart Tests documentation: https://docs.cloudbees.com/docs/cloudbees-smart-tests/latest/
