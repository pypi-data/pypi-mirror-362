"""Write operation analysis for Python TDD validation."""

WRITE_ANALYSIS = """
## Write Operation Analysis

You are reviewing a WRITE operation that creates a new Python file.

### For Test Files:
Evaluate if the new test file:
1. Contains exactly ONE test function/method initially
   - Count only functions starting with `test_` or methods in TestCase classes
   - ONE test means literally one `def test_*():` function
   - Imports, setup code, fixtures, and helper functions DON'T count as tests
2. Has a test that will fail (not pass immediately)
3. Tests a specific behavior or requirement
4. Uses appropriate test framework (pytest/unittest)
5. Follows Python test naming conventions

**IMPORTANT**: Only count actual test functions:
- `def test_something():` → This is a test (count it)
- `def helper_function():` → NOT a test (don't count)
- `@pytest.fixture` → NOT a test (don't count)
- Class-level setup → NOT a test (don't count)

**Example of a VALID single-test file:**
```python
# test_hello.py
import pytest

def test_hello_returns_greeting():
    # Test that hello function returns correct greeting
    from hello import hello
    assert hello() == "Hello, World!"
```
This has exactly ONE test function, so it's allowed.

**Red Flags**:
- Multiple test functions in initial file (more than one `def test_*():`)
- Tests that would pass without implementation
- Empty or placeholder tests (`pass`, `...`, `assert True`)
- Tests without meaningful assertions

### For Implementation Files:
Evaluate if the new implementation file:
1. Is being created in response to a failing test
2. Contains minimal code to address the test failure
3. Doesn't include speculative or untested features
4. Has appropriate module structure

**Required Context**:
- Evidence of failing test output
- Clear connection between test failure and implementation

### Common Patterns:

**Allowed Writes**:
- Test file with one failing test
- Empty `__init__.py` for package creation
- Minimal implementation to fix `ModuleNotFoundError`
- Stub class/function to fix `NameError`
- Configuration files (non-code)

**TDD Violations**:
- Implementation without visible failing tests
- Test file with multiple tests
- Complex implementation beyond test requirements
- Feature-complete code without iterative development

### File Types:

**Always Allowed**:
- `test_*.py`, `*_test.py` (with one test)
- `conftest.py` (pytest configuration)
- `__init__.py` (package markers)
- Non-Python files (`.md`, `.txt`, `.yml`, etc.)

**Requires Test Context**:
- Any `.py` file that's not a test
- Module implementations
- Class definitions
- Business logic

The key question: Is there a failing test that justifies creating this file?
"""
