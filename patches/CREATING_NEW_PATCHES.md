# Creating New Demo Patches

This guide helps you create new demo patches for the Smart Tests CI/CD demonstration.

## What Are Demo Patches?

Demo patches are git patch files that introduce intentional breaking changes to simulate realistic development scenarios. They allow users to see how Smart Tests predicts which tests will fail based on code changes.

## Patch Requirements

### 1. Must Break Tests
- Each patch should break a **specific number of tests** (aim for 5-15 test failures)
- Patches demonstrate Smart Tests' ability to predict affected tests
- Breaking too few tests (<3) isn't a good demo
- Breaking too many tests (>20) makes it harder to analyze

### 2. Must Be Independent
- Patches should **not conflict** with each other
- Users should be able to apply patches in any order
- Patches should modify different files/domains when possible
- If patches must touch the same file, modify different sections

### 3. Should Simulate Real Scenarios
- Introduce realistic changes (validation rules, business logic, data requirements)
- Avoid artificial/nonsensical changes
- Changes should make sense to developers

### 4. Must Be Reversible
- Users can apply with `git apply patches/your-patch.patch`
- Users can revert with `git apply -R patches/your-patch.patch`
- Patches should be clean without merge conflicts

## Step-by-Step: Creating a New Patch

### Step 1: Identify Target Area

Choose a domain model or feature area to modify. Current patches cover:
- **Projects** - Project validation (patch 01)
- **Issues** - Issue validation (patch 02)
- **Comments** - Comment validation (patch 03)
- **Users** - User authentication validation (patch 04)

**Available areas for new patches:**
- Tags/Labels validation
- Assignment rules (who can be assigned to issues)
- Project membership permissions
- Issue status transitions
- Date/time fields validation
- File attachments (if added)
- API rate limiting
- Search functionality

### Step 2: Design the Breaking Change

Choose a change that will break existing tests. Examples:

**Validation Changes:**
```python
# Before: Email optional
email: Optional[str] = None

# After: Email required with specific format
email: EmailStr = Field(..., regex=r'^[a-z]+@company\.com$')
```

**Business Logic Changes:**
```python
# Before: Anyone can create issues
def create_issue(project_id: int, user_id: int):
    # Create issue

# After: Only project members can create issues
def create_issue(project_id: int, user_id: int):
    if not is_project_member(project_id, user_id):
        raise HTTPException(403, "Only project members can create issues")
```

**Data Requirement Changes:**
```python
# Before: Due date optional
due_date: Optional[datetime] = None

# After: Due date required and must be in future
due_date: datetime = Field(...)
# + Add validation in service layer
```

### Step 3: Implement Changes on a Clean Branch

```bash
# Start from clean main branch
git checkout main
git pull origin main

# Create a working branch
git checkout -b create-patch-05

# Make your changes
# Edit the relevant files (schemas, models, services)
```

**Files typically modified:**
- `app/schemas/[domain].py` - Pydantic schemas (validation)
- `app/models/[domain].py` - SQLAlchemy models (database)
- `app/services/[domain]_service.py` - Business logic

### Step 4: Test Your Changes

```bash
# Run tests to see which ones break
make test

# Or run specific test suites
make test-unit
make test-integration

# Count failures and note which tests break
pytest -v | grep FAILED | wc -l
```

**Ideal outcome:** 5-15 test failures that are related to your change.

**Too few failures?** Make the validation stricter or add more checks.

**Too many failures?** Relax the validation or narrow the scope.

### Step 5: Create the Patch File

```bash
# Create patch from your staged changes
git add app/schemas/[domain].py app/models/[domain].py app/services/[domain]_service.py
git diff --cached > patches/05-your-patch-name.patch

# Or create patch from unstaged changes
git diff > patches/05-your-patch-name.patch
```

**Naming convention:** `[number]-[descriptive-name].patch`
- Number: Sequential (01, 02, 03...)
- Name: Lowercase with hyphens, describes the change
- Examples: `05-require-issue-assignee.patch`, `06-validate-tag-names.patch`

### Step 6: Verify the Patch

```bash
# Revert your changes
git checkout app/

# Test applying the patch
git apply patches/05-your-patch-name.patch

# Verify files changed correctly
git diff

# Run tests again to confirm breakage
make test

# Revert the patch
git apply -R patches/05-your-patch-name.patch

# Verify clean state
git status
```

### Step 7: Test Independence with Other Patches

```bash
# Test applying your patch with existing patches
git apply patches/01-require-project-description.patch
git apply patches/05-your-patch-name.patch

# Should apply cleanly without conflicts
# Run tests
make test

# Revert all
git apply -R patches/05-your-patch-name.patch
git apply -R patches/01-require-project-description.patch
```

### Step 8: Document the Patch

Add your patch to `patches/README.md`:

