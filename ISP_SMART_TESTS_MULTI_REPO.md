# Smart Tests Across Multiple Repositories

| | |
|---|---|
| **Author(s)** | PS Team (Anudeep) |
| **Team** | PS |
| **Date** | 2026-07-10 |
| **PS Official** | Pending |
| **ENG Approval** | Pending |

---

> **Important — read the single-repo guide first**
>
> This guide assumes you already understand the Smart Tests basics from [ISP_SMART_TESTS_ROBOT.md](./ISP_SMART_TESTS_ROBOT.md): PTSv1 vs PTSv2, observation vs production mode, the `smart-tests` CLI, GitHub OIDC auth, and the subset profiles (robot / file / raw). This guide covers only what is *different* when the tests and the application under test live in **separate repositories**.
>
> Multi-repo docs: https://docs.cloudbees.com/docs/cloudbees-smart-tests/latest/send-data-to-smart-tests/record-builds/record-builds-from-multiple-repositories

---

## Overview

Smart Tests predicts which tests to run based on your code changes. When your tests and the code they exercise live in the **same** repository, a single `git diff` tells the prediction engine everything it needs. But many teams keep the application in one repository and its test assets (or a shared test harness) in another. A change in *either* repository should map to the right subset of tests, and the build must be correlated to the versions of *both* repositories.

This is what CloudBees calls **recording builds from multiple repositories**. This demo implements it with two repositories:

| Repository | Role | Contains |
|---|---|---|
| `smart-tests-robot-demo` | **Centralized orchestrator** | The GitHub Actions workflows that drive the multi-repo runs. Runs no application of its own in these workflows. |
| `smart-tests-multi-repo-demo` | **Application under test** | The Book Library FastAPI app and its Playwright and Robot Framework test suites. |

A workflow in the orchestrator repo checks out **both** repositories, records the commits of **both**, records **one build tagged with both repositories' commit SHAs**, then runs the Book Library tests and records the results. Smart Tests can now attribute a change in either repository to that build.

**Demonstration repositories:**
- Orchestrator: https://github.com/cloudbees-ps/smart-tests-robot-demo
- Application under test: https://github.com/cloudbees-ps/smart-tests-multi-repo-demo

### By the end of this guide, you will:

- Understand when a multi-repo Smart Tests setup is needed and when it is not
- Know the difference between *recording a repository's commits* and *tagging a build with a commit*
- Understand the three CloudBees "record builds from multiple repositories" scenarios and which one this demo implements
- Know the centralized-orchestration integration pattern: dual checkout, dual `record commit`, one multi-repo `record build`
- Know which workflow and branch to run for each framework/profile/version combination

**Target audience:** Teams whose application code and test assets live in different Git repositories.

---

## Use Case: When Multi-Repo Helps

| Situation | Why multi-repo recording matters |
|---|---|
| Tests live in a separate repo from the app | A change in the app repo must still map to tests defined elsewhere. The build must reference both so the prediction engine sees both change histories. |
| A shared/centralized test harness tests several apps | One orchestration repo runs suites against many app repos. Each build ties the harness version to the specific app version tested. |
| Microservices tested together in one environment | Services are built and deployed from different repos, then tested together. The build captures the exact commit of each service under test. |
| Monorepo split into app + infrastructure repos | Coverage and impact analysis need the versions of both repos that produced the deployed artifact. |

> **Note — when you do NOT need this:** If your tests and the code they exercise live in the same repository, use the single-repo flow in [ISP_SMART_TESTS_ROBOT.md](./ISP_SMART_TESTS_ROBOT.md). Multi-repo recording adds a second checkout and a second `record commit`; only take on that overhead when the code and tests are genuinely split.

---

## Recording Builds from Multiple Repositories

The CloudBees documentation describes three scenarios. The key idea underneath all of them:

> `record commit` **sends** a repository's commit graph to Smart Tests. `record build --commit REPO=SHA` only **tags** the build with a commit reference; it does not send commits. The `--no-commit-collection` flag tells `record build` not to collect commits because you are recording them separately.

