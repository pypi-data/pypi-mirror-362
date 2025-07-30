import json
import tempfile
from pathlib import Path
from unittest.mock import Mock
from claude_code_adk_validator.pytest_reporter import PytestReporter


def test_pytest_reporter_captures_test_failure():
    """Test that PytestReporter captures failing test information."""
    reporter = PytestReporter()

    # Mock a failing test report
    report = Mock()
    report.when = "call"
    report.failed = True
    report.nodeid = "test_calculator.py::test_add"
    report.longreprtext = "AttributeError: module 'calculator' has no attribute 'add'"

    # Process the report
    reporter.pytest_runtest_logreport(report)

    # Get the captured results
    results = reporter.get_test_results()

    assert len(results["testModules"]) == 1
    assert results["testModules"][0]["moduleId"] == "test_calculator.py"
    assert len(results["testModules"][0]["tests"]) == 1

    test = results["testModules"][0]["tests"][0]
    assert test["name"] == "test_add"
    assert test["fullName"] == "test_calculator.py::test_add"
    assert test["state"] == "failed"
    assert "AttributeError" in test["errors"][0]["message"]


def test_pytest_reporter_saves_results_on_session_finish():
    """Test that PytestReporter saves results when session finishes."""
    with tempfile.TemporaryDirectory() as temp_dir:
        reporter = PytestReporter(data_dir=temp_dir)

        # Mock a test report
        report = Mock()
        report.when = "call"
        report.failed = True
        report.nodeid = "test_example.py::test_something"
        report.longreprtext = "Test failed"

        # Process the report
        reporter.pytest_runtest_logreport(report)

        # Simulate session finish
        reporter.pytest_sessionfinish(None, 0)

        # Check that results were saved
        test_file = Path(temp_dir) / "test.json"
        assert test_file.exists()

        # Verify content
        with open(test_file) as f:
            saved_results = json.load(f)

        assert len(saved_results["testModules"]) == 1
        assert saved_results["testModules"][0]["moduleId"] == "test_example.py"
