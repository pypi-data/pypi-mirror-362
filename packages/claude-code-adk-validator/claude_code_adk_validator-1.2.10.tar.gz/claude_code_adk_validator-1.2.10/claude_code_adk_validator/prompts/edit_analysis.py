"""Edit operation analysis for Python TDD validation."""

EDIT_ANALYSIS = """
## Edit Operation Analysis

You are reviewing an EDIT operation that modifies existing Python code.

### For Test Files:
Evaluate if the edit:
1. Adds only ONE test at a time (multiple tests = violation)
2. Creates a meaningful test that will fail initially
3. Tests a specific, focused behavior
4. Uses proper assertions (not `assert True` or empty tests)

### For Implementation Files:
Evaluate if the edit:
1. Is justified by a currently failing test
2. Makes minimal changes to pass the specific test  
3. Doesn't add functionality beyond what the test requires
4. Maintains existing test coverage (refactoring is ok if tests stay green)

### Common Edit Patterns:

**Allowed Edits**:
- Adding one test function to a test file
- Implementing minimal code to fix a failing test
- Refactoring code while tests remain green
- Fixing bugs identified by failing tests
- Updating imports/dependencies required by tests

**TDD Violations**:
- Adding multiple tests in one edit
- Implementing features without failing tests
- Making changes unrelated to current test failures
- Removing or disabling tests
- Adding complex logic not required by tests

### Phase Detection:
- **RED**: Test file edited to add new failing test
- **GREEN**: Implementation edited to make tests pass
- **REFACTOR**: Code improved while all tests stay green

Remember: The edit should advance the TDD cycle by exactly one step.
"""