| Doc scenario | Approach | This demo |
|---|---|---|
| **1. Combined in one build, then tested** | One call: `record build --source repoA=path --source repoB=path` collects commits and records the build together | Planned (see below) |
| **2. Built/deployed separately, then tested together (microservices)** | `record commit` per repo, then `record build --no-commit-collection --commit repo=sha ...` | **Implemented** |
| **3. Incremental build over multiple repos** | `record commit` for changed/cloned repos only, then `record build --no-commit-collection --commit ...` for all repos (unchanged ones tagged by SHA from cache) | Planned (see below) |

### Scenario 2 (implemented)

Every centralized workflow in this demo follows Scenario 2. In one workflow run:

1. Check out both repositories (orchestrator at the workspace root, application into `multi-repo-app/`).
2. `record commit` for **each** repository (both are present in this run).
3. `record build --no-commit-collection --commit <orchestrator>=<sha> --commit <app>=<sha>` to tag the build with both commits.
4. Subset, run the Book Library tests, and record results using the chosen profile.

```bash
# 2. Record commits for BOTH repositories
smart-tests record commit --name ${{ github.repository }} --source ${{ github.workspace }} --max-days 90
smart-tests record commit --name anuddeeph2/smart-tests-multi-repo-demo --source ${{ github.workspace }}/multi-repo-app --max-days 90

# 3. Record ONE build tagged with both repositories' commits
smart-tests record build --build ${{ github.run_id }} \
  --no-commit-collection \
  --commit ${{ github.repository }}=${{ github.sha }} \
  --commit anuddeeph2/smart-tests-multi-repo-demo=${{ steps.multi-repo-sha.outputs.sha }}
```

> **Warning — the `--name` on `record commit` must match the `--commit` tag on `record build`.** Smart Tests correlates the tagged SHA to the recorded commit graph by repository name. If the names differ, the build points at a commit Smart Tests does not recognize and multi-repo impact analysis degrades silently.

> **Note — why record commits for both here:** With `--no-commit-collection`, `record build` sends no commits. If only the orchestrator's commits are recorded, the app repo's commit tag resolves to nothing (unless the app repo recorded that SHA in a separate pipeline). Because this workflow checks out both repos and tests immediately, it records both repos' commits in the same run — no cross-repo ordering dependency.

### Scenario 1 (planned)

Because these workflows already check out both repositories together, they are also a natural fit for Scenario 1, which collapses the two steps into a single call:

```bash
smart-tests record build --build ${{ github.run_id }} \
  --source ${{ github.repository }}=${{ github.workspace }} \
  --source anuddeeph2/smart-tests-multi-repo-demo=${{ github.workspace }}/multi-repo-app
```

No separate `record commit`, no `--no-commit-collection`, no `--commit` tags — `record build --source` collects the commits and records the build in one shot. This variant is planned as a separate demo.

### Scenario 3 (planned)

Scenario 3 covers incremental builds where only changed repositories are cloned and the rest are referenced by SHA from cache. Its distinguishing trait: **more `--commit` tags than `record commit` calls** (unchanged repos are tagged by hash without a local `record commit`). Demonstrating it cleanly requires a third repository that is tagged by SHA but not cloned in a given run. This variant is planned as a separate demo.

---

## The Centralized Multi-Repo Workflows

All eight workflows live in `smart-tests-robot-demo`, run on the self-hosted ARC runner (`runner-robot-demo`), and use GitHub OIDC auth. They cover both test frameworks, both subset profiles, and both PTS versions. Each triggers on push to its own branch.

