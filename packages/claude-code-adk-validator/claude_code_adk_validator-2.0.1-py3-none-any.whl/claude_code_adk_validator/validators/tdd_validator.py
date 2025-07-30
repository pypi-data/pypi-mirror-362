"""TDD-focused validator inspired by tdd-guard's sophisticated TDD analysis."""

import json
import subprocess
import os
import re
from typing import Dict, Any, List, Optional, TypedDict
from ..hook_response import HookResponse, ResponseBuilder, RiskLevel, ValidationStage


class TestModuleResult(TypedDict):
    passed: int
    failed: int
    tests: List[str]


class TestResultProcessor:
    """Process pytest JSON output similar to tdd-guard's TestResultsProcessor."""

    def process_pytest_json(self, json_data: str) -> str:
        """Process pytest JSON output into formatted test results."""
        try:
            data = json.loads(json_data)

            if not data.get("tests"):
                return "No test results found."

            # Format similar to tdd-guard's output
            modules: Dict[str, TestModuleResult] = {}
            for test in data["tests"]:
                file_path = test.get("nodeid", "").split("::")[0]
                if file_path not in modules:
                    modules[file_path] = {"passed": 0, "failed": 0, "tests": []}

                if test.get("outcome") == "passed":
                    modules[file_path]["passed"] += 1
                    modules[file_path]["tests"].append(
                        f"   ✓ {test.get('test_name', 'unknown')} 0ms"
                    )
                elif test.get("outcome") == "failed":
                    modules[file_path]["failed"] += 1
                    error_msg = test.get("call", {}).get("longrepr", "Unknown error")
                    modules[file_path]["tests"].append(
                        f"   × {test.get('test_name', 'unknown')} 0ms"
                    )
                    modules[file_path]["tests"].append(f"     → {error_msg}")

            # Format output
            output_lines = []
            total_passed = 0
            total_failed = 0

            for file_path, results in modules.items():
                test_count = results["passed"] + results["failed"]
                total_passed += results["passed"]
                total_failed += results["failed"]

                if results["failed"] == 0:
                    output_lines.append(f" ✓ {file_path} ({test_count} tests) 0ms")
                else:
                    output_lines.append(
                        f" ❯ {file_path} ({test_count} tests | {results['failed']} failed) 0ms"
                    )
                    output_lines.extend(results["tests"])

            # Summary
            if total_failed > 0:
                output_lines.append(
                    f" Test Files  {len([m for m in modules.values() if m['failed'] > 0])} failed | {len([m for m in modules.values() if m['failed'] == 0])} passed ({len(modules)})"
                )
                output_lines.append(
                    f"      Tests  {total_failed} failed | {total_passed} passed ({total_failed + total_passed})"
                )
            else:
                output_lines.append(
                    f" Test Files  {len(modules)} passed ({len(modules)})"
                )
                output_lines.append(
                    f"      Tests  {total_passed} passed ({total_passed})"
                )

            return "\n".join(output_lines)

        except (json.JSONDecodeError, KeyError) as e:
            return f"Error processing test results: {e}"


