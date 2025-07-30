# TDD Enforcement Implementation Plan

## Key Learnings from TDD-Guard

### 1. Core Architecture
TDD-Guard successfully enforces Test-Driven Development by:
- **Capturing test results** during test runs using a custom reporter
- **Storing test results** in a JSON file accessible to the validator
- **Including test output** in the validation context
- **Using sophisticated prompts** for each TDD phase

### 2. Critical Components

#### Test Result Capture (VitestReporter)
- Implements Vitest reporter interface
- Captures test module ID, test names, states (passed/failed), and error messages
- Saves results to `.claude/tdd-guard/data/test.json` on session end

#### Validation Context
- Combines file modifications, todo list, and **test results**
- Test results provide crucial context for determining TDD phase
- Allows validator to distinguish between Red, Green, and Refactor phases

#### Prompt Engineering
- Specific prompts for Write vs Edit operations
- Phase-specific validation rules
- Maps test failure types to allowed implementations

### 3. TDD Rules from TDD-Guard

#### Red Phase (Writing Tests)
- **Allowed**: Writing ONE failing test
- **Blocked**: Writing multiple tests at once
- **Blocked**: Tests that pass immediately

#### Green Phase (Making Tests Pass)
- **Allowed**: Minimal implementation to fix specific test failure
- **Allowed**: Implementation that matches the test failure type
- **Blocked**: Implementation without proper test failure
- **Blocked**: Excessive implementation beyond test requirements

#### Refactor Phase (Improving Code)
- **Allowed**: Refactoring when tests are passing
- **Blocked**: Refactoring without passing tests
- **Blocked**: Changes that break existing tests

### 4. Test Failure Mapping
TDD-Guard maps specific test failures to allowed implementations:
- `ReferenceError: X is not defined` → Allow creating X
- `TypeError: X is not a constructor` → Allow making X a class
- `AssertionError` → Allow fixing the specific assertion

## Our Implementation Plan

### Phase 1: Foundation (Completed)
1. **PytestReporter**
   - Captures test results during pytest runs
   - Implements pytest hooks (pytest_runtest_logreport, pytest_sessionfinish)
   - Saves results automatically on session end

2. **FileStorage**
   - Manages test result persistence
   - Saves to `.claude/claude-code-adk-validator/data/test.json`
   - Provides load/save interface

### Phase 2: Python Environment Detection (Next)
1. **Python Environment Detector**
   - Detect virtual environments (venv, virtualenv, conda, poetry, uv)
   - Find pytest executable in the environment
   - Handle cases where pytest isn't installed

### Phase 3: TDD Validation Logic
1. **Python-Specific Prompts**
   - Adapt TDD-Guard prompts for Python
   - Create phase detection logic
   - Map Python test failures to allowed implementations

2. **Update TDDValidator**
   - Load test results from FileStorage
   - Include test results in validation context
   - Implement phase-aware validation

### Phase 4: Integration
1. **Pytest Configuration**
   - Create setup script to add reporter to pytest.ini/pyproject.toml
   - Handle existing pytest configurations
   - Provide clear setup instructions

2. **End-to-End Testing**
   - Test complete Red-Green-Refactor cycle
   - Verify blocking/allowing decisions
   - Test edge cases

## Key Differences from TDD-Guard

1. **Language**: Python instead of TypeScript/JavaScript
2. **Test Framework**: Pytest instead of Vitest
3. **Integration**: Works with existing claude-code-adk-validator
4. **Multi-Stage**: Part of a larger validation pipeline

## Success Criteria

1. **Red Phase**: Can write failing tests without being blocked
2. **Green Phase**: Can implement minimal code to pass specific test
3. **Refactor Phase**: Can refactor when tests are green
4. **Violations**: Blocks multiple tests, premature implementation, excessive code

## Next Steps

1. Create Python environment detector
2. Write Python-specific TDD prompts
3. Update TDDValidator to use test results
4. Create pytest configuration setup
5. Test complete workflow

## Example Workflow

```python
# 1. Red Phase - Write failing test (ALLOWED)
def test_calculator_add():
    calc = Calculator()
    assert calc.add(2, 3) == 5  # Fails: Calculator not defined

# 2. Run test, capture failure
# pytest → PytestReporter → FileStorage → test.json

# 3. Green Phase - Minimal implementation (ALLOWED)
class Calculator:
    def add(self, a, b):
        return a + b  # Validator sees test failure, allows this

# 4. Refactor Phase - Improve code (ALLOWED when tests pass)
class Calculator:
    """A simple calculator class."""
    def add(self, a: int, b: int) -> int:
        """Add two numbers."""
        return a + b
```

## Critical Insight

The v1.2.1 limitation (blocking all Python implementations) exists because:
- Current validator has no access to test results
- Cannot determine if we're in Red, Green, or Refactor phase
- Assumes all implementation is premature

With test result storage, the validator can make informed decisions based on:
- Whether tests exist
- What specific failures occurred
- Current TDD phase

This transforms the validator from a blunt instrument to a sophisticated TDD coach.