| Framework | Profile | PTS | Workflow file | Branch |
|---|---|---|---|---|
| Playwright | raw | v1 | `tests-playwright-github-app-integration-oidc-multi-repo-raw-v1.yml` | `patch-playwright-multi-repo-raw` |
| Playwright | raw | v2 | `tests-playwright-github-app-integration-oidc-multi-repo-raw-v2.yml` | `patch-playwright-multi-repo-raw` |
| Playwright | file | v1 | `tests-playwright-github-app-integration-oidc-multi-repo-file-v1.yml` | `patch-playwright-multi-repo-file` |
| Playwright | file | v2 | `tests-playwright-github-app-integration-oidc-multi-repo-file-v2.yml` | `patch-playwright-multi-repo-file` |
| Robot | raw | v1 | `tests-robot-github-app-integration-oidc-multi-repo-raw-v1.yml` | `patch-multi-repo-raw` |
| Robot | raw | v2 | `tests-robot-github-app-integration-oidc-multi-repo-raw-v2.yml` | `patch-multi-repo-raw` |
| Robot | file | v1 | `tests-robot-github-app-integration-oidc-multi-repo-file-v1.yml` | `patch-multi-repo-file` |
| Robot | file | v2 | `tests-robot-github-app-integration-oidc-multi-repo-file-v2.yml` | `patch-multi-repo-file` |

