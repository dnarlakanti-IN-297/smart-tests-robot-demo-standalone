# CI Demonstration Patches

This directory contains patch files used for CI/CD demonstration purposes. These patches can be applied to simulate code changes and test failures.

## Available Patches

**Note**: All patches are independent and can be applied in any order or combination.

### 01-require-project-description.patch

**Purpose**: Makes project descriptions required with minimum 50 characters, breaking tests with short descriptions.

**Changes**:
- Makes `description` field required in Project model (non-nullable)
- Updates ProjectCreate schema to require description (minimum 50 characters, maximum 500)
- Adds validation in ProjectService to enforce 50-character minimum

**Expected Impact**:
- ❌ Breaks 8 tests (2 unit + 6 integration tests)
- ✅ Demonstrates Smart Tests selecting relevant tests
- 🎯 Shows CI catching breaking changes

**Tests that will fail**:
- Unit tests:
  - `test_create_project` (description too short: "A new project" = 13 chars)
  - `test_create_project_duplicate_key` (description too short: "Duplicate key" = 13 chars)
- Integration tests:
  - `test_create_project` (description too short)
  - `test_create_project_duplicate_key` (description too short)
  - `test_get_user_projects` (uses fixture with short description)
  - `test_get_project_by_id` (uses fixture with short description)
  - `test_update_project` (uses fixture with short description)
  - Plus potentially more E2E tests

### 02-require-long-issue-titles.patch

**Purpose**: Makes issue titles require minimum 20 characters.

**Changes**:
- Updates IssueBase schema to require `title` minimum 20 characters (was 1)
- Updates IssueUpdate schema with same validation

**Expected Impact**:
- ❌ Breaks ~10 tests (5 unit + 5 integration tests)
- ✅ Affects issue-related tests only
- 🎯 Shows validation of user input

**Tests that will fail**:
- Unit tests: `test_create_issue`, `test_create_issue_no_access`, `test_update_issue`, `test_create_issue_with_tags`
- Integration tests: `test_create_issue`, `test_create_issue_without_access`, `test_update_issue`, `test_update_issue_status`

### 03-require-long-comments.patch

**Purpose**: Makes comments require minimum 15 characters.

**Changes**:
- Updates CommentBase schema to require `content` minimum 15 characters (was 1)
- Updates CommentUpdate schema with same validation
- Adds maximum 1000 characters limit

**Expected Impact**:
- ❌ Breaks ~10 tests (8 unit + 2 integration tests)
- ✅ Affects comment-related tests only
- 🎯 Demonstrates data quality requirements

**Tests that will fail**:
- Unit tests: All comment service tests that use short comments
- Integration tests: `test_get_comments_by_issue`, `test_update_comment_by_non_author`

### 04-require-corporate-email.patch

**Purpose**: Requires users to have corporate email addresses from approved domains.

**Changes**:
- Adds email validation to UserBase schema
- Requires email domain to be one of: `company.com`, `corp.com`, `enterprise.com`
- Uses Pydantic field_validator for validation

**Expected Impact**:
- ❌ Breaks ~7 tests (3 unit + 4 integration tests)
- ✅ Affects user/auth tests only
- 🎯 Shows business rule enforcement

**Tests that will fail**:
- Unit tests: `test_create_user`, `test_create_user_duplicate_email`, `test_create_user_duplicate_username`
- Integration tests: `test_register_user`, `test_register_duplicate_email`, `test_register_duplicate_username`, `test_access_protected_endpoint_with_token`

## Combining Patches

All patches are independent and can be combined:

```bash
# Apply multiple patches at once
git apply patches/01-require-project-description.patch
git apply patches/02-require-long-issue-titles.patch
git apply patches/03-require-long-comments.patch
git apply patches/04-require-corporate-email.patch

# This will break ~35 total tests across the entire codebase
```

**Expected failures when all patches applied**:
- Project tests: 8 failures
- Issue tests: 10 failures
- Comment tests: 10 failures
- User/Auth tests: 7 failures
- **Total: ~35 test failures** (perfect for comprehensive CI demos)

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

**Prerequisites**: Create a patch branch first
```bash
git checkout -b patch-demo
git push -u origin patch-demo
```

Navigate to Actions → "Apply CI Demo Patch" → Run workflow

Options:
- **Branch**: Select a branch starting with `patch-*` (e.g., `patch-demo`)
- **action**: `apply` (introduce breaking changes) or `revert` (restore original)
- **patch_name**: Name of patch file (e.g., `01-require-project-description.patch`)

**Note**: This workflow only runs on branches starting with `patch-*` for safety.

## Patch Combinations for Different Demo Scenarios

### Scenario 1: Small Impact
Apply one patch to show focused test failures:
```bash
git apply patches/04-require-corporate-email.patch  # 7 failures
```

### Scenario 2: Medium Impact
Apply 2-3 patches for broader test coverage:
```bash
git apply patches/01-require-project-description.patch  # 8 failures
git apply patches/02-require-long-issue-titles.patch   # 10 failures
# Total: ~18 failures
```

### Scenario 3: High Impact
Apply all patches for maximum demonstration:
```bash
git apply patches/*.patch  # All 4 patches
# Total: ~35 failures across all test suites
```

## Future Enhancements

Potential additional patches:
- Fix patches that resolve the breaking changes
- Refactoring patches that improve code without breaking tests
- Performance optimization patches

## Creating New Patches

Want to create additional demo patches? See:

- **[CREATING_NEW_PATCHES.md](./CREATING_NEW_PATCHES.md)** - Comprehensive guide to creating new demo patches with step-by-step instructions, requirements, and examples
- **[AI_PATCH_GENERATION_PROMPT.txt](./AI_PATCH_GENERATION_PROMPT.txt)** - Ready-to-use prompt template for AI assistants to help generate patches

**Quick start:**
1. Read CREATING_NEW_PATCHES.md to understand the process
2. Copy the prompt from AI_PATCH_GENERATION_PROMPT.txt
3. Customize it with your target domain and change idea
4. Use an AI assistant to generate the patch code
5. Test, validate, and document your patch

**Patch ideas:**
- Require issue assignees
- Validate tag name format (alphanumeric, length limits)
- Enforce project member restrictions
- Add issue status transition rules
- Enhance password complexity requirements
- Add due date validation for issues

## Notes

- These patches are for demonstration purposes only
- Do not apply patches to production branches
- Always review patch contents before applying
- Patches are versioned for reproducible demonstrations
