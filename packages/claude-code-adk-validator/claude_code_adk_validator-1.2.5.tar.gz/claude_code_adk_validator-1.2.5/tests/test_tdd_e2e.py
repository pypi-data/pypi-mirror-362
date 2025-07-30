"""End-to-end tests for TDD validation workflow."""

import json
import subprocess
import tempfile
import os
import shutil
from pathlib import Path


class TestTDDEndToEnd:
    """End-to-end tests for TDD validation workflow."""

    def setup_method(self):
        """Setup test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)

        # Create minimal project structure
        self.data_dir = Path(".claude/claude-code-adk-validator/data")
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Create test results file path
        self.test_results_file = self.data_dir / "test.json"

    def teardown_method(self):
        """Cleanup test environment."""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    def run_validator(self, tool_name: str, tool_input: dict) -> dict:
        """Run TDD validator and return result."""
        hook_input = {"tool_name": tool_name, "tool_input": tool_input}

        # Change to original directory to run validator
        os.chdir(self.original_cwd)

        process = subprocess.Popen(
            ["uv", "run", "python", "-m", "claude_code_adk_validator", "--stage=tdd"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd="/home/jihun/code_base/jk_hooks_gemini_challenge",
        )

        stdout, stderr = process.communicate(input=json.dumps(hook_input))

        # Return to test directory
        os.chdir(self.test_dir)

        return {"exit_code": process.returncode, "stdout": stdout, "stderr": stderr}

    def create_test_results(self, test_modules: list):
        """Create test results file."""
        test_results = {"testModules": test_modules}
        with open(self.test_results_file, "w") as f:
            json.dump(test_results, f, indent=2)

    def test_single_test_file_approved(self):
        """Test that single test file is approved."""
        result = self.run_validator(
            "Write",
            {
                "file_path": "test_hello.py",
                "content": '''def test_hello_world():
    """Test hello function."""
    from hello import hello
    assert hello() == "Hello, World!"''',
            },
        )

        assert result["exit_code"] == 0

        # Parse JSON response
        response = json.loads(result["stdout"])
        assert response["continue"] is True
        assert response["decision"] == "approve"
        assert "single test" in response["reason"]
        assert "TDD Red phase" in response["reason"]

    def test_multiple_tests_blocked(self):
        """Test that multiple tests in new file are blocked."""
        result = self.run_validator(
            "Write",
            {
                "file_path": "test_calculator.py",
                "content": """def test_add():
    assert add(2, 3) == 5

