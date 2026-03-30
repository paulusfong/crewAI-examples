# Mutation Testing Setup for Stock Analysis

## Overview

This document describes the mutation testing setup for the Stock Analysis crew, specifically for the `CalculatorTool`.

## What is Mutation Testing?

Mutation testing evaluates test suite quality by introducing deliberate bugs (mutations) into your code and checking if your tests catch them. A **high mutation score** means your tests are effective at catching real bugs.

### Mutation Score Interpretation

| Score | Quality | Interpretation |
|-------|---------|----------------|
| 90%+ | Excellent | Tests catch most bugs |
| 75-89% | Good | Some gaps to address |
| 50-74% | Fair | Significant testing gaps |
| <50% | Poor | Tests need major improvement |

## Test Suite

### Location
- Tests: `tests/tools/test_calculator_tool.py`
- Code: `src/stock_analysis/tools/calculator_tool.py`

### Test Coverage
- **28 test cases** covering:
  - Basic arithmetic operations (6 tests)
  - Complex expressions with order of operations (4 tests)
  - Unary operators (3 tests)
  - Error handling (8 tests)
  - Edge cases (5 tests)
  - Real-world examples (2 tests)

- **85% code coverage** (40 statements, 6 missed)

### Missed Lines
Lines not covered by tests:
- Line 40: Branch in `_eval_node` for `ast.Num` (Python < 3.8)
- Line 46: Unsupported operator error path
- Line 52: Unsupported unary operator error path
- Line 55: Unsupported node type error path
- Lines 62-63: Generic exception handler

## Mutation Testing Configuration

### Framework
- **mutmut** (Python mutation testing framework)

### Configuration File
`.mutmut.ini`:
```ini
[mutmut]
paths_to_mutate=src/stock_analysis/tools/calculator_tool.py
runner=pytest -x --assert=plain
backup_dir=.mutmut_cache
```

### Common Mutations

mutmut introduces these types of mutations:

| Mutation Type | Example | Purpose |
|---------------|---------|---------|
| Arithmetic operators | `+` → `-` | Test math logic |
| Comparison operators | `>` → `>=` | Test boundary conditions |
| Boolean operators | `and` → `or` | Test logic |
| Return values | `return x` → `return None` | Test null handling |
| String literals | `"str"` → `""` | Test string handling |
| Number literals | `5` → `6` | Test numeric constants |
| Remove statements | `validate()` → removed | Test side effects |

## Running Mutation Testing

### Full Mutation Run
```bash
python3 -m mutmut run
```

### View Results
```bash
# Show summary
python3 -m mutmut results

# Show specific mutant
python3 -m mutmut show <mutant_id>

# Show only surviving mutants
python3 -m mutmut results | grep "Survived"
```

### View in HTML Report
```bash
python3 -m mutmut html
# Open htmlcov/index.html in browser
```

### Incremental Testing (Faster)
```bash
# Only test changed code since last run
python3 -m mutmut run --rerun-all
```

## Expected Results

Based on our 85% code coverage, we expect:

1. **Most mutants killed** - Our comprehensive test suite should catch most mutations
2. **Some survivors** - Untested branches (6% uncovered lines) may allow some mutants to survive
3. **Boundary condition gaps** - We may find missing tests for edge cases like:
   - Operator precedence edge cases
   - Specific error message validation
   - Missing branches in error handling

## Interpreting Surviving Mutants

If mutants survive, it means:

1. **Missing test case** - We need to add a test for that code path
2. **Weak assertion** - Test runs but doesn't check the right thing
3. **Equivalent mutant** - The mutation doesn't change behavior (rare)
4. **Dead code** - Code is unreachable (should be removed)

## Next Steps After Mutation Testing

1. **Review surviving mutants**: `mutmut show <id>`
2. **Add missing tests** for uncaught mutations
3. **Improve assertions** for weak tests
4. **Remove dead code** if found
5. **Re-run** mutation testing to verify improvements

## Running Tests

### Unit Tests Only
```bash
python3 -m pytest tests/tools/test_calculator_tool.py -v
```

### With Coverage Report
```bash
python3 -m pytest tests/tools/test_calculator_tool.py --cov=src/stock_analysis/tools --cov-report=html
```

### Fast (No Coverage)
```bash
python3 -m pytest tests/tools/test_calculator_tool.py -q
```

## CI/CD Integration

To add mutation testing to CI/CD:

```yaml
# .github/workflows/mutation-testing.yml
name: Mutation Testing

on:
  pull_request:
    paths:
      - 'src/stock_analysis/tools/**'

jobs:
  mutation:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install dependencies
        run: |
          pip install pytest mutmut
      - name: Run mutation tests
        run: |
          cd crews/stock_analysis
          mutmut run
          mutmut results
      - name: Check mutation score
        run: |
          # Fail if mutation score < 80%
          mutmut results | grep "survived" | awk '{if ($1 > 20) exit 1}'
```

## Performance Considerations

- **Runtime**: Mutation testing is 10-100x slower than normal tests
- **Parallelization**: Run `mutmut run --parallel` for faster execution
- **Incremental mode**: Only test changed files in CI
- **Cache results**: Keep `.mutmut_cache` between runs

## Additional Resources

- [mutmut documentation](https://mutmut.readthedocs.io/)
- [Mutation Testing Best Practices](https://en.wikipedia.org/wiki/Mutation_testing)
- [Test Coverage vs Mutation Score](https://www.softwaretestinghelp.com/mutation-testing/)

## Maintenance

- Run mutation testing before major releases
- Set minimum mutation score threshold (e.g., 80%)
- Review and update tests when mutants survive
- Track mutation score trends over time
