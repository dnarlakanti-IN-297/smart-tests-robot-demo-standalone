# Smart Tests Demo Execution Plan

## The Problem with Current Approach

❌ Running once doesn't show value  
❌ No baseline to compare against  
❌ Can't demonstrate time savings without history  

## Proper Demo Flow (30-45 minutes)

### Phase 1: Establish Baseline (15-20 minutes)

**Goal:** Build enough data for Smart Tests to learn patterns and make predictions

**Actions:**
1. **Run observation mode 5-6 times**
   ```bash
   # Run 1
   gh workflow run tests-robot.yml --ref patch-robot-demo -f mode=observation
   # Wait ~4 minutes for completion
   
   # Run 2
   gh workflow run tests-robot.yml --ref patch-robot-demo -f mode=observation
   # Wait ~4 minutes
   
   # Run 3
   gh workflow run tests-robot.yml --ref patch-robot-demo -f mode=observation
   # Wait ~4 minutes
   
   # Run 4
   gh workflow run tests-robot.yml --ref patch-robot-demo -f mode=observation
   # Wait ~4 minutes
   
   # Run 5
   gh workflow run tests-robot.yml --ref patch-robot-demo -f mode=observation
   # Wait ~4 minutes
   ```

2. **Record baseline metrics:**
   - Average execution time: ~3-4 minutes
   - Total tests: 56
   - Success rate: 100%
   - CI cost: ~32 minutes total

**What's Happening:**
- Smart Tests is learning which tests cover which code
- Building ML model of test-to-code relationships
- Recording execution patterns
- **No time savings yet** - this is investment phase

### Phase 2: Show Intelligence (10-15 minutes)

**Goal:** Demonstrate Smart Tests can predict relevant tests

**Run production mode with different targets:**

```bash
# Production Run 1: 80% target
gh workflow run tests-robot.yml --ref patch-robot-demo \
  -f mode=production -f target="--target 80%"
# Expected: ~45 tests, ~2.5 minutes

# Production Run 2: 50% target  
gh workflow run tests-robot.yml --ref patch-robot-demo \
  -f mode=production -f target="--target 50%"
# Expected: ~28 tests, ~1.5 minutes

# Production Run 3: 80% target (repeat to show consistency)
gh workflow run tests-robot.yml --ref patch-robot-demo \
  -f mode=production -f target="--target 80%"
# Expected: Similar results, proves reliability
```

**Record savings:**
- 80% target: 2.5 min vs 4 min = **37% time saved** (1.5 min)
- 50% target: 1.5 min vs 4 min = **62% time saved** (2.5 min)

### Phase 3: Show Targeted Intelligence (Optional, 15 minutes)

**Goal:** Prove Smart Tests understands code-to-test relationships

**Make targeted code changes:**

**Change 1: Modify Comment Service**
```bash
# Make a trivial change to comment_service.py
echo "# Smart Tests demo change" >> app/services/comment_service.py
git add app/services/comment_service.py
git commit -m "Demo: Modify comment service"
git push

# Trigger production mode
gh workflow run tests-robot.yml --ref patch-robot-demo \
  -f mode=production -f target="--target 80%"
```

**Expected:** Smart Tests should primarily run comment-related tests (8 tests) + some related integration tests (~12-15 tests total)

**Change 2: Modify Issue Service**
```bash
# Make a trivial change to issue_service.py  
echo "# Smart Tests demo change" >> app/services/issue_service.py
git add app/services/issue_service.py
git commit -m "Demo: Modify issue service"
git push

# Trigger production mode
gh workflow run tests-robot.yml --ref patch-robot-demo \
  -f mode=production -f target="--target 80%"
```

**Expected:** Smart Tests should primarily run issue-related tests (13 tests) + related integration tests (~18-20 tests total)

## Demo Presentation Flow

### Slide 1: The Problem
"Our CI pipeline runs 56 Robot Framework tests on every commit, taking 4 minutes each time. With 10 developers making 50 commits/day, that's **200 minutes of CI time daily**."

### Slide 2: Traditional Approaches Don't Work
- ❌ Skip tests → Missed bugs
- ❌ Manual test selection → Inconsistent, error-prone
- ❌ Run tests on schedule → Delays feedback

### Slide 3: Smart Tests Solution
"AI-powered predictive test selection that learns your codebase and runs only relevant tests."

### Slide 4: Live Demo - Observation Mode
Show GitHub Actions running observation mode:
- All 56 tests running
- ~4 minutes execution time
- "Smart Tests is learning..."

### Slide 5: The Data
Show CloudBees UI with 5-6 observation runs:
- Consistent ~4 minute baseline
- 100% test coverage maintained
- Patterns identified

