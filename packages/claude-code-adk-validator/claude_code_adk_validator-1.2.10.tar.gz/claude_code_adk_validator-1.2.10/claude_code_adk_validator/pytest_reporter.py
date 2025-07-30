"""Pytest reporter plugin for capturing test results."""

from typing import Dict, List, Any, Optional
from collections import defaultdict
from claude_code_adk_validator.file_storage import FileStorage


class PytestReporter:
    """Pytest plugin that captures test results in TDD Guard format."""

    def __init__(self, data_dir: Optional[str] = None):
        self.test_modules: Dict[str, Dict[str, Any]] = defaultdict(
            lambda: {"moduleId": None, "tests": []}
        )
        # Always create FileStorage instance to save results
        self.storage = FileStorage(data_dir or ".claude/claude-code-adk-validator/data")

    def pytest_runtest_logreport(self, report: Any) -> None:
        """Hook called for test report processing."""
        if report.when == "call":
            module_id = report.nodeid.split("::")[0]
            test_name = report.nodeid.split("::")[-1]

            self.test_modules[module_id]["moduleId"] = module_id

            test_result = {
                "name": test_name,
                "fullName": report.nodeid,
                "state": "failed" if report.failed else "passed",
                "errors": [],
            }

            if report.failed:
                test_result["errors"].append({"message": report.longreprtext})

            self.test_modules[module_id]["tests"].append(test_result)

    def pytest_sessionfinish(self, session: Any, exitstatus: int) -> None:
        """Hook called when test session finishes."""
        if self.storage:
            results = self.get_test_results()
            self.storage.save_test_results(results)

    def get_test_results(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get captured test results in expected format."""
        return {"testModules": list(self.test_modules.values())}
