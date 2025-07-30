"""Core TDD principles adapted for Python development."""

TDD_CORE_PRINCIPLES = """
## Test-Driven Development (TDD) Core Principles

TDD follows the Red-Green-Refactor cycle:

### RED Phase: Write a Failing Test First
- Write ONE test that describes the desired behavior
- The test MUST fail initially (proves the test actually tests something)
- Test failure should clearly indicate what needs to be implemented
- Common Python test frameworks: pytest, unittest

### GREEN Phase: Make the Test Pass
- Write the MINIMAL implementation needed to pass the failing test
- Implementation should directly address the specific test failure
- Avoid over-engineering or adding unnecessary features
- Focus only on making the current test pass

### REFACTOR Phase: Improve Code Quality
- With tests passing, refactor code for better design
- Remove duplication, improve naming, simplify logic
- Tests must continue to pass after refactoring
- This ensures behavior remains correct

### Critical Rules:

1. **One Test at a Time**: Only add one failing test before implementing
   - ONE test = exactly one `def test_*():` function
   - Helper functions, fixtures, imports don't count as tests
   
   **Example - GOOD (one test):**
   ```python
   import pytest
   
   def test_calculator_add():
       from calculator import add
       assert add(2, 3) == 5
   ```
   
   **Example - BAD (multiple tests):**
   ```python
   def test_add():
       assert add(2, 3) == 5
   
   def test_subtract():  # Second test - NOT ALLOWED initially
       assert subtract(5, 3) == 2
   ```

2. **Test Must Fail First**: A test that passes immediately indicates:
   - The feature already exists (no new development needed)
   - The test doesn't actually test anything (bad test)
   
3. **Minimal Implementation**: Implement only enough to pass the current failing test

### Common Python Test Patterns:

**Test Discovery**:
- Files: `test_*.py` or `*_test.py`
- Functions: `def test_*()` or methods in TestCase classes
- Directories: `tests/`, `test/`, or alongside code

**Assertions**:
- pytest: `assert expression` with automatic introspection
- unittest: `self.assertEqual()`, `self.assertTrue()`, etc.

**Test Organization**:
- Arrange: Set up test data and preconditions
- Act: Execute the code being tested
- Assert: Verify the expected outcome

### Python-Specific TDD Considerations:

1. **Import Errors**: `ModuleNotFoundError` indicates missing module - create empty `__init__.py` or module file
2. **Name Errors**: `NameError: name 'X' is not defined` - create class/function/variable X
3. **Attribute Errors**: `AttributeError: 'X' object has no attribute 'Y'` - add method/property Y to class X
4. **Type Errors**: Often indicate missing parameters or wrong types - adjust signatures
5. **Assertion Errors**: The actual test failure - implement logic to satisfy assertion

### File Type Rules:

**Always Allowed**:
- Creating/editing test files (`test_*.py`, `*_test.py`)
- Creating empty `__init__.py` files
- Creating test fixtures and utilities

**Requires Failing Test**:
- Creating implementation files (non-test `.py` files)
- Adding new functions/classes to existing files
- Modifying existing implementation logic

**Configuration/Documentation**:
- `setup.py`, `pyproject.toml`, `requirements.txt` - allowed without tests
- `README.md`, documentation files - allowed without tests
- Configuration files (`.ini`, `.yml`, `.json`) - allowed without tests
"""
