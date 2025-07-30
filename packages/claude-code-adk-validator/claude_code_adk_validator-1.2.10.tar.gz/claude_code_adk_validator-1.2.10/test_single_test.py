"""Test file with exactly one test to check TDD validator."""


def test_hello_world():
    """Test that hello function returns greeting."""
    from hello import hello
    assert hello() == "Hello, World!"