class TDDValidator:
    """TDD validation using patterns from tdd-guard with pytest integration."""

    def __init__(self) -> None:
        self.test_processor = TestResultProcessor()

    def get_pytest_results(self) -> Optional[str]:
        """Run pytest and get JSON results."""
        try:
            # Try to run pytest with JSON output
            subprocess.run(
                [
                    "uv",
                    "run",
                    "pytest",
                    "--json-report",
                    "--json-report-file=/tmp/pytest_results.json",
                    "--tb=short",
                ],
                capture_output=True,
                text=True,
                timeout=30,
            )

            # Read the JSON report file
            if os.path.exists("/tmp/pytest_results.json"):
                with open("/tmp/pytest_results.json", "r") as f:
                    json_data = f.read()
                result = self.test_processor.process_pytest_json(json_data)
                return result if isinstance(result, str) else None

        except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
            pass

        return None

    def is_test_file(self, file_path: str) -> bool:
        """Determine if file is a test file based on comprehensive path patterns."""
        file_name = os.path.basename(file_path)
        path_lower = file_path.lower()

        # Enhanced test file patterns
        test_patterns = [
            # Standard pytest/unittest patterns
            file_name.startswith("test_"),
            file_name.endswith("_test.py"),
            file_name.endswith("_tests.py"),
            file_name.endswith(".test.py"),
            # Directory-based patterns
            "/test/" in path_lower,
            "/tests/" in path_lower,
            "/testing/" in path_lower,
            # Pytest-specific patterns
            file_name.startswith("conftest.py"),
            # Framework-specific patterns
            "test_" in file_name and file_name.endswith(".py"),
            # Common test directory structures
            path_lower.endswith("/test.py"),
            "spec_" in file_name and file_name.endswith(".py"),
            file_name.endswith("_spec.py"),
        ]

        return any(test_patterns)

    def count_tests_in_content(self, content: str) -> int:
        """Count number of test functions/methods in content with comprehensive patterns."""
        test_count = 0

        # Pattern 1: Standard pytest/unittest test functions
        test_functions = re.findall(r"^\s*def test_\w+\s*\(", content, re.MULTILINE)
        test_count += len(test_functions)

        # Pattern 2: Async test functions
        async_test_functions = re.findall(
            r"^\s*async def test_\w+\s*\(", content, re.MULTILINE
        )
        test_count += len(async_test_functions)

        # Pattern 3: unittest TestCase methods
        unittest_methods = re.findall(
            r"^\s*def test\w+\s*\(self", content, re.MULTILINE
        )
        test_count += len(unittest_methods)

        # Pattern 4: pytest fixtures (can be considered test setup)
        # Don't count fixtures as tests, but detect them for context
        re.findall(r"@pytest\.fixture\s*\n\s*def \w+", content, re.MULTILINE)

        # Pattern 5: Spec-style test functions
        spec_tests = re.findall(
            r"^\s*def (should_|when_|it_|spec_)\w+\s*\(", content, re.MULTILINE
        )
        test_count += len(spec_tests)

        return test_count

    def analyze_test_quality(self, content: str) -> Dict[str, Any]:
        """Analyze test quality and detect potential TDD violations."""
        analysis = {
            "empty_tests": [],
            "placeholder_tests": [],
            "missing_assertions": [],
            "has_fixtures": False,
            "has_setup_teardown": False,
            "test_complexity": "low",
        }

        lines = content.split("\n")
        current_test = None
        test_content: List[str] = []

        for i, line in enumerate(lines):
            # Detect test function start
            if re.match(
                r"^\s*(async\s+)?def test_\w+|def (should_|when_|it_|spec_)\w+", line
            ):
                if current_test:
                    self._analyze_single_test(current_test, test_content, analysis)
                current_test = line.strip()
                test_content = []
            elif current_test and (line.startswith("    ") or line.strip() == ""):
                test_content.append(line)
            elif current_test and not line.startswith(" "):
                # End of current test
                self._analyze_single_test(current_test, test_content, analysis)
                current_test = None
                test_content = []

        # Analyze last test
        if current_test:
            self._analyze_single_test(current_test, test_content, analysis)

        # Detect fixtures and setup/teardown
        analysis["has_fixtures"] = bool(re.search(r"@pytest\.fixture", content))
        analysis["has_setup_teardown"] = bool(
            re.search(r"def (setUp|tearDown|setup_method|teardown_method)", content)
        )

        return analysis

    def _analyze_single_test(
        self, test_name: str, test_lines: List[str], analysis: Dict[str, Any]
    ) -> None:
        """Analyze a single test function for quality issues."""
        test_body = "\n".join(test_lines).strip()

        # Check for empty tests
        if not test_body or test_body in ["pass", "...", "pass\n", "...\n"]:
            analysis["empty_tests"].append(test_name)

        # Check for placeholder patterns
        placeholder_patterns = [
            r"# TODO",
            r"# FIXME",
            r"# XXX",
            r"pytest\.skip",
            r"pytest\.xfail",
            r"raise NotImplementedError",
            r"assert True",
            r"assert 1 == 1",
        ]

        for pattern in placeholder_patterns:
            if re.search(pattern, test_body, re.IGNORECASE):
                analysis["placeholder_tests"].append(test_name)
                break

        # Check for missing assertions
        assertion_patterns = [
            r"assert\s+",
            r"self\.assert",
            r"self\.assertEqual",
            r"self\.assertTrue",
            r"self\.assertFalse",
            r"self\.assertRaises",
            r"expect\(",
            r"should\.",
        ]

        has_assertion = any(
            re.search(pattern, test_body, re.IGNORECASE)
            for pattern in assertion_patterns
        )
        if not has_assertion and test_name not in analysis["empty_tests"]:
            analysis["missing_assertions"].append(test_name)

    def detect_test_framework(self, content: str) -> str:
        """Detect which testing framework is being used."""
        if "import unittest" in content or "from unittest" in content:
            return "unittest"
        elif "import pytest" in content or "@pytest." in content:
            return "pytest"
        elif "import nose" in content or "from nose" in content:
            return "nose"
        elif re.search(r"def test_\w+", content):
            return "pytest"  # Default assumption for test_ functions
        else:
            return "unknown"

    def validate_write_operation(
        self, file_path: str, content: str, context: str = ""
    ) -> HookResponse:
        """Validate Write operations following tdd-guard's TDD principles."""

        if self.is_test_file(file_path):
            # Creating a test file - check TDD principles with enhanced analysis
            test_count = self.count_tests_in_content(content)
            test_quality = self.analyze_test_quality(content)
            framework = self.detect_test_framework(content)

            # Check for multiple tests violation
            if test_count > 1:
                return ResponseBuilder.block(
                    reason="TDD Violation: Multiple tests in new test file. TDD requires writing ONE test at a time.",
                    risk_level=RiskLevel.HIGH,
                    suggestions=[
                        "Write only one test initially",
                        "Follow Red-Green-Refactor cycle",
                        "Add additional tests one at a time",
                    ],
                    educational_notes=[
                        "TDD Core Principle: One failing test at a time",
                        "This ensures focused development and proper test-driven design",
                        f"Detected {framework} framework with {test_count} tests",
                    ],
                    validation_stage=ValidationStage.TDD,
                    tool_name="Write",
                    detected_patterns=["multiple_tests", f"framework_{framework}"],
                )

            # Check for test quality issues
            if test_count == 1:
                quality_issues = []
                if test_quality["empty_tests"]:
                    quality_issues.append("Empty test detected")
                if test_quality["placeholder_tests"]:
                    quality_issues.append("Placeholder test detected")
                if test_quality["missing_assertions"]:
                    quality_issues.append("Test missing assertions")

                if quality_issues:
                    return ResponseBuilder.warn(
                        reason=f"Test quality concerns: {', '.join(quality_issues)}",
                        risk_level=RiskLevel.MEDIUM,
                        suggestions=[
                            "Add meaningful assertions to your test",
                            "Ensure test actually validates expected behavior",
                            "Replace placeholder code with real test logic",
                        ],
                        educational_notes=[
                            "TDD Red Phase: Tests should fail for the right reasons",
                            "Empty or placeholder tests don't drive development effectively",
                        ],
                        validation_stage=ValidationStage.TDD,
                        tool_name="Write",
                        detected_patterns=["test_quality_issues"],
                    )

                return ResponseBuilder.approve(
                    reason=f"Creating {framework} test file with single test - follows TDD Red phase",
                    risk_level=RiskLevel.LOW,
                    educational_notes=[
                        "Good TDD practice: Starting with one failing test"
                    ],
                    validation_stage=ValidationStage.TDD,
                    tool_name="Write",
                )

            # Handle case with no tests (might be conftest.py or test utilities)
            elif test_count == 0:
                if "conftest" in file_path:
                    return ResponseBuilder.approve(
                        reason="Creating pytest configuration file (conftest.py)",
                        risk_level=RiskLevel.LOW,
                        educational_notes=["Test configuration files are acceptable"],
                        validation_stage=ValidationStage.TDD,
                        tool_name="Write",
                    )
                else:
                    return ResponseBuilder.warn(
                        reason="Creating test file with no test functions",
                        risk_level=RiskLevel.MEDIUM,
                        suggestions=[
                            "Add at least one test function",
                            "Consider if this should be a test file",
                        ],
                        educational_notes=[
                            "TDD requires actual tests to drive development"
                        ],
                        validation_stage=ValidationStage.TDD,
                        tool_name="Write",
                    )
        else:
            # Creating implementation file - need evidence of failing test
            test_output = self.get_pytest_results()

            if not test_output:
                return ResponseBuilder.warn(
                    reason="Creating implementation without visible test output. Consider running tests first.",
                    risk_level=RiskLevel.MEDIUM,
                    suggestions=[
                        "Run tests to confirm Red phase",
                        "Ensure failing test exists before implementation",
                    ],
                    educational_notes=[
                        "TDD Red Phase: Test should fail before implementation",
                        "This is acceptable if starting new feature development",
                    ],
                    validation_stage=ValidationStage.TDD,
                    tool_name="Write",
                )

            if "failed" in test_output.lower():
                return ResponseBuilder.approve(
                    reason="Creating implementation with failing tests - follows TDD Green phase",
                    risk_level=RiskLevel.LOW,
                    educational_notes=[
                        "Good TDD practice: Implementing to fix failing tests"
                    ],
                    validation_stage=ValidationStage.TDD,
                    tool_name="Write",
                )
            else:
                return ResponseBuilder.warn(
                    reason="Creating implementation but all tests passing. Ensure this addresses a specific failing test.",
                    risk_level=RiskLevel.MEDIUM,
                    suggestions=[
                        "Verify implementation is needed for current failing test"
                    ],
                    validation_stage=ValidationStage.TDD,
                    tool_name="Write",
                )

        return ResponseBuilder.approve(
            reason="Write operation acceptable under TDD principles",
            risk_level=RiskLevel.LOW,
            validation_stage=ValidationStage.TDD,
            tool_name="Write",
        )

    def validate_edit_operation(
        self, file_path: str, old_content: str, new_content: str, context: str = ""
    ) -> HookResponse:
        """Validate Edit operations following TDD principles."""

        if self.is_test_file(file_path):
            # Editing test file
            old_test_count = self.count_tests_in_content(old_content)
            new_test_count = self.count_tests_in_content(new_content)

            if new_test_count > old_test_count + 1:
                return ResponseBuilder.block(
                    reason="TDD Violation: Adding multiple tests at once. Add one test at a time.",
                    risk_level=RiskLevel.HIGH,
                    suggestions=["Add only one test per edit operation"],
                    educational_notes=["TDD requires incremental test addition"],
                    validation_stage=ValidationStage.TDD,
                    tool_name="Edit",
                )

            return ResponseBuilder.approve(
                reason="Test file edit follows TDD principles",
                risk_level=RiskLevel.LOW,
                validation_stage=ValidationStage.TDD,
                tool_name="Edit",
            )
        else:
            # Editing implementation file - check if tests are passing (refactor) or failing (green phase)
            test_output = self.get_pytest_results()

            if test_output and "failed" not in test_output.lower():
                return ResponseBuilder.approve(
                    reason="Editing implementation with passing tests - TDD Refactor phase",
                    risk_level=RiskLevel.LOW,
                    educational_notes=[
                        "Refactoring with green tests is good TDD practice"
                    ],
                    validation_stage=ValidationStage.TDD,
                    tool_name="Edit",
                )

            return ResponseBuilder.approve(
                reason="Implementation edit acceptable under TDD principles",
                risk_level=RiskLevel.LOW,
                validation_stage=ValidationStage.TDD,
                tool_name="Edit",
            )

    def validate_operation(
        self, tool_name: str, tool_input: Dict[str, Any], context: str = ""
    ) -> HookResponse:
        """Main entry point for TDD validation."""

        if tool_name == "Write":
            file_path = tool_input.get("file_path", "")
            content = tool_input.get("content", "")
            return self.validate_write_operation(file_path, content, context)

        elif tool_name == "Edit":
            file_path = tool_input.get("file_path", "")
            old_string = tool_input.get("old_string", "")
            new_string = tool_input.get("new_string", "")
            return self.validate_edit_operation(
                file_path, old_string, new_string, context
            )

        elif tool_name in ["MultiEdit", "Update"]:
            # For now, allow MultiEdit operations - could be enhanced later
            return ResponseBuilder.approve(
                reason="Multi-edit operations require manual TDD review",
                risk_level=RiskLevel.LOW,
                validation_stage=ValidationStage.TDD,
                tool_name=tool_name,
            )

        else:
            return ResponseBuilder.approve(
                reason="Tool not covered by TDD validation",
                risk_level=RiskLevel.LOW,
                validation_stage=ValidationStage.TDD,
                tool_name=tool_name,
            )
