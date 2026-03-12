# CI Demonstration Patches

This directory contains patch files used for CI/CD demonstration purposes. These patches can be applied to simulate code changes and test failures.

## Available Patches

### 01-require-project-description.patch

**Purpose**: Makes project descriptions required, breaking tests that create projects without descriptions.

**Changes**:
- Makes `description` field required in Project model (non-nullable)
- Updates ProjectCreate schema to require description (minimum 10 characters)
- Adds validation in ProjectService to enforce description requirement

**Expected Impact**:
- ❌ Breaks ~5-10 tests that create projects without descriptions
- ✅ Demonstrates Smart Tests selecting relevant tests
- 🎯 Shows CI catching breaking changes

**Tests that will fail**:
- Unit tests: `test_create_project` (without description)
- Integration tests: `test_create_project` (without description)
- E2E tests: `test_create_new_project` (may fail if no description provided)

## Usage

### Apply a patch manually:
```bash
git apply patches/01-require-project-description.patch
```

### Revert a patch:
```bash
git apply -R patches/01-require-project-description.patch
```

### Use GitHub Actions workflow:
Navigate to Actions → "Apply CI Demo Patch" → Run workflow

Options:
- **action**: `apply` (introduce breaking changes) or `revert` (restore original)
- **patch_name**: Name of patch file (e.g., `01-require-project-description.patch`)

## Future Patches

Planned timeline of patches for comprehensive CI demos:
- `02-break-tests.patch` - Intentional test failures
- `03-fix-tests.patch` - Fix the broken tests
- `04-refactor.patch` - Code refactoring without behavior changes

## Notes

- These patches are for demonstration purposes only
- Do not apply patches to production branches
- Always review patch contents before applying
- Patches are versioned for reproducible demonstrations
