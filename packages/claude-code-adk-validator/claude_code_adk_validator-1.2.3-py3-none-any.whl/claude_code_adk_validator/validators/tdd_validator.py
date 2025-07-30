"""TDD-focused validator inspired by tdd-guard's sophisticated TDD analysis."""

import json
import os
import re
import sys
from typing import Dict, Any, List, Optional, TypedDict
from ..hook_response import HookResponse, ResponseBuilder, RiskLevel, ValidationStage
from ..prompts import (
    TDD_CORE_PRINCIPLES,
    EDIT_ANALYSIS,
    WRITE_ANALYSIS,
    PYTHON_ERROR_MAPPINGS,
)

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None


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

    def __init__(self, api_key: Optional[str] = None) -> None:
        self.test_processor = TestResultProcessor()
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        self.client = (
            genai.Client(api_key=self.api_key) if self.api_key and genai else None
        )
        # Initialize FileStorage to load test results
        from ..file_storage import FileStorage

        self.storage = FileStorage()

    def get_pytest_results(self) -> Optional[str]:
        """Load pytest results from FileStorage instead of running pytest."""
        try:
            # Load test results from storage
            test_results = self.storage.load_test_results()
            if not test_results:
                return None

            # Format the results similar to tdd-guard's output
            return self.format_test_output(test_results)

        except Exception as e:
            # Log but don't fail on errors
            print(f"Error loading test results: {e}", file=sys.stderr)
            return None

    def format_test_output(self, test_results: Dict[str, Any]) -> str:
        """Format test results from FileStorage similar to tdd-guard's output."""
        if not test_results or "testModules" not in test_results:
            return "No test results found."

        output_lines = []
        total_passed = 0
        total_failed = 0
        failed_modules = 0
        passed_modules = 0

        for module in test_results["testModules"]:
            module_id = module.get("moduleId", "unknown")
            tests = module.get("tests", [])

            # Count test results in this module
            module_passed = 0
            module_failed = 0
            test_details = []

            for test in tests:
                test_name = test.get("name", "unknown")
                full_name = test.get("fullName", test_name)
                state = test.get("state", "unknown")

                if state == "passed":
                    module_passed += 1
                    test_details.append(f"   [PASS] {full_name} 0ms")
                elif state == "failed":
                    module_failed += 1
                    test_details.append(f"   [FAIL] {full_name} 0ms")
                    # Add error message if available
                    errors = test.get("errors", [])
                    if errors and errors[0].get("message"):
                        test_details.append(f"     -> {errors[0]['message']}")

            # Update totals
            total_passed += module_passed
            total_failed += module_failed

            # Format module output
            test_count = module_passed + module_failed
            if module_failed == 0:
                output_lines.append(f" [PASS] {module_id} ({test_count} tests) 0ms")
                passed_modules += 1
            else:
                output_lines.append(
                    f" [FAIL] {module_id} ({test_count} tests | {module_failed} failed) 0ms"
                )
                failed_modules += 1
                output_lines.extend(test_details)

        # Add summary
        if total_failed > 0:
            output_lines.append(
                f" Test Files  {failed_modules} failed | {passed_modules} passed ({failed_modules + passed_modules})"
            )
            output_lines.append(
                f"      Tests  {total_failed} failed | {total_passed} passed ({total_failed + total_passed})"
            )
        else:
            output_lines.append(
                f" Test Files  {passed_modules} passed ({passed_modules})"
            )
            output_lines.append(f"      Tests  {total_passed} passed ({total_passed})")

        return "\n".join(output_lines)

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

    def analyze_tdd_with_llm(
        self,
        file_path: str,
        content: str,
        test_output: Optional[str],
        operation: str = "Write",
    ) -> Optional[HookResponse]:
        """Use LLM for deep TDD analysis with test context."""
        if not self.client:
            return None

        try:
            # Build context similar to tdd-guard
            is_test = self.is_test_file(file_path)
            file_type = "test file" if is_test else "implementation file"

            # Select appropriate analysis prompt based on operation
            operation_analysis = (
                WRITE_ANALYSIS if operation == "Write" else EDIT_ANALYSIS
            )

            prompt = f"""You are a TDD expert reviewing Python code changes.

{TDD_CORE_PRINCIPLES}

{operation_analysis}

{PYTHON_ERROR_MAPPINGS}

## Current Context:
- File: {file_path} ({file_type})
- Operation: {operation}

## Test Output:
```
{test_output or 'No test output available - this suggests tests have not been run'}
```

## Code Content:
```python
{content[:2000]}
```

## Your Analysis:
Based on the TDD principles and the specific operation type, analyze this change.

Respond with:
- tdd_violation: yes/no
- severity: critical/high/medium/low
- phase: red/green/refactor/unknown
- reason: Specific explanation focusing on TDD compliance
- suggestions: Actionable steps to follow TDD properly"""

            response = self.client.models.generate_content(
                model="gemini-2.5-pro",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.1,
                    max_output_tokens=1000,
                ),
            )

            # Parse response and determine action
            if not response or not hasattr(response, "text") or not response.text:
                # LLM failed - return None to fall back to rule-based validation
                print("LLM returned no response for TDD analysis", file=sys.stderr)
                return None

            # Debug: Log LLM response
            if os.environ.get("TDD_DEBUG"):
                print(f"LLM TDD Response: {response.text[:500]}", file=sys.stderr)

            # Safely get response text
            response_text = (response.text or "").lower()

            if "tdd_violation: yes" in response_text:
                reason_match = re.search(
                    r"reason:\s*(.+?)(?:\n|$)", response.text, re.IGNORECASE
                )
                reason = (
                    reason_match.group(1).strip()
                    if reason_match
                    else "TDD violation detected by AI analysis"
                )

                severity_match = re.search(
                    r"severity:\s*(critical|high)", response_text
                )
                if severity_match:
                    return ResponseBuilder.block(
                        reason=f"LLM TDD Analysis: {reason}",
                        risk_level=RiskLevel.HIGH,
                        suggestions=[
                            "Write failing tests first",
                            "Follow Red-Green-Refactor cycle",
                            "Implement one feature at a time",
                        ],
                        educational_notes=[
                            "AI-powered TDD analysis detected violation"
                        ],
                        validation_stage=ValidationStage.TDD,
                        tool_name="Write",
                    )

        except Exception as e:
            # Log but don't fail on LLM errors
            print(f"LLM TDD analysis error: {e}", file=sys.stderr)
            print("Falling back to rule-based validation", file=sys.stderr)

        return None

    def is_programming_file(self, file_path: str) -> bool:
        """Check if file is a programming language file that should have TDD enforcement."""
        # Get file extension
        _, ext = os.path.splitext(file_path.lower())

        # Programming language extensions that should follow TDD
        programming_extensions = {
            ".py",
            ".js",
            ".ts",
            ".jsx",
            ".tsx",
            ".java",
            ".kt",
            ".swift",
            ".go",
            ".rs",
            ".dart",
            ".cpp",
            ".c",
            ".cs",
            ".rb",
            ".php",
            ".scala",
            ".clj",
            ".ex",
            ".exs",
            ".ml",
            ".hs",
            ".lua",
            ".r",
        }

        return ext in programming_extensions

    def validate_write_operation(
        self, file_path: str, content: str, context: str = ""
    ) -> HookResponse:
        """Validate Write operations following tdd-guard's TDD principles."""

        # Skip TDD validation for non-programming files
        if not self.is_programming_file(file_path):
            return ResponseBuilder.approve(
                reason="Non-programming file - TDD validation skipped",
                validation_stage=ValidationStage.TDD,
                tool_name="Write",
            )

        if self.is_test_file(file_path):
            # Creating a test file - check TDD principles with enhanced analysis
            test_count = self.count_tests_in_content(content)
            test_quality = self.analyze_test_quality(content)
            framework = self.detect_test_framework(content)

            # Check for multiple tests violation
            if test_count > 1:
                # Try LLM analysis first for better context
                test_output = self.get_pytest_results()
                llm_response = self.analyze_tdd_with_llm(
                    file_path, content, test_output, "Write"
                )
                if llm_response:
                    return llm_response

                return ResponseBuilder.block(
                    reason=f"TDD Violation: Found {test_count} tests in new file. TDD requires ONE test at a time.",
                    risk_level=RiskLevel.HIGH,
                    suggestions=[
                        "Keep only one test function (def test_*) in the initial file",
                        "Move other tests to separate commits",
                        "Each test should drive minimal implementation",
                    ],
                    educational_notes=[
                        "TDD Principle: Write the simplest failing test first",
                        "One test at a time ensures:",
                        "- Focused implementation",
                        "- Clear test-to-code mapping",
                        "- Avoidable over-engineering",
                        "",
                        f"Found {test_count} test functions in your file",
                        "Keep only one and add others incrementally",
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
                # Let LLM analyze without test context but provide setup instructions
                llm_response = self.analyze_tdd_with_llm(
                    file_path, content, None, "Write"
                )
                if llm_response:
                    return llm_response

                return ResponseBuilder.block(
                    reason="TDD Violation: No test results found. You need to set up pytest and write tests first.",
                    risk_level=RiskLevel.HIGH,
                    suggestions=[
                        "First install pytest: uv add --dev pytest pytest-cov",
                        "Create a test file with ONE test that will fail",
                        "Run tests to see them fail (Red phase)",
                        "Then implement the code to make tests pass",
                    ],
                    educational_notes=[
                        "TDD Setup Instructions:",
                        "",
                        "1. Install pytest: uv add --dev pytest",
                        "",
                        "2. Create pytest.ini in project root:",
                        "[tool:pytest]",
                        "plugins = claude_code_adk_validator.pytest_reporter",
                        "testpaths = tests",
                        "python_files = test_*.py",
                        "",
                        "3. Create conftest.py:",
                        "from claude_code_adk_validator.pytest_reporter import PytestReporter",
                        "_reporter = PytestReporter('.claude/claude-code-adk-validator/data')",
                        "def pytest_configure(config):",
                        "    config.pluginmanager.register(_reporter, 'tdd-reporter')",
                        "",
                        "4. Write ONE failing test, then run: uv run pytest",
                        "5. Only then can you write implementation code",
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
                return ResponseBuilder.block(
                    reason="TDD Violation: All tests are passing! Write a failing test before adding new implementation.",
                    risk_level=RiskLevel.HIGH,
                    suggestions=[
                        "Write a failing test for the new feature",
                        "Follow Red-Green-Refactor cycle",
                        "Don't write code until you have a failing test",
                    ],
                    validation_stage=ValidationStage.TDD,
                    tool_name="Write",
                )

        # Layer 2: LLM analysis for defense in depth
        test_output = self.get_pytest_results()
        llm_response = self.analyze_tdd_with_llm(
            file_path, content, test_output, "Write"
        )
        if llm_response:
            return llm_response

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

        # Skip TDD validation for non-programming files
        if not self.is_programming_file(file_path):
            return ResponseBuilder.approve(
                reason="Non-programming file - TDD validation skipped",
                validation_stage=ValidationStage.TDD,
                tool_name="Edit",
            )

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

            # Layer 2: LLM analysis for comprehensive validation
            llm_response = self.analyze_tdd_with_llm(
                file_path, new_content, test_output, "Edit"
            )
            if llm_response:
                return llm_response

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
            # Enhanced validation for Update operations
            file_path = tool_input.get("file_path", "")
            
            # Skip TDD validation for non-programming files
            if not self.is_programming_file(file_path):
                return ResponseBuilder.approve(
                    reason="Non-programming file - TDD validation skipped",
                    validation_stage=ValidationStage.TDD,
                    tool_name=tool_name,
                )
            
            # Get test results for Update operations
            test_output = self.get_pytest_results()
            
            if test_output and "failed" not in test_output.lower():
                return ResponseBuilder.approve(
                    reason=f"{tool_name} operation with passing tests - TDD Refactor phase acceptable",
                    risk_level=RiskLevel.LOW,
                    educational_notes=[
                        "Refactoring with green tests is good TDD practice"
                    ],
                    validation_stage=ValidationStage.TDD,
                    tool_name=tool_name,
                )
            else:
                return ResponseBuilder.warn(
                    reason=f"{tool_name} operation detected - ensure TDD principles are followed",
                    risk_level=RiskLevel.MEDIUM,
                    suggestions=[
                        "Run tests after modifications: uv run pytest",
                        "Follow Red-Green-Refactor cycle",
                        "Add tests for new functionality"
                    ],
                    educational_notes=[
                        "Multi-edit operations should maintain TDD workflow"
                    ],
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
