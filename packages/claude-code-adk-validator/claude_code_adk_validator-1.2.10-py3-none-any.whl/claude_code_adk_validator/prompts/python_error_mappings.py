"""Python error mappings for TDD implementation guidance."""

PYTHON_ERROR_MAPPINGS = """
## Python Error to Implementation Mappings

When tests fail with specific Python errors, here's the minimal implementation allowed:

### ModuleNotFoundError / ImportError
```
ModuleNotFoundError: No module named 'calculator'
```
**Allowed**: Create empty module file or `__init__.py`
```python
# calculator.py or calculator/__init__.py
# Empty file is sufficient
```

### NameError
```
NameError: name 'Calculator' is not defined
```
**Allowed**: Create empty class definition
```python
class Calculator:
    pass
```

```
NameError: name 'add' is not defined  
```
**Allowed**: Create function stub
```python
def add():
    pass
```

### AttributeError
```
AttributeError: 'Calculator' object has no attribute 'add'
```
**Allowed**: Add method stub to class
```python
class Calculator:
    def add(self):
        pass
```

### TypeError
```
TypeError: add() takes 0 positional arguments but 2 were given
```
**Allowed**: Update function signature
```python
def add(a, b):
    pass
```

```
TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'
```
**Allowed**: Return appropriate type
```python
def add(a, b):
    return 0  # Minimal implementation
```

### AssertionError
```
AssertionError: assert 4 == 5
```
**Allowed**: Implement minimal logic to pass assertion
```python
def add(a, b):
    return a + b  # Only what's needed
```

### ValueError
```
ValueError: invalid literal for int() with base 10: 'abc'
```
**Allowed**: Add minimal validation
```python
def parse_number(s):
    try:
        return int(s)
    except ValueError:
        raise ValueError(f"Invalid number: {s}")
```

### KeyError / IndexError
```
KeyError: 'name'
```
**Allowed**: Return minimal valid structure
```python
def get_user():
    return {"name": ""}  # Minimal dict
```

### General Rules:
1. **Fix only the immediate error** - don't anticipate future failures
2. **Use minimal values** - empty strings, 0, empty lists, None
3. **Don't add validation** - unless the test specifically fails on it
4. **Don't add error handling** - unless the test expects it
5. **Keep signatures simple** - only what the failing test requires

### Progressive Implementation:
1. First failure: `NameError` → Create empty class/function
2. Second failure: `TypeError` (arguments) → Add parameters
3. Third failure: `TypeError` (return) → Return minimal value
4. Fourth failure: `AssertionError` → Implement actual logic

This ensures each implementation step is driven by a specific test failure.
"""
