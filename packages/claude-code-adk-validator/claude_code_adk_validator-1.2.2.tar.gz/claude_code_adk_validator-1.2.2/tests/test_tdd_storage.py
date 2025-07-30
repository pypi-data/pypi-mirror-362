from claude_code_adk_validator.storage.tdd_storage import TDDStorage


def test_tdd_storage_exists():
    """Test that TDDStorage class exists."""
    storage = TDDStorage()
    assert storage is not None
