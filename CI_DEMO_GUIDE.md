# CI Demonstration Guide

This guide explains how to use the patch system to demonstrate CI/CD behavior and Smart Tests optimization.

## 🎯 Overview

The CI demo patch system allows you to simulate code changes that break tests, demonstrating:
- **Smart Tests** selecting relevant test subsets
- **CI pipelines** catching breaking changes
- **Test failure scenarios** and recovery
- **Workflow automation** with GitHub Actions

## 📁 What Was Created

### 1. Patch File
**Location**: `patches/01-require-project-description.patch`

**Changes**: Makes project descriptions required (minimum 10 characters)
- Model: `description = Column(Text, nullable=False)`
- Schema: `description: str = Field(..., min_length=10, max_length=500)`
- Service: Adds validation to enforce description requirement

**Expected Test Failures**: ~5-10 tests that create projects without descriptions

### 2. GitHub Actions Workflow
**Location**: `.github/workflows/apply-demo-patch.yml`

**Trigger**: Manual (workflow_dispatch)

**Inputs**:
- `action`: Choose `apply` or `revert`
- `patch_name`: Patch file name (default: `01-require-project-description.patch`)

### 3. Documentation
**Location**: `patches/README.md`

Comprehensive documentation for all patches and usage instructions.

## 🚀 How to Use

### Option 1: GitHub Actions (Recommended for Demos)

1. **Navigate to GitHub Actions**
   - Go to your repository on GitHub
   - Click the "Actions" tab
   - Select "Apply CI Demo Patch" workflow

2. **Run the Workflow**
   - Click "Run workflow" button
   - Select branch: `main`
   - Choose action:
     - `apply` - Introduce breaking changes
     - `revert` - Restore original state
   - Enter patch name: `01-require-project-description.patch`
   - Click "Run workflow"

3. **Watch the CI Pipeline**
   - The workflow commits and pushes the changes
   - This triggers the "Tests" workflow automatically
   - Smart Tests will select relevant test subsets
   - Some tests will fail (intentionally)

4. **Review Results**
   - Check the Tests workflow results
   - See which tests Smart Tests selected
   - Observe failure patterns
   - Review Smart Tests analytics on CloudBees platform

5. **Restore Original State**
   - Run the workflow again with `revert` action
   - This removes the breaking changes
   - CI should pass again

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

### When Patch is Applied:

**Unit Tests** (may fail):
```
tests/unit/test_project_service.py::TestProjectService::test_create_project
tests/unit/test_project_service.py::TestProjectService::test_create_project_duplicate_key
```

**Integration Tests** (may fail):
```
tests/integration/test_projects_api.py::TestProjectsAPI::test_create_project
tests/integration/test_projects_api.py::TestProjectsAPI::test_create_project_invalid_key
```

**E2E Tests** (may fail):
```
tests/e2e/test_projects_e2e.py::test_create_new_project[chromium]
```

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
