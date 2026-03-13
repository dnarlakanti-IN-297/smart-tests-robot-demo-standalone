# CI Demonstration Guide

This guide explains how to use the patch system to demonstrate CI/CD behavior and Smart Tests optimization.

## 🎯 Overview

The CI demo patch system allows you to simulate code changes that break tests, demonstrating:
- **Smart Tests** selecting relevant test subsets
- **CI pipelines** catching breaking changes
- **Test failure scenarios** and recovery
- **Workflow automation** with GitHub Actions

## 📁 What Was Created

### 1. Patch Files
**Location**: `patches/`

**Available patches** (can be applied independently or combined):

1. **01-require-project-description.patch** - 8 test failures
   - Makes project descriptions required (minimum 50 characters)

2. **02-require-long-issue-titles.patch** - 10 test failures
   - Requires issue titles to be minimum 20 characters

3. **03-require-long-comments.patch** - 10 test failures
   - Requires comments to be minimum 15 characters

4. **04-require-corporate-email.patch** - 7 test failures
   - Requires corporate email domains (company.com, corp.com, enterprise.com)

**Total available failures**: ~35 tests when all patches applied together

See `patches/README.md` for detailed documentation of each patch.

### 2. GitHub Actions Workflow
**Location**: `.github/workflows/apply-demo-patch.yml`

**Trigger**: Manual (workflow_dispatch)

**Inputs**:
- `action`: Choose `apply` or `revert`
- `patch_name`: Patch file name (e.g., `01-require-project-description.patch`, `02-require-long-issue-titles.patch`, etc.)

**Note**: Apply patches one at a time using the workflow, or apply multiple locally then push.

### 3. Documentation
**Location**: `patches/README.md`

Comprehensive documentation for all patches and usage instructions.

## 🚀 How to Use

### Option 1: GitHub Actions (Recommended for Demos)

1. **Create a patch branch** (first time only)
   ```bash
   git checkout -b patch-demo
   git push -u origin patch-demo
   ```

2. **Navigate to GitHub Actions**
   - Go to your repository on GitHub
   - Click the "Actions" tab
   - Select "Apply CI Demo Patch" workflow

3. **Run the Workflow**
   - Click "Run workflow" button
   - Select branch: `patch-demo` (or any branch starting with `patch-`)
   - Choose action:
     - `apply` - Introduce breaking changes
     - `revert` - Restore original state
   - Enter patch name: `01-require-project-description.patch`
   - Click "Run workflow"

4. **Watch the CI Pipeline**
   - The workflow commits and pushes the changes to the `patch-demo` branch
   - The Tests workflow runs automatically on the patch branch
   - Smart Tests will select relevant test subsets
   - Some tests will fail (intentionally)

5. **Review Results**
   - Check the Tests workflow results
   - See which tests Smart Tests selected
   - Observe failure patterns
   - Review Smart Tests analytics on CloudBees platform

6. **Restore Original State**
   - Run the workflow again with `revert` action
   - This removes the breaking changes from the patch branch
   - CI should pass again

**Note**: The workflow only runs on branches starting with `patch-*` for safety. This prevents accidentally applying demo patches to production branches like `main` or `develop`.

### Option 2: Local Manual Application

```bash
# Apply the patch
git apply patches/01-require-project-description.patch

# Run tests locally to see failures
pytest tests/unit/test_project_service.py -v
pytest tests/integration/test_projects_api.py -v

# Revert the patch
git apply -R patches/01-require-project-description.patch
```

## 🎬 Demo Script

### Scenario: Smart Tests Demo

**Setup** (5 minutes):
1. Show the current CI pipeline - all tests passing
2. Explain: "We're going to introduce a breaking change"
3. Show the patch file contents

**Apply Breaking Change** (2 minutes):
1. Navigate to Actions → "Apply CI Demo Patch"
2. Run workflow with `action: apply`
3. Show the commit being created

**Observe CI Behavior** (5-10 minutes):
1. Navigate to the triggered "Tests" workflow
2. Point out:
   - Unit & Integration Tests job running
   - E2E Tests job running
   - Smart Tests generating test subsets (50% target)
3. Show test failures in the logs
4. Explain: "Smart Tests selected relevant tests based on code changes"

**Smart Tests Analytics** (5 minutes):
1. Open CloudBees Platform
2. Show Smart Tests dashboard
3. Point out:
   - Test selection patterns
   - Time savings (50% reduction)
   - Failed tests being tracked
   - Historical data trends

**Recovery** (2 minutes):
1. Run workflow with `action: revert`
2. Show CI passing again
3. Explain: "This demonstrates the complete dev cycle"

## 📊 Expected Results

### When Patches Are Applied:

**Patch 1 (Project Descriptions)** - 8 failures:
- 2 unit tests (project service)
- 6 integration tests (project API)

**Patch 2 (Issue Titles)** - 10 failures:
- 5 unit tests (issue service)
- 5 integration tests (issue API)

**Patch 3 (Comments)** - 10 failures:
- 8 unit tests (comment service)
- 2 integration tests (comment API)

**Patch 4 (Corporate Emails)** - 7 failures:
- 3 unit tests (user service)
- 4 integration tests (auth API)

**All Patches Combined** - ~35 failures:
- Demonstrates broad impact across codebase
- Shows Smart Tests prioritizing relevant domains
- Perfect for comprehensive CI demonstrations

### Smart Tests Behavior:

- **Before patch**: Selects 50% of tests (random/historical)
- **After patch**: Prioritizes tests related to:
  - Project creation
  - Project services
  - Project API endpoints
- **Time Savings**: ~50% reduction in test execution time
- **Coverage**: Full test suite covered over multiple builds

## 🔮 Future Enhancements

The patch system is designed to be extensible:

```
patches/
├── 01-require-project-description.patch  ✅ (current)
├── 02-break-tests.patch                  📋 (planned)
├── 03-fix-tests.patch                    📋 (planned)
├── 04-refactor.patch                     📋 (planned)
└── README.md
```

**Planned patches**:
- `02-break-tests.patch`: Additional breaking changes
- `03-fix-tests.patch`: Fixes for broken tests
- `04-refactor.patch`: Code refactoring without behavior changes

This creates a timeline of changes for comprehensive CI/CD demonstrations.

## 🛡️ Safety Notes

- ⚠️  **Do not apply patches to production branches**
- ✅ Patches are safe for `main` branch (demo environment)
- 🔄 Always revert patches after demonstrations
- 📊 Patches are version-controlled and reproducible
- 🧪 All changes are intentional and documented

## 🤝 Contributing

To create a new patch:

1. Make desired code changes locally
2. Create patch: `git diff > patches/XX-patch-name.patch`
3. Revert changes: `git checkout .`
4. Update `patches/README.md` with patch details
5. Test the patch: `git apply patches/XX-patch-name.patch`
6. Commit the patch file (not the changes)

## 📚 Additional Resources

- [Smart Tests Documentation](./SMART_TESTS.md)
- [E2E Testing Guide](./E2E_TESTING.md)
- [GitHub Actions Workflows](.github/workflows/)
- [CloudBees Smart Tests](https://docs.cloudbees.com/docs/cloudbees-platform/latest/analytics/smart-tests)

---

**Questions?** Check `patches/README.md` or review the workflow file at `.github/workflows/apply-demo-patch.yml`
