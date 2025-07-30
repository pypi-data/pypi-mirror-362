"""Tests for FileStorage class."""

import json
import tempfile
from pathlib import Path
from claude_code_adk_validator.file_storage import FileStorage


def test_file_storage_saves_and_loads_test_results():
    """Test that FileStorage can save and load test results."""
    with tempfile.TemporaryDirectory() as temp_dir:
        storage = FileStorage(data_dir=temp_dir)

        test_results = {
            "testModules": [
                {
                    "moduleId": "test_calculator.py",
                    "tests": [
                        {
                            "name": "test_add",
                            "fullName": "test_calculator.py::test_add",
                            "state": "failed",
                            "errors": [{"message": "AssertionError: 2 != 3"}],
                        }
                    ],
                }
            ]
        }

        # Save test results
        storage.save_test_results(test_results)

        # Load test results
        loaded_results = storage.load_test_results()

        assert loaded_results == test_results

        # Verify file exists
        test_file = Path(temp_dir) / "test.json"
        assert test_file.exists()

        # Verify content
        with open(test_file) as f:
            file_content = json.load(f)
        assert file_content == test_results


def test_file_storage_returns_none_when_no_results_exist():
    """Test that FileStorage returns None when test results don't exist."""
    with tempfile.TemporaryDirectory() as temp_dir:
        storage = FileStorage(data_dir=temp_dir)

        # Load without saving first
        results = storage.load_test_results()

        assert results is None
