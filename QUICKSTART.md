# Smart Tests Quickstart Guide

This guide walks you through running the Issue Tracker application with Smart Tests predictive test selection. You'll see how Smart Tests intelligently selects which tests to run based on code changes.

## What You'll Learn

By the end of this guide, you will:
- ✅ Understand how Smart Tests uses AI to predict which tests are affected by code changes
- ✅ See how much time Smart Tests could save while maintaining code quality
- ✅ Experience a realistic CI/CD workflow with breaking changes and test failures
- ✅ Learn to interpret Smart Tests predictions and accuracy metrics
- ✅ Compare full test runs vs. intelligent test subset predictions

**⏱️ Estimated Time:** 15-20 minutes

## The Journey

```
📋 Setup (one-time)        🧪 Demo Workflow              📊 Analysis
├─ Fork repo              ├─ Run baseline tests        ├─ View predictions
├─ Enable Actions         ├─ Create patch branch       ├─ Compare results
└─ Add Smart Tests token  ├─ Apply breaking changes    └─ Understand savings
                          └─ Run tests again
```

## How This Demo Works


**This Demo's Approach:**
1. **Baseline Run** - Establishes a clean state with all tests passing
2. **Code Changes** - Applies patches that simulate new features with bugs (e.g., stricter validation rules)
3. **Smart Prediction** - Smart Tests creates a predicted test subset but still runs all tests
4. **Validation** - Compare what the subset would have caught vs. actual failures to measure prediction accuracy

This demo uses 4 independent patches that break different parts of the codebase, letting you see how Smart Tests handles various change scenarios.

## Key Concepts

Before starting, familiarize yourself with these terms:

| Term | Definition |
|------|------------|
| **Predictive Test Selection** | AI-powered technique that selects a subset of tests likely to be affected by code changes |
| **Observation Mode** | Mode where Smart Tests creates predicted test subsets but runs all tests anyway, allowing you to validate prediction accuracy in the UI |
| **Test Session** | A single execution of your test suite, recorded by Smart Tests for analysis |
| **Patch** | A file containing code changes that can be applied to simulate feature development |
| **Baseline** | The initial test run with all tests passing, used as a reference point |

## Prerequisites