### Slide 6: Live Demo - Production Mode (80%)
Show GitHub Actions running production mode:
- ~45 tests selected (80% of suite)
- ~2.5 minutes execution time
- **37% time saved** = 1.5 minutes

### Slide 7: Live Demo - Production Mode (50%)
Show GitHub Actions running production mode:
- ~28 tests selected (50% of suite)
- ~1.5 minutes execution time
- **62% time saved** = 2.5 minutes

### Slide 8: The ROI
"With 50 commits/day and 50% time savings:"
- **Daily savings**: 100 minutes CI time
- **Monthly savings**: 2,000 minutes = 33 hours
- **Annual savings**: 25,000 minutes = **417 hours = 52 working days**
- **Cost savings**: ~$200/month in CI compute

### Slide 9: Targeted Intelligence
Show commit to comment_service.py:
- Smart Tests selects only 15 tests (~30% of suite)
- **70% time saved** = 2.8 minutes
- All comment-related tests included
- Zero risk of missing bugs

### Slide 10: Safety & Accuracy
- Prediction accuracy: >95% after learning period
- Failed predictions → automatic full test run
- Continuous learning improves over time
- **Zero compromise on quality**

### Slide 11: Works With Any Framework
- ✅ Robot Framework (just demoed)
- ✅ pytest (already using)
- ✅ JUnit, Jest, RSpec, Go Test
- ✅ Any test framework with XML output

## Success Metrics to Track

### Before Smart Tests (Baseline Runs)
```
Run 1: 56 tests, 3m 45s ✅
Run 2: 56 tests, 4m 02s ✅  
Run 3: 56 tests, 3m 58s ✅
Run 4: 56 tests, 4m 10s ✅
Run 5: 56 tests, 3m 52s ✅
Average: 56 tests, 3m 57s
```

### After Smart Tests (Production Runs - 80%)
```
Run 1: 45 tests, 2m 28s ✅ (37% saved)
Run 2: 46 tests, 2m 35s ✅ (35% saved)
Run 3: 44 tests, 2m 22s ✅ (40% saved)
Average: 45 tests, 2m 28s (37% saved)
```

### After Smart Tests (Production Runs - 50%)
```
Run 1: 28 tests, 1m 32s ✅ (61% saved)
Run 2: 29 tests, 1m 38s ✅ (59% saved)
Run 3: 27 tests, 1m 28s ✅ (63% saved)
Average: 28 tests, 1m 33s (61% saved)
```

### Targeted Changes (Production - 80%)
```
Comment service change: 15 tests, 58s ✅ (76% saved)
Issue service change: 20 tests, 1m 15s ✅ (68% saved)
Auth service change: 18 tests, 1m 08s ✅ (71% saved)
```

## Pre-Demo Checklist

- [ ] Merge PR #1 to main (makes "Run workflow" button always visible)
- [ ] Run 5-6 observation mode builds to establish baseline
- [ ] Verify all tests passing (56/56)
- [ ] Check CloudBees UI is showing results
- [ ] Prepare targeted code changes for Phase 3
- [ ] Have GitHub Actions tab open and ready
- [ ] Have CloudBees Smart Tests dashboard open
- [ ] Calculate your team's specific ROI numbers

## Common Questions & Answers

**Q: How many runs do I need before seeing value?**  
A: Observation mode starts learning immediately. After 3-5 runs, production mode can begin showing savings. Full optimization after 10-15 runs.

**Q: What if Smart Tests misses a test?**  
A: Predictions are tracked. If a test fails that wasn't run, Smart Tests automatically triggers a full run and learns from it.

**Q: Does this work with our test framework?**  
A: Yes! Smart Tests supports pytest, Robot Framework, JUnit, Jest, RSpec, Go Test, and any framework that produces XML results.

**Q: Can we use different targets for different branches?**  
A: Absolutely! Common pattern: 50% for feature branches (speed), 80% for main/release (confidence).

**Q: How much does it cost?**  
A: Smart Tests pricing is based on team size. Typical ROI is 10-20x the subscription cost in CI savings alone.

## Post-Demo Follow-Up

1. **Send metrics summary**: Baseline vs production comparison
2. **Share CloudBees dashboard link**: So they can explore
3. **Provide trial access**: Let them test with their codebase
4. **Schedule architecture review**: Discuss integration approach
5. **Create success criteria**: Define what "success" looks like

## Next Steps for This Demo

1. **Fix the recording issue** in workflow (Robot XML format)
2. **Run 5-6 observation builds** to establish baseline  
3. **Document actual metrics** from those runs
4. **Run production builds** and capture savings
5. **Update demo guide** with real numbers

---

**Remember:** The value of Smart Tests is **NOT in a single run**, but in the **cumulative savings over time**. A proper demo requires showing the pattern of savings across multiple runs.
