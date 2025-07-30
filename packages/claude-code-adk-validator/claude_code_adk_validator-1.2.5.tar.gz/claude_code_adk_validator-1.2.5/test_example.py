"""Example test file to demonstrate TDD workflow with pytest reporter."""


def test_calculator_multiply():
    """Test that multiply function multiplies two numbers."""
    from calculator import multiply
    assert multiply(3, 4) == 12