- GitHub account
- CloudBees account (free tier available at [cloudbees.io](https://cloudbees.io))

> **⚠️ IMPORTANT: PTSv2 Requirement**
>
> Your CloudBees organization or sub-organization **must have PTSv2 (Predictive Test Selection v2) enabled** for Smart Tests to run predictive test selection.
>
> **Not sure if PTSv2 is enabled?**
> Send a Slack message to the **#team-smart-tests-se** channel with your organization or sub-organization ID to verify or request enablement.
>
> Without PTSv2 enabled, the workflows will run but Smart Tests will not generate predictive test subsets.

---

## Phase 1: Setup (One-Time Configuration)

### 1. Fork the Repository

Fork this repository to your GitHub account using the "Fork" button at the top right.

### 2. Enable GitHub Actions

1. Go to your forked repository
2. Click on the **Actions** tab
3. Click **"I understand my workflows, go ahead and enable them"** if prompted

### 3. Configure Smart Tests Token

#### Get your CloudBees API token:

1. Log in to [cloudbees.io](https://cloudbees.io)
2. Navigate to **Smart Tests** → **Settings**
3. Create a **Workspace API Key**
4. Copy the generated token

#### Add token to GitHub:

1. Go to your forked repository settings
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"**
4. Name: `SMART_TESTS_TOKEN`
5. Value: Paste your CloudBees API token
6. Click **"Add secret"**

---

## Phase 2: Running the Demo

### Step 1: Establish Baseline (All Tests Passing)

1. Go to **Actions** tab in your repository
2. Select **"Tests"** workflow from the left sidebar
3. Click **"Run workflow"** → Select branch `main` → Click **"Run workflow"**
4. Wait for the workflow to complete (should be green ✅)

> **What just happened?** You ran the full test suite (unit, integration, and E2E tests) with Smart Tests in observation mode. Smart Tests recorded this baseline run—all tests passed, establishing a clean reference state for future comparisons.

### Step 2: View Results in Smart Tests

1. Switch back to [cloudbees.io](https://cloudbees.io)
2. Navigate to **Predictive Test Selection** → **Observation Mode**
3. You should see your test session with all tests passing
   - Unit tests: All passed
   - Integration tests: All passed
   - E2E tests: All passed

> **What just happened?** Smart Tests recorded your baseline test session in its dashboard. You can see all tests passed successfully. This baseline provides a reference point—when you introduce changes later, you'll be able to compare whether Smart Tests would have predicted the failures correctly.

### Step 3: Create a Patch Branch

1. Go to **Code** tab in your repository
2. Click the branch dropdown (shows "main")
3. Type `patch-demo` in the text field
4. Click **"Create branch: patch-demo from main"**

> **Note**: Patches can only be applied to branches starting with `patch-*` to keep main clean for repeatability.

### Step 4: Apply a Demo Patch

1. Go to **Actions** tab
2. Select **"Apply CI Demo Patch"** workflow
3. Click **"Run workflow"**
4. Configure the workflow:
   - **Branch**: Select `patch-demo` (or your `patch-*` branch)
   - **action**: Select `apply`
   - **patch_name**: Choose one of:
     - `01-require-project-description.patch` - Makes project descriptions required (50+ chars)
     - `02-require-long-issue-titles.patch` - Requires issue titles 20+ characters
     - `03-require-long-comments.patch` - Requires comments 15+ characters
     - `04-require-corporate-email.patch` - Requires corporate email domains
5. Click **"Run workflow"**
6. Wait for completion (workflow commits changes to your patch branch)

> **What just happened?** The patch simulates a developer introducing new features (e.g., stricter validation rules) that accidentally break some existing tests.

### Step 5: Run Tests with Breaking Changes

1. Go to **Actions** → **"Tests"** workflow
2. Click **"Run workflow"**
3. Select your `patch-demo` branch
4. Click **"Run workflow"**
5. Wait for completion (some tests will fail ❌)

> **What just happened?** Smart Tests analyzed the code changes in your patch (git diff) and created a predicted test subset. However, in observation mode, it still ran all tests (not just the subset). The failing tests show that the new validation rules broke existing functionality. In the next step, you'll see whether Smart Tests' predicted subset would have caught these failures!

### Step 6: Analyze Smart Tests Predictions

1. Return to [cloudbees.io](https://cloudbees.io)
2. Go to **Predictive Test Selection** → **Observation Mode**
3. Find your latest test session (from the patch branch)
4. **Key observations**:
   - See which tests failed
   - Check if Smart Tests would have predicted these failures based on code changes
   - Compare full test run vs. predicted test subset
   - View time savings from predictive selection

> **What just happened?** This is where the magic happens! In observation mode, Smart Tests ran all tests but also shows you what would have happened if only the predicted subset ran. You can compare:
> - **What actually ran**: All tests (because you're in observation mode)
> - **What Smart Tests predicted**: The subset it would have selected (usually much smaller)
> - **Accuracy**: Whether the predicted subset included the tests that actually failed
> - **Time saved**: The difference in execution time between full suite and predicted subset
>
> High accuracy with significant time savings demonstrates Smart Tests' value—you could have caught these bugs faster with less compute time if you were using the predictions in production.

### Step 7: Continue Experimenting

You can apply additional patches to see more scenarios:

1. Run **"Apply CI Demo Patch"** again on your `patch-*` branch
2. Choose a different patch file
3. Run **"Tests"** workflow again
4. Check Smart Tests predictions in CloudBees.io

**Available patch scenarios:**
- **Project validation** (patch 01): Breaks 8 tests
- **Issue validation** (patch 02): Breaks ~10 tests
- **Comment validation** (patch 03): Breaks ~10 tests
- **Email validation** (patch 04): Breaks ~7 tests

> **Tip**: You can apply multiple patches together for a more comprehensive demo (~35 total failures).

---

## Phase 3: Analysis & Next Steps

### Resetting the Demo

To start fresh with a new experiment:

1. Create a new patch branch (e.g., `patch-demo-2`)
2. Apply patches to the new branch
3. Run tests
4. The `main` branch remains clean and ready for new demos

### Understanding the Results

#### In GitHub Actions:
- **Green ✅**: All tests passed
- **Red ❌**: Some tests failed
- **Observation mode behavior**: All tests run (Smart Tests creates predictions but doesn't skip any tests)

#### In CloudBees Smart Tests:
- **Observation Mode**: Shows that all tests actually ran
- **Predicted Subset**: Shows which tests Smart Tests would have selected if predictions were active
- **Accuracy**: Whether the predicted subset included all the tests that actually failed
- **Time Savings**: How much time the predicted subset would have saved compared to running all tests

---

## Troubleshooting

### Workflow not triggering?
- Ensure GitHub Actions are enabled in your fork
- Check that you're running on a `patch-*` branch for Apply CI Demo Patch

### No results in CloudBees?
- Verify `SMART_TESTS_TOKEN` secret is set correctly
- Check workflow logs for Smart Tests CLI output
- Ensure your CloudBees account is active
- **Verify PTSv2 is enabled**: Send your organization/sub-organization ID to #team-smart-tests-se Slack channel

### Smart Tests not generating predictions?
- Check that PTSv2 (Predictive Test Selection v2) is enabled for your CloudBees organization
- Contact #team-smart-tests-se on Slack with your organization ID to verify enablement
- Workflows will run successfully but won't generate test subsets without PTSv2

### Patches failing to apply?
- Ensure you're using a branch starting with `patch-`
- Try creating a fresh branch from `main`
- Check that patches haven't already been applied

---

## Learn More

- **[SMART_TESTS.md](./SMART_TESTS.md)** - Deep dive into Smart Tests integration
- **[CI_DEMO_GUIDE.md](./CI_DEMO_GUIDE.md)** - Detailed CI/CD demonstration guide
- **[patches/README.md](./patches/README.md)** - Complete patch documentation
- **[CloudBees Smart Tests Docs](https://docs.cloudbees.com/docs/cloudbees-platform/latest/analytics/smart-testing)** - Official Smart Tests documentation