def test_subtract():
    assert subtract(5, 3) == 2""",
            },
        )

        assert result["exit_code"] == 2
        assert "Found 2 tests" in result["stderr"]
        assert "ONE test at a time" in result["stderr"]

    def test_implementation_without_tests_blocked(self):
        """Test that implementation without test results is blocked."""
        # Ensure no test results exist
        if self.test_results_file.exists():
            self.test_results_file.unlink()

        result = self.run_validator(
            "Write",
            {
                "file_path": "calculator.py",
                "content": """def add(a, b):
    return a + b""",
            },
        )

        assert result["exit_code"] == 2
        assert "No test results found" in result["stderr"]
        assert "set up pytest" in result["stderr"]

    def test_implementation_with_failing_tests_approved(self):
        """Test that implementation with failing tests is approved."""
        # Create failing test results
        self.create_test_results(
            [
                {
                    "moduleId": "test_calculator.py",
                    "tests": [
                        {
                            "name": "test_add",
                            "fullName": "test_calculator.py::test_add",
                            "state": "failed",
                            "errors": [
                                {"message": "NameError: name 'add' is not defined"}
                            ],
                        }
                    ],
                }
            ]
        )

        result = self.run_validator(
            "Write",
            {
                "file_path": "calculator.py",
                "content": """def add(a, b):
    return a + b""",
            },
        )

        assert result["exit_code"] == 0

        response = json.loads(result["stdout"])
        assert response["continue"] is True
        assert response["decision"] == "approve"
        assert "failing tests" in response["reason"]
        assert "Green phase" in response["reason"]

    def test_implementation_with_passing_tests_blocked(self):
        """Test that implementation with passing tests is blocked."""
        # Create passing test results
        self.create_test_results(
            [
                {
                    "moduleId": "test_calculator.py",
                    "tests": [
                        {
                            "name": "test_add",
                            "fullName": "test_calculator.py::test_add",
                            "state": "passed",
                            "errors": [],
                        }
                    ],
                }
            ]
        )

        result = self.run_validator(
            "Write",
            {
                "file_path": "new_feature.py",
                "content": """def multiply(a, b):
    return a * b""",
            },
        )

        assert result["exit_code"] == 2
        assert "All tests are passing" in result["stderr"]
        assert "failing test before adding new implementation" in result["stderr"]

    def test_edit_with_passing_tests_refactor_approved(self):
        """Test that editing implementation with passing tests is approved (refactor)."""
        # Create passing test results
        self.create_test_results(
            [
                {
                    "moduleId": "test_calculator.py",
                    "tests": [
                        {
                            "name": "test_add",
                            "fullName": "test_calculator.py::test_add",
                            "state": "passed",
                            "errors": [],
                        }
                    ],
                }
            ]
        )

        result = self.run_validator(
            "Edit",
            {
                "file_path": "calculator.py",
                "old_string": "def add(a, b):\\n    return a + b",
                "new_string": 'def add(a: int, b: int) -> int:\\n    """Add two numbers."""\\n    return a + b',
            },
        )

        assert result["exit_code"] == 0

        response = json.loads(result["stdout"])
        assert response["continue"] is True
        assert response["decision"] == "approve"
        assert "Refactor phase" in response["reason"]

    def test_test_file_with_setup_not_counted(self):
        """Test that setup functions don't count as tests."""
        result = self.run_validator(
            "Write",
            {
                "file_path": "test_with_setup.py",
                "content": '''import pytest
from unittest.mock import Mock

def setup_module():
    """Setup for tests."""
    pass

@pytest.fixture
def mock_data():
    return Mock()

def test_hello_world():
    """Test hello world function."""
    from hello import hello
    assert hello() == "Hello, World!"''',
            },
        )

        assert result["exit_code"] == 0

        response = json.loads(result["stdout"])
        assert response["continue"] is True
        assert response["decision"] == "approve"
        assert "single test" in response["reason"]

    def test_empty_test_file_warned(self):
        """Test that empty test file gets warning."""
        result = self.run_validator(
            "Write",
            {
                "file_path": "test_empty.py",
                "content": '''"""Empty test file."""
import pytest''',
            },
        )

        assert result["exit_code"] == 0

        response = json.loads(result["stdout"])
        assert response["continue"] is True
        assert response["decision"] == "warn"
        assert "no test functions" in response["reason"]

    def test_conftest_file_approved(self):
        """Test that conftest.py files are approved."""
        result = self.run_validator(
            "Write",
            {
                "file_path": "conftest.py",
                "content": """import pytest

@pytest.fixture
def sample_data():
    return {"key": "value"}""",
            },
        )

        assert result["exit_code"] == 0

        response = json.loads(result["stdout"])
        assert response["continue"] is True
        assert response["decision"] == "approve"
        assert "conftest.py" in response["reason"]

    def test_non_python_file_skipped(self):
        """Test that non-Python files skip TDD validation."""
        result = self.run_validator(
            "Write",
            {
                "file_path": "README.md",
                "content": """# My Project

This is a test project.""",
            },
        )

        assert result["exit_code"] == 0

        response = json.loads(result["stdout"])
        assert response["continue"] is True
        assert response["decision"] == "approve"
        assert "Non-programming file" in response["reason"]

    def test_init_file_approved(self):
        """Test that __init__.py files are approved."""
        result = self.run_validator(
            "Write",
            {
                "file_path": "__init__.py",
                "content": '''"""Package initialization."""''',
            },
        )

        assert result["exit_code"] == 0

        response = json.loads(result["stdout"])
        assert response["continue"] is True
        assert response["decision"] == "approve"
        assert "Non-programming file" in response["reason"]

    def test_quality_issues_warned(self):
        """Test that test quality issues are warned."""
        result = self.run_validator(
            "Write",
            {
                "file_path": "test_quality.py",
                "content": '''def test_placeholder():
    """Placeholder test."""
    # TODO: implement actual test
    assert True''',
            },
        )

        assert result["exit_code"] == 0

        response = json.loads(result["stdout"])
        assert response["continue"] is True
        assert response["decision"] == "warn"
        assert "quality concerns" in response["reason"]

    def test_unittest_style_test_approved(self):
        """Test that unittest style tests are approved."""
        result = self.run_validator(
            "Write",
            {
                "file_path": "test_unittest.py",
                "content": '''import unittest

class TestCalculator(unittest.TestCase):
    def test_add(self):
        """Test addition."""
        from calculator import add
        self.assertEqual(add(2, 3), 5)''',
            },
        )

        assert result["exit_code"] == 0

        response = json.loads(result["stdout"])
        assert response["continue"] is True
        assert response["decision"] == "approve"
        assert "single test" in response["reason"]