```markdown
### 05-your-patch-name.patch

**Purpose**: Brief description of what this patch does and why.

**Changes**:
- Specific change 1
- Specific change 2
- Specific change 3

**Expected Impact**:
- ❌ Breaks X tests (Y unit + Z integration tests)
- ✅ Demonstrates [specific Smart Tests capability]
- 🎯 Shows [specific scenario]

**Tests that will fail**:
- Unit tests:
  - `test_function_name` (reason)
  - `test_another_function` (reason)
- Integration tests:
  - `test_api_endpoint` (reason)
```

### Step 9: Update the Workflow

Add your patch to `.github/workflows/apply-demo-patch.yml`:

```yaml
patch_name:
  description: 'Patch to apply'
  required: true
  type: choice
  options:
    - 01-require-project-description.patch
    - 02-require-long-issue-titles.patch
    - 03-require-long-comments.patch
    - 04-require-corporate-email.patch
    - 05-your-patch-name.patch  # Add here
  default: '01-require-project-description.patch'
```

### Step 10: Commit Everything

```bash
# Add patch file and documentation
git add patches/05-your-patch-name.patch
git add patches/README.md
git add .github/workflows/apply-demo-patch.yml

# Commit
git commit -m "Add demo patch 05: [brief description]"
```

## AI Assistant Prompt

Use this prompt with an AI assistant (like Claude) to generate patches:

---

**Prompt:**

```
I need to create a new demo patch for this Issue Tracker application that will intentionally break some tests to demonstrate Smart Tests' predictive capabilities.

Requirements:
1. The patch should introduce a realistic code change (new validation rule, business logic requirement, or data constraint)
2. It should break between 5-15 tests (ideally distributed across unit and integration tests)
3. It must be independent of existing patches (no conflicts when applied together)
4. It should modify the [DOMAIN] area (choose: projects, issues, comments, tags, users, assignments)

Current existing patches:
- 01: Requires project descriptions (50+ chars) - breaks 8 tests
- 02: Requires long issue titles (20+ chars) - breaks ~10 tests
- 03: Requires long comments (15+ chars) - breaks ~10 tests
- 04: Requires corporate email domains - breaks ~7 tests

Suggested change idea: [YOUR IDEA HERE, or ask AI to suggest]

Please:
1. Analyze the codebase structure for the target domain
2. Suggest a specific breaking change that will fail tests
3. Show which files need to be modified (schemas, models, services)
4. Provide the exact code changes needed
5. Predict which tests will break and why
6. Generate the git patch file content
7. Write the documentation section for patches/README.md

After implementation, I'll verify:
- Patch applies cleanly
- Expected number of tests fail
- Patch is independent (no conflicts with existing patches)
- Changes are realistic and demonstrate Smart Tests effectively
```

---

## Example Patch Ideas

### Idea 1: Require Issue Assignee
**Domain:** Issues
**Change:** Make assignee field required (can't create unassigned issues)
**Expected failures:** ~8 tests (tests that create issues without assignees)

### Idea 2: Validate Tag Names
**Domain:** Tags
**Change:** Require tag names to be 3-20 chars, alphanumeric only
**Expected failures:** ~5-7 tests (tests with short tags or special characters)

### Idea 3: Project Member Restrictions
**Domain:** Projects
**Change:** Only project owners can add/remove members
**Expected failures:** ~6-8 tests (tests where non-owners modify membership)

### Idea 4: Issue Status Transitions
**Domain:** Issues
**Change:** Enforce valid status transitions (can't jump from OPEN to CLOSED without IN_PROGRESS)
**Expected failures:** ~10-12 tests (tests that skip workflow steps)

### Idea 5: Comment Length and Format
**Domain:** Comments
**Change:** Require comments to be 20-500 chars and not all caps
**Expected failures:** ~8-10 tests (tests with short comments or all-caps)

### Idea 6: Password Complexity
**Domain:** Users
**Change:** Require passwords with uppercase, lowercase, digit, and special char
**Expected failures:** ~5-7 tests (tests with simple passwords)

## Tips for Success

✅ **DO:**
- Test your patch thoroughly before committing
- Document expected test failures accurately
- Choose realistic, developer-friendly scenarios
- Verify independence from other patches
- Run both unit and integration tests

❌ **DON'T:**
- Create patches that break >20 tests (too noisy)
- Create patches that break <3 tests (not impactful enough)
- Modify test files themselves (only application code)
- Create patches that conflict with existing ones
- Use nonsensical or artificial changes

## Troubleshooting

**Patch won't apply:**
- Ensure you created it from a clean main branch
- Check for trailing whitespace issues
- Verify file paths are correct

**Wrong number of test failures:**
- Adjust validation strictness (more/less strict)
- Widen or narrow scope of changes
- Consider cascade effects on related tests

**Conflicts with existing patches:**
- Modify different files if possible
- Edit different sections of the same file
- Use git ranges to avoid overlap

**Tests fail for wrong reasons:**
- Review error messages carefully
- Ensure changes are applied correctly
- Check that test data fixtures meet new requirements

## Questions?

See existing patches in `patches/` directory for examples.
