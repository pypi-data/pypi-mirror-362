#!/usr/bin/env python3

import os
import tempfile
import time
from claude_code_adk_validator.context_analyzer import ContextAnalyzer
from claude_code_adk_validator.validators.security_validator import SecurityValidator
from claude_code_adk_validator.hook_response import ResponseBuilder


def test_context_analyzer_recording():
    """Test that context analyzer records tool usage correctly."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
        history_file = f.name

    try:
        analyzer = ContextAnalyzer(history_file=history_file)

        # Record a tool usage event
        tool_input = {"file_path": "test.py", "content": "print('hello')"}
        analyzer.record_tool_usage("Write", tool_input, "approved")

        # Verify it was recorded
        recent_tools = analyzer._get_recent_tool_usage()
        assert len(recent_tools) == 1
        assert recent_tools[0].tool_name == "Write"
        assert recent_tools[0].outcome == "approved"
        assert recent_tools[0].file_path == "test.py"

    finally:
        os.unlink(history_file)


def test_context_aware_edit_without_test_pattern():
    """Test detection of editing code without running tests."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
        history_file = f.name

    try:
        analyzer = ContextAnalyzer(history_file=history_file)

        # Simulate multiple edits without tests
        for i in range(3):
            tool_input = {
                "file_path": f"module_{i}.py",
                "content": f"def func_{i}(): pass",
            }
            analyzer.record_tool_usage("Edit", tool_input, "approved")
            time.sleep(0.1)  # Small delay to ensure different timestamps

        # Test context-aware response for another edit
        base_response = ResponseBuilder.approve(
            "File operation approved", tool_name="Edit"
        )
        enhanced_response = analyzer.get_context_aware_response(
            "Edit", {"file_path": "another.py", "content": "more code"}, base_response
        )

        # Should detect pattern and add educational note
        assert any(
            "Consider running tests" in note
            for note in enhanced_response.metadata.educational_notes
        )

    finally:
        os.unlink(history_file)


def test_context_aware_missing_imports_pattern():
    """Test detection of Python code that might need imports."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
        history_file = f.name

    try:
        analyzer = ContextAnalyzer(history_file=history_file)

        # Test code with numpy usage but no imports
        tool_input = {
            "file_path": "analysis.py",
            "content": "arr = numpy.array([1, 2, 3])\nprint(arr.mean())",
        }

        base_response = ResponseBuilder.approve(
            "File operation approved", tool_name="Write"
        )
        enhanced_response = analyzer.get_context_aware_response(
            "Write", tool_input, base_response
        )

        # Should detect missing imports pattern
        assert any(
            "imports" in note for note in enhanced_response.metadata.educational_notes
        )

    finally:
        os.unlink(history_file)


def test_context_aware_tdd_pattern():
    """Test detection of test-driven development workflow."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
        history_file = f.name

    try:
        analyzer = ContextAnalyzer(history_file=history_file)

        # Simulate TDD workflow: write test first
        test_input = {
            "file_path": "test_module.py",
            "content": "def test_add(): assert add(1, 2) == 3",
        }
        analyzer.record_tool_usage("Write", test_input, "approved")
        time.sleep(0.1)

        # Then write implementation
        impl_input = {
            "file_path": "module.py",
            "content": "def add(a, b): return a + b",
        }
        base_response = ResponseBuilder.approve(
            "File operation approved", tool_name="Write"
        )
        enhanced_response = analyzer.get_context_aware_response(
            "Write", impl_input, base_response
        )

        # Should detect TDD pattern and praise it
        assert any(
            "TDD workflow" in note
            for note in enhanced_response.metadata.educational_notes
        )

    finally:
        os.unlink(history_file)


def test_security_validator_with_context():
    """Test SecurityValidator integration with context analysis."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
        history_file = f.name

    try:
        # Initialize validator with context analysis
        validator = SecurityValidator(enable_context_analysis=True)
        validator.context_analyzer.history_file = history_file

        # Test basic validation with context recording
        tool_input = {"file_path": "test.py", "content": "print('hello world')"}
        response = validator.validate_operation("Write", tool_input, "")

        # Verify response structure
        assert response.decision.value in ["approve", "warn", "block"]
        assert response.metadata.tool_name == "Write"

        # Verify context was recorded
        recent_tools = validator.context_analyzer._get_recent_tool_usage()
        assert len(recent_tools) == 1

    finally:
        os.unlink(history_file)


def test_multiple_bash_pattern():
    """Test detection of repeated bash commands."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
        history_file = f.name

    try:
        analyzer = ContextAnalyzer(history_file=history_file)

        # Simulate multiple bash commands
        bash_commands = ["ls -la", "grep pattern file.txt", "awk '{print $1}' data.txt"]
        for cmd in bash_commands:
            tool_input = {"command": cmd}
            analyzer.record_tool_usage("Bash", tool_input, "approved")
            time.sleep(0.1)

        # Test context-aware response for another bash command
        base_response = ResponseBuilder.approve("Command approved", tool_name="Bash")
        enhanced_response = analyzer.get_context_aware_response(
            "Bash", {"command": "sort data.txt"}, base_response
        )

        # Should suggest scripting
        assert any(
            "script" in note for note in enhanced_response.metadata.educational_notes
        )

    finally:
        os.unlink(history_file)


def test_disable_context_analysis():
    """Test SecurityValidator with context analysis disabled."""
    validator = SecurityValidator(enable_context_analysis=False)

    # Should work without context analyzer
    tool_input = {"file_path": "test.py", "content": "print('hello')"}
    response = validator.validate_operation("Write", tool_input, "")

    assert response.decision.value in ["approve", "warn", "block"]
    assert validator.context_analyzer is None


if __name__ == "__main__":
    test_context_analyzer_recording()
    test_context_aware_edit_without_test_pattern()
    test_context_aware_missing_imports_pattern()
    test_context_aware_tdd_pattern()
    test_security_validator_with_context()
    test_multiple_bash_pattern()
    test_disable_context_analysis()
    print("✅ All context-aware response tests passed!")
