# Smart Tests Integration

This project integrates [Smart Tests](https://docs.cloudbees.com/docs/cloudbees-platform/latest/analytics/smart-tests) to optimize E2E test execution by running only a subset of tests based on historical data and code changes.

**Note:** We use `pytest` framework with Smart Tests (not `playwright`) because we run tests via `pytest` with the `pytest-playwright` plugin, not the Playwright CLI directly.

## What is Smart Tests?

Smart Tests uses AI and historical test data to intelligently select which tests to run, reducing CI time while maintaining test coverage. It analyzes:
- Code changes
- Test execution history
- Test failure patterns
- Test execution times

## How It Works

### Before Smart Tests
```bash
pytest tests/e2e/  # Runs all 29 E2E tests (~70 seconds)
```

### After Smart Tests
```bash
# Generate test list (collect test cases)
pytest --collect-only -q tests/e2e/ | grep "::" > test_list.txt

# Request subset (e.g., 50% of tests)
cat test_list.txt | smart-tests subset pytest \
  --session @session.txt \
  --target 50% > smart-tests-subset.txt

# Run only the subset (~35 seconds)
pytest $(cat smart-tests-subset.txt)
```

## Setup

### 1. Get a Smart Tests Token

1. Sign up at [CloudBees Platform](https://www.cloudbees.com/)
2. Navigate to Analytics → Smart Tests
3. Generate an API token

### 2. Add Token to GitHub Secrets

1. Go to your repository on GitHub
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `SMART_TESTS_TOKEN`
5. Value: Your Smart Tests API token
6. Click **Add secret**

### 3. Workflow Integration

The Smart Tests integration is already configured in `.github/workflows/tests.yml` in the `e2e-tests` job:

```yaml
env:
  SMART_TESTS_TOKEN: ${{ secrets.SMART_TESTS_TOKEN }}

steps:
  - name: Verify Smart Tests connectivity
    run: smart-tests verify || true

  - name: Record build with Smart Tests
    run: smart-tests record build --build ${{ github.run_id }}

  - name: Record session with Smart Tests
    run: smart-tests record session --build ${{ github.run_id }} --observation --test-suite pytest-e2e > session.txt

  - name: Generate test list
    run: |
      pytest --collect-only -q tests/e2e/ | grep "::" > test_list.txt || true
      cat test_list.txt

  - name: Create Smart Tests subset
    run: |
      cat test_list.txt | smart-tests subset pytest \
        --session @session.txt \
        --target 50% > smart-tests-subset.txt
      cat smart-tests-subset.txt

  - name: Run E2E tests (Smart Tests subset)
    run: |
      if [ -s smart-tests-subset.txt ]; then
        pytest $(cat smart-tests-subset.txt) -v --junit-xml=test-results/junit.xml
      else
        echo "No tests to run in subset"
      fi

  - name: Record test results with Smart Tests
    if: always()
    run: smart-tests record tests pytest --session @session.txt "test-results/*.xml"
```

## Configuration Options

### Target Optimization

Control how many tests to run:

```bash
--target 50%      # Run 50% of tests
--target 30%      # Run 30% of tests (faster, less coverage)
--target 75%      # Run 75% of tests (slower, more coverage)
```

### Test Suite Name

Customize the test suite identifier:

```bash
--test-suite pytest-e2e          # E2E tests with pytest
--test-suite pytest-integration  # Integration tests
--test-suite pytest-smoke        # Smoke tests
```

## Benefits

### Time Savings
- **Before**: All 29 E2E tests = ~70 seconds
- **After**: 50% subset = ~35 seconds
- **Savings**: 50% reduction in E2E test time

### Smart Selection
Smart Tests doesn't randomly select tests. It prioritizes:
1. Tests that recently failed
2. Tests affected by code changes
3. Tests with historical instability
4. Critical path tests

### Full Coverage Over Time
While each build runs a subset, the complete test suite is covered across multiple builds, ensuring no tests are neglected.

## Local Usage

You can also use Smart Tests locally:

```bash
# Install smart-tests-cli
pip install smart-tests-cli~=2.0

# Set your token
export SMART_TESTS_TOKEN="your-token-here"

# Verify connectivity
smart-tests verify

# Record a build
smart-tests record build --build local-$(date +%s)

# Record a session
smart-tests record session \
  --build local-$(date +%s) \
  --observation \
  --test-suite pytest-e2e > session.txt

# Generate test list (collect test cases)
pytest --collect-only -q tests/e2e/ | grep "::" > test_list.txt

# Generate subset
cat test_list.txt | smart-tests subset pytest \
  --session @session.txt \
  --target 50% > subset.txt

# Run subset
pytest $(cat subset.txt) -v --junit-xml=test-results/junit.xml

# Record results
smart-tests record tests pytest --session @session.txt "test-results/*.xml"
```

## Troubleshooting

### Token Issues

If you get authentication errors:
```bash
# Verify token is set
echo $SMART_TESTS_TOKEN

# Test connectivity
smart-tests verify
```

### No Tests in Subset

If `smart-tests-subset.txt` is empty:
- First run may select all tests to gather baseline data
- Adjust `--target` percentage
- Check that test files match the pattern `test_*.py`

### Python Version

Smart Tests CLI requires Python 3.13+:
```bash
python --version  # Should be 3.13 or higher
```

## Resources

- [Smart Tests Documentation](https://docs.cloudbees.com/docs/cloudbees-platform/latest/analytics/smart-tests)
- [Smart Tests CLI GitHub](https://github.com/cloudbees/smart-tests-cli)
- [CloudBees Platform](https://www.cloudbees.com/)

## Monitoring

Track your Smart Tests performance:
1. View test execution trends in CloudBees Analytics
2. Monitor time savings per build
3. Analyze test selection patterns
4. Review test coverage over time

## Disabling Smart Tests

To temporarily disable Smart Tests and run all tests:

```yaml
# In .github/workflows/tests.yml, replace:
pytest $(cat smart-tests-subset.txt)

# With:
pytest tests/e2e/
```

Or set target to 100%:
```bash
--target 100%
```
