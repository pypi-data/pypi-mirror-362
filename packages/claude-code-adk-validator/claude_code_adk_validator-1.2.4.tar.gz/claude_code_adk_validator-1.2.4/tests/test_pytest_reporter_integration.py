"""Integration tests for pytest reporter with file storage."""

import tempfile
from unittest.mock import Mock
from claude_code_adk_validator.pytest_reporter import PytestReporter
from claude_code_adk_validator.file_storage import FileStorage


def test_pytest_reporter_saves_results_to_file_storage():
    """Test that PytestReporter can save results using FileStorage."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create reporter with file storage
        storage = FileStorage(data_dir=temp_dir)
        reporter = PytestReporter()

        # Simulate a failing test
        report1 = Mock()
        report1.when = "call"
        report1.failed = True
        report1.nodeid = "test_calculator.py::test_add"
        report1.longreprtext = "AssertionError: assert 2 == 3"

        # Simulate a passing test
        report2 = Mock()
        report2.when = "call"
        report2.failed = False
        report2.nodeid = "test_calculator.py::test_subtract"

        # Process the reports
        reporter.pytest_runtest_logreport(report1)
        reporter.pytest_runtest_logreport(report2)

        # Save results to storage
        results = reporter.get_test_results()
        storage.save_test_results(results)

        # Load and verify
        loaded_results = storage.load_test_results()
        assert loaded_results == results
        assert len(loaded_results["testModules"]) == 1
        assert len(loaded_results["testModules"][0]["tests"]) == 2

        # Check specific test results
        tests = loaded_results["testModules"][0]["tests"]
        failing_test = [t for t in tests if t["name"] == "test_add"][0]
        passing_test = [t for t in tests if t["name"] == "test_subtract"][0]

        assert failing_test["state"] == "failed"
        assert "AssertionError" in failing_test["errors"][0]["message"]
        assert passing_test["state"] == "passed"
        assert len(passing_test["errors"]) == 0