Their Actions display names are prefixed `[Multi-Repo Scenario 2]` to mark that they implement the recording Scenario 2 pattern (distinct from the demo's own orchestration labels).

> **Important — one workspace per profile type.** Smart Tests locks a workspace to the first profile type (`robot`, `file`, or `raw`) it receives; mixing profiles in one workspace returns `422` errors. Each workflow therefore targets its own workspace variable (for example `SMART_TESTS_WORKSPACE_V1_PLAYWRIGHT_RAW`, `SMART_TESTS_WORKSPACE_V1_PLAYWRIGHT_FILE`, `SMART_TESTS_WORKSPACE_V1_RAW_MULTI_REPO`, `SMART_TESTS_WORKSPACE_V1_MULTI_REPO`). Provision a separate workspace per framework/profile/version combination you intend to run.

---

## How the Integration Works

The multi-repo workflows reuse the subset profile mechanics documented in [ISP_SMART_TESTS_ROBOT.md](./ISP_SMART_TESTS_ROBOT.md) (robot / file / raw). Only the setup around them changes.

### 1. Dual checkout

```yaml
- name: Checkout smart-tests-robot-demo        # orchestrator, at workspace root
  uses: actions/checkout@v4
  with:
    fetch-depth: 0

- name: Checkout smart-tests-multi-repo-demo   # application under test, into multi-repo-app/
  uses: actions/checkout@v4
  with:
    repository: anuddeeph2/smart-tests-multi-repo-demo
    ref: <branch or SHA>
    token: ${{ secrets.MULTI_REPO_PAT }}
    path: multi-repo-app
    fetch-depth: 0

- name: Get smart-tests-multi-repo-demo commit SHA
  id: multi-repo-sha
  run: echo "sha=$(git -C multi-repo-app rev-parse HEAD)" >> $GITHUB_OUTPUT
```

> **Note — why a PAT is needed for the second checkout:** `github.token` only grants access to the repository running the workflow. Checking out a second private repository (even in the same account) requires a Personal Access Token with `repo` scope, stored as the `MULTI_REPO_PAT` secret. Once both demo repositories are public, this requirement goes away.

### 2. Record commits for both repositories

See the Scenario 2 code block above. `--source ${{ github.workspace }}` records the orchestrator; `--source ${{ github.workspace }}/multi-repo-app` records the application repo.

### 3. Record one multi-repo build

One `record build` call with `--no-commit-collection` and two `--commit repo=sha` tags (see above). The application SHA comes from the `multi-repo-sha` step so the tag matches the exact version checked out.

### 4. Subset, run, and record (per profile)

From here the flow is identical to the single-repo profile flows in [ISP_SMART_TESTS_ROBOT.md](./ISP_SMART_TESTS_ROBOT.md), except the tests come from `multi-repo-app/`:

- **raw profile:** generate testPath list from the app's tests, `subset raw`, run the subset, record `raw-results.json` with `record tests raw`.
- **file profile:** pipe the app's `.robot` (or Playwright spec) files into `subset file`, run the subset, record with `record tests file`.

The Book Library app is started (`uvicorn app.main:app`) and seeded (`python -m app.db.init_db && python -m app.db.seed_data`) from `multi-repo-app/` before its tests run.

---

## Prerequisites

In addition to the single-repo prerequisites in [ISP_SMART_TESTS_ROBOT.md](./ISP_SMART_TESTS_ROBOT.md):

| Requirement | Notes |
|---|---|
| **Both repositories forked** | Fork `smart-tests-robot-demo` (orchestrator) and `smart-tests-multi-repo-demo` (app under test) into the same account |
| **`MULTI_REPO_PAT` secret** | PAT with `repo` scope, added to the orchestrator repo, so it can check out the (private) app repo. Not needed once both repos are public. |
| **OIDC repository variables** | `SMART_TESTS_ORGANIZATION_v1` / `_v2` plus a distinct `SMART_TESTS_WORKSPACE_*` variable per framework/profile/version (UUID values) |
| **One workspace per profile type** | Provision separate workspaces so `robot` / `file` / `raw` results never mix in one workspace (avoids `422`) |
| **OIDC enabled for each workspace** | Backend enablement by the CloudBees Smart Tests team; workflows return `401` until active |

---

## Running the Demo

1. Fork both repositories into the same account and enable GitHub Actions on the orchestrator fork.
2. Add the `MULTI_REPO_PAT` secret and the OIDC repository variables (organization + per-profile workspace UUIDs).
3. In the orchestrator repo's **Actions** tab, pick the workflow for your framework/profile/version (see the table above).
4. Click **Run workflow**, select the matching branch, and set the inputs:
   - **mode:** `observation` (all tests run; savings projected) or `production` (only the subset runs; savings realized)
   - **optimization_target_type / _value:** e.g. `target` / `75%`
5. After the run, open **Smart Tests > Builds** in CloudBees Unify. The build shows **two repositories** and a test session. Confirm the session recorded results and that the Predictive Test Selection panel correlates the subset with the recorded results.

> **Note — PTSv1 warm-up still applies.** For PTSv1 multi-repo workflows, the ML model needs several observation runs before it returns a real subset; until then the workflow runs all tests. PTSv2 predicts from the first run. This is identical to the single-repo behavior.

---

## Knowledge Check: Multi-Repo

1. **Does `record build --no-commit-collection --commit repoA=sha --commit repoB=sha` send both repositories' commits to Smart Tests?**
   - [ ] Yes — it sends both
   - [x] No — it only *tags* the build with the two SHAs; the commits must be sent separately by `record commit`
   - [ ] It sends only the first repository's commits
   - [ ] Only in production mode

2. **In this demo, where are the commits of the application repo (`smart-tests-multi-repo-demo`) recorded?**
   - [ ] Only in the application repo's own pipeline
   - [x] By a second `record commit --source .../multi-repo-app` in the same centralized workflow run
   - [ ] They are not recorded, only tagged
   - [ ] By `record build --source`

3. **Which recording scenario does this demo implement?**
   - [ ] Scenario 1 — combined in one build, then tested
   - [x] Scenario 2 — built/deployed separately, then tested together
   - [ ] Scenario 3 — incremental over multiple repos
   - [ ] None — it uses single-repo recording

4. **Why does each framework/profile/version target its own workspace?**
   - [ ] To parallelize runs
   - [x] Smart Tests locks a workspace to the first profile type it receives; mixing `robot` / `file` / `raw` in one workspace returns `422`
   - [ ] To use different tokens
   - [ ] It is optional

---

## Additional Resources

- Single-repo guide: [ISP_SMART_TESTS_ROBOT.md](./ISP_SMART_TESTS_ROBOT.md)
- Orchestrator repository: https://github.com/cloudbees-ps/smart-tests-robot-demo
- Application-under-test repository: https://github.com/cloudbees-ps/smart-tests-multi-repo-demo
- CloudBees "record builds from multiple repositories": https://docs.cloudbees.com/docs/cloudbees-smart-tests/latest/send-data-to-smart-tests/record-builds/record-builds-from-multiple-repositories
- CloudBees Smart Tests documentation: https://docs.cloudbees.com/docs/cloudbees-smart-tests/latest/
- GitHub OIDC migration guide: https://docs.cloudbees.com/docs/cloudbees-smart-tests/latest/send-data-to-smart-tests/set-up-smart-tests/migration-to-github-oidc-auth
