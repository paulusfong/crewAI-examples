# Quick Start: Adding Mutation Testing to Your Python Project

A 15-minute guide to evaluating your test suite quality with mutation testing.

## What You'll Learn

- ✅ Install and run mutation testing
- ✅ Interpret mutation scores
- ✅ Identify and fix test gaps
- ✅ Set up CI/CD integration

## Prerequisites

- Python 3.10+
- Existing test suite with pytest
- 5-10 minutes

## Step 1: Install Mutation Testing (1 min)

```bash
pip install mutmut pytest pytest-cov
```

## Step 2: Run Your First Mutation Test (2 min)

```bash
# Basic run (tests all Python files)
python -m mutmut run

# Target specific file
python -m mutmut run --paths-to-mutate=src/mymodule.py
```

**What's happening:**
1. Mutmut generates mutants (code with deliberate bugs)
2. Runs your test suite against each mutant
3. Records which mutants survived (tests didn't catch them)

**Example output:**
```
2. Checking mutants
⠋ 15/23  🎉 12  ⏰ 0  🤔 0  🙁 3  🔇 0
```

Legend:
- 🎉 **Killed**: Test caught the mutation (good!)
- 🙁 **Survived**: Test missed the mutation (needs fixing)
- ⏰ **Timeout**: Test took too long
- 🤔 **Suspicious**: Test was slow but finished

## Step 3: View Results (1 min)

```bash
# Summary
python -m mutmut results

# Show specific mutant
python -m mutmut show 1

# Show all survivors
python -m mutmut results | grep Survived
```

**Example output:**
```
Survived 🙁 (3)
---- src/calculator.py (3) ----
1, 5, 12
```

## Step 4: Analyze Survivors (5 min)

```bash
python -m mutmut show 1
```

**Example mutant:**
```python
# Original code
def calculate_total(price, tax_rate):
    return price * (1 + tax_rate)

# Mutant (changed operator)
def calculate_total(price, tax_rate):
    return price * (1 - tax_rate)  # + became -
```

**Why it survived:**
```python
# Weak test (doesn't check the actual result)
def test_calculate_total():
    result = calculate_total(100, 0.1)
    assert result  # Just checks it returns something!
```

## Step 5: Fix the Tests (5 min)

### Common Gaps and Fixes

#### Gap 1: Not Checking Return Values

```python
# ❌ Weak
def test_calculate():
    result = calculate(5, 3)
    assert result  # Any non-zero passes

# ✅ Strong
def test_calculate():
    result = calculate(5, 3)
    assert result == 8  # Exact value
```

#### Gap 2: Not Validating Error Messages

```python
# ❌ Weak
def test_invalid_input():
    with pytest.raises(ValueError):
        calculate("invalid")

# ✅ Strong
def test_invalid_input():
    with pytest.raises(ValueError, match="must be a number"):
        calculate("invalid")
```

#### Gap 3: Not Testing Attributes

```python
# ❌ Missing
# (No test for class attributes)

# ✅ Added
def test_tool_name():
    tool = MyTool()
    assert tool.name == "Expected Name"
```

#### Gap 4: Not Testing Edge Cases

```python
# ❌ Incomplete
def test_division():
    assert divide(10, 2) == 5

# ✅ Complete
def test_division():
    assert divide(10, 2) == 5
    assert divide(10, 3) == 3.333...
    assert divide(0, 5) == 0
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)
```

## Step 6: Re-run and Verify (1 min)

```bash
# Clear cache and re-run
rm -rf .mutmut-cache
python -m mutmut run

# Check new score
python -m mutmut results
```

**Goal:** 75%+ mutation score for production code

## Interpreting Your Score

| Score | Rating | Action |
|-------|--------|--------|
| 90%+ | Excellent | 🎉 Amazing! Consider this your baseline |
| 75-89% | Good | ✅ Production-ready, document survivors |
| 50-74% | Fair | ⚠️ Improve critical paths first |
| <50% | Poor | 🚨 Significant testing gaps |

## Configuration (Optional)

Create `pyproject.toml`:

```toml
[tool.mutmut]
paths = ["src/"]
test_command = "pytest -x tests/"
```

Or `.mutmut.ini`:

```ini
[mutmut]
paths_to_mutate=src/mymodule.py
runner=pytest -x tests/
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Mutation Testing

on:
  pull_request:
    paths:
      - 'src/**/*.py'

jobs:
  mutation:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install mutmut pytest
      - name: Run mutation tests
        run: |
          python -m mutmut run
          python -m mutmut results
      - name: Check threshold
        run: |
          # Fail if < 75% mutation score
          SCORE=$(python -m mutmut results | grep -oP '\d+(?=%)' | head -1)
          if [ "$SCORE" -lt 75 ]; then
            echo "Mutation score $SCORE% is below 75%"
            exit 1
          fi
```

## Best Practices

### ✅ DO

- Start with critical modules (one at a time)
- Set realistic thresholds (75%+ is great)
- Document unreachable code survivors
- Run in CI for important changes
- Track mutation score over time

### ❌ DON'T

- Try to reach 100% (diminishing returns)
- Run on every commit (too slow)
- Test trivial code (getters/setters)
- Ignore survivors without investigation
- Remove defensive code to hit 100%

## Troubleshooting

### "No mutants generated"

**Problem:** Mutmut can't find code to mutate

**Solution:**
```bash
# Specify path explicitly
python -m mutmut run --paths-to-mutate=src/myfile.py
```

### "Tests take forever"

**Problem:** Mutation testing is slow (10-100x normal tests)

**Solutions:**
- Run incrementally: `--tests-dir=tests/unit/`
- Parallelize: use `--runner="pytest -n auto"`
- Cache results: keep `.mutmut-cache` between runs

### "Too many survivors"

**Problem:** Low mutation score

**Solutions:**
1. Check top 3-5 survivors first (biggest impact)
2. Look for patterns (all error messages? all validations?)
3. Fix patterns, not individual mutants
4. Accept some survivors in defensive code

## Quick Reference

```bash
# Run mutation testing
python -m mutmut run

# View summary
python -m mutmut results

# Show specific mutant
python -m mutmut show <id>

# Apply mutant to see it in code
python -m mutmut apply <id>

# Revert applied mutant
git checkout <file>

# Clear cache and start fresh
rm -rf .mutmut-cache

# Run with specific test command
python -m mutmut run --runner="pytest -x tests/test_specific.py"

# Generate HTML report (mutmut v2)
python -m mutmut html
```

## Example: Our Journey

**Starting point:**
- 28 tests, 85% code coverage
- Mutation score: 60.87% (Fair)
- 9 survivors

**Actions taken:**
- Added 3 tests (tool metadata)
- Enhanced 6 tests (error message validation)
- Total time: ~30 minutes

**Result:**
- 31 tests, 85% code coverage (same)
- Mutation score: 82.6% (Good)
- 4 survivors (all unreachable defensive code)

**Improvement:** +21.73% mutation score

## Next Steps

1. ✅ Run mutation testing on one module
2. ✅ Fix top 3-5 survivors
3. ✅ Document remaining survivors
4. ✅ Set up CI/CD threshold
5. ✅ Add to team's workflow

## Resources

- **Mutmut docs:** https://mutmut.readthedocs.io/
- **Our full case study:** [blog-post-mutation-testing.md](./blog-post-mutation-testing.md)
- **Mutation testing concepts:** https://en.wikipedia.org/wiki/Mutation_testing

## Getting Help

Common issues:
- **Import errors:** Make sure your code is importable (`python -c "import mymodule"`)
- **Config not found:** Mutmut looks for `pyproject.toml` or `.mutmut.ini` in current directory
- **Slow performance:** Use `--tests-dir` to target specific tests

---

**Time to completion:** 15 minutes
**Difficulty:** Beginner-friendly
**Prerequisites:** Existing test suite

*Happy mutation testing! 🧬*
