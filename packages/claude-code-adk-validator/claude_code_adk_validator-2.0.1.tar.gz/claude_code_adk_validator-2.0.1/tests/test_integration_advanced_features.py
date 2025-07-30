#!/usr/bin/env python3
"""Integration tests for advanced features combining hook chaining, JSON responses, and context awareness."""

import json
import os
import subprocess
import tempfile
import time
from pathlib import Path

import pytest


def test_hook_chaining_integration() -> None:
    """Test complete hook chaining workflow from setup to execution."""

    with tempfile.TemporaryDirectory() as temp_dir:
        os.chdir(temp_dir)

        # Initialize a fake git repo for testing
        subprocess.run(["git", "init"], check=True, capture_output=True)

        # Test setup-chaining command
        result = subprocess.run(
            [
                "uv",
                "run",
                "python",
                "-m",
                "claude_code_adk_validator",
                "--setup-chaining",
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert (
            "Claude Code hooks with chaining configured successfully" in result.stdout
        )

        # Verify configuration files were created
        claude_dir = Path(".claude")
        assert claude_dir.exists()

        settings_file = claude_dir / "settings.local.json"
        assert settings_file.exists()

        # Parse and verify settings structure
        with open(settings_file) as f:
            settings = json.load(f)

        assert "hooks" in settings
        hooks = settings["hooks"]
        assert "PreToolUse" in hooks
        assert len(hooks["PreToolUse"]) == 2  # Two matchers: Write/Edit/etc and Bash

        # Verify both matchers are configured correctly
        matchers = [item["matcher"] for item in hooks["PreToolUse"]]
        assert "Write|Edit|MultiEdit|Update" in matchers
        assert "Bash" in matchers

        # Verify the Write/Edit matcher has 3 stages (security, tdd, file-analysis)
        write_matcher = next(
            item for item in hooks["PreToolUse"] if "Write" in item["matcher"]
        )
        assert len(write_matcher["hooks"]) == 3

        # Verify Bash matcher has 1 stage (security only)
        bash_matcher = next(
            item for item in hooks["PreToolUse"] if item["matcher"] == "Bash"
        )
        assert len(bash_matcher["hooks"]) == 1


def test_advanced_json_response_compliance() -> None:
    """Test that all advanced JSON responses comply with Claude Code schema."""

    from claude_code_adk_validator.validators.security_validator import (
        SecurityValidator,
    )
    from claude_code_adk_validator.hook_response import HookResponse

    validator = SecurityValidator(enable_context_analysis=False)

    # Test various scenarios and verify JSON compliance
    test_cases = [
        ("Bash", {"command": "echo hello"}, "approve"),
        ("Bash", {"command": "grep pattern file"}, "warn"),
        ("Bash", {"command": "rm -rf /"}, "block"),
        ("Write", {"file_path": "test.py", "content": "print('hello')"}, "approve"),
        (
            "Edit",
            {"file_path": "test.py", "old_string": "old", "new_string": "new 🚀"},
            "block",
        ),
    ]

    for tool_name, tool_input, expected_decision in test_cases:
        response = validator.validate_operation(tool_name, tool_input, "")

        # Verify HookResponse structure
        assert isinstance(response, HookResponse)
        assert response.decision.value == expected_decision
        assert isinstance(response.continue_processing, bool)
        assert isinstance(response.reason, str)
        assert len(response.reason) > 0

        # Verify metadata structure
        metadata = response.metadata
        assert metadata.tool_name == tool_name
        assert metadata.validation_stage is not None
        assert metadata.validation_stage.value in [
            "security",
            "tdd",
            "file_analysis",
            "tool_enforcement",
        ]
        assert metadata.risk_level.value in ["low", "medium", "high", "critical"]
        assert isinstance(metadata.suggestions, list)
        assert isinstance(metadata.educational_notes, list)
        assert isinstance(metadata.detected_patterns, list)

        # Test JSON serialization
        json_str = response.model_dump_json(by_alias=True)
        parsed = json.loads(json_str)

        # Verify JSON has Claude Code expected fields
        assert "continue" in parsed
        assert "decision" in parsed
        assert "reason" in parsed
        assert "metadata" in parsed


def test_context_aware_end_to_end() -> None:
    """Test complete context-aware workflow with tool history tracking."""

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
        history_file = f.name

    try:
        from claude_code_adk_validator.validators.security_validator import (
            SecurityValidator,
        )

        # Initialize validator with context analysis
        validator = SecurityValidator(enable_context_analysis=True)
        assert validator.context_analyzer is not None
        validator.context_analyzer.history_file = history_file

        # Simulate a realistic development workflow
        workflow_steps = [
            # Step 1: Write some code
            (
                "Write",
                {"file_path": "module.py", "content": "def add(a, b): return a + b"},
            ),
            # Step 2: Edit the code multiple times without tests
            (
                "Edit",
                {
                    "file_path": "module.py",
                    "old_string": "def add(a, b): return a + b",
                    "new_string": "def add(a, b):\n    return a + b",
                },
            ),
            (
                "Edit",
                {
                    "file_path": "module.py",
                    "old_string": "return a + b",
                    "new_string": "result = a + b\n    return result",
                },
            ),
            # Step 3: Another edit should trigger "edit without test" pattern
            (
                "Edit",
                {
                    "file_path": "module.py",
                    "old_string": "result = a + b",
                    "new_string": "result = a + b  # Addition",
                },
            ),
        ]

        responses = []
        for tool_name, tool_input in workflow_steps:
            response = validator.validate_operation(tool_name, tool_input, "")
            responses.append(response)
            time.sleep(0.1)  # Ensure different timestamps

        # The last response should have context-aware enhancement
        final_response = responses[-1]
        educational_notes = final_response.metadata.educational_notes

        # Should detect edit-without-test pattern
        has_test_recommendation = any(
            "test" in note.lower() for note in educational_notes
        )
        assert (
            has_test_recommendation
        ), f"Expected test recommendation in: {educational_notes}"

        # Verify tool usage was recorded
        assert validator.context_analyzer is not None
        recent_tools = validator.context_analyzer._get_recent_tool_usage()
        assert len(recent_tools) >= 4

        # Test missing imports pattern
        import_test_input = {
            "file_path": "analysis.py",
            "content": "arr = numpy.array([1, 2, 3])\nprint(arr.mean())",
        }

        import_response = validator.validate_operation("Write", import_test_input, "")
        import_notes = import_response.metadata.educational_notes

        has_import_recommendation = any(
            "import" in note.lower() for note in import_notes
        )
        assert (
            has_import_recommendation
        ), f"Expected import recommendation in: {import_notes}"

    finally:
        os.unlink(history_file)


def test_staged_validation_integration() -> None:
    """Test the staged validation system with different stages."""

    # Test security stage
    result = subprocess.run(
        [
            "uv",
            "run",
            "python",
            "-m",
            "claude_code_adk_validator",
            "--stage",
            "security",
        ],
        input='{"tool_name": "Bash", "tool_input": {"command": "echo hello"}}',
        capture_output=True,
        text=True,
        cwd="/home/jihun/code_base/jk_hooks_gemini_challenge",
    )

    if result.returncode != 0:
        print(f"Command failed with return code {result.returncode}")
        print(f"stdout: {result.stdout}")
        print(f"stderr: {result.stderr}")

    assert result.returncode == 0
    response_data = json.loads(result.stdout)
    assert response_data["decision"] == "approve"
    assert response_data["metadata"]["validation_stage"] == "security"

    # Test dangerous command blocking
    result = subprocess.run(
        [
            "uv",
            "run",
            "python",
            "-m",
            "claude_code_adk_validator",
            "--stage",
            "security",
        ],
        input='{"tool_name": "Bash", "tool_input": {"command": "rm -rf /"}}',
        capture_output=True,
        text=True,
        cwd="/home/jihun/code_base/jk_hooks_gemini_challenge",
    )

    assert result.returncode == 2  # Block exit code
    response_data = json.loads(result.stdout)
    assert response_data["decision"] == "block"
    assert "security threat" in response_data["reason"].lower()


def test_real_world_scenario_git_workflow() -> None:
    """Test a realistic git workflow with hook chaining."""

    with tempfile.TemporaryDirectory() as temp_dir:
        os.chdir(temp_dir)

        # Initialize git repo
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test User"], check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], check=True)

        # Setup hooks
        result = subprocess.run(
            [
                "uv",
                "run",
                "python",
                "-m",
                "claude_code_adk_validator",
                "--setup-chaining",
            ],
            capture_output=True,
            text=True,
            cwd=temp_dir,
        )
        assert result.returncode == 0

        # Test legitimate git operations
        git_commands = [
            {"tool_name": "Bash", "tool_input": {"command": "git status"}},
            {"tool_name": "Bash", "tool_input": {"command": "git add ."}},
            {"tool_name": "Bash", "tool_input": {"command": "git commit -m 'test'"}},
            {"tool_name": "Bash", "tool_input": {"command": "git checkout main"}},
        ]

        for cmd in git_commands:
            result = subprocess.run(
                [
                    "uv",
                    "run",
                    "python",
                    "-m",
                    "claude_code_adk_validator",
                    "--stage",
                    "security",
                ],
                input=json.dumps(cmd),
                capture_output=True,
                text=True,
                cwd=temp_dir,
            )

            # All legitimate git commands should be approved
            assert result.returncode == 0
            response = json.loads(result.stdout)
            assert response["decision"] in [
                "approve",
                "warn",
            ]  # warn for tool enforcement


def test_performance_and_reliability() -> None:
    """Test performance characteristics and error handling."""

    from claude_code_adk_validator.validators.security_validator import (
        SecurityValidator,
    )

    validator = SecurityValidator(enable_context_analysis=True)

    # Test performance with multiple rapid operations
    start_time = time.time()

    for i in range(50):
        tool_input = {"file_path": f"test_{i}.py", "content": f"print('hello {i}')"}
        response = validator.validate_operation("Write", tool_input, "")
        assert response.decision.value == "approve"

    elapsed = time.time() - start_time

    # Should handle 50 operations in under 5 seconds (100ms per operation)
    assert elapsed < 5.0, f"Performance test failed: {elapsed:.2f}s for 50 operations"

    # Test error handling with malformed input
    try:
        validator.validate_operation("UnknownTool", {}, "")
        # Should not raise exception, should return approve for unknown tools
    except Exception as e:
        pytest.fail(f"Error handling failed: {e}")

    # Test with missing required fields
    response = validator.validate_operation("Bash", {}, "")
    assert response.decision.value == "approve"  # Should handle gracefully


def test_documentation_compliance() -> None:
    """Verify features match documented capabilities."""

    # Test CLI help shows advanced features
    result = subprocess.run(
        ["uv", "run", "python", "-m", "claude_code_adk_validator", "--help"],
        capture_output=True,
        text=True,
        cwd="/home/jihun/code_base/jk_hooks_gemini_challenge",
    )

    assert result.returncode == 0
    help_text = result.stdout

    # Should document advanced features
    assert "--setup-chaining" in help_text
    assert "--stage" in help_text

    # Test version information
    result = subprocess.run(
        ["uv", "run", "python", "-m", "claude_code_adk_validator", "--version"],
        capture_output=True,
        text=True,
        cwd="/home/jihun/code_base/jk_hooks_gemini_challenge",
    )

    assert result.returncode == 0
    # Should show version information


if __name__ == "__main__":
    try:
        print("Running test_hook_chaining_integration...")
        test_hook_chaining_integration()
        print("✅ test_hook_chaining_integration passed!")

        print("Running test_advanced_json_response_compliance...")
        test_advanced_json_response_compliance()
        print("✅ test_advanced_json_response_compliance passed!")

        print("Running test_context_aware_end_to_end...")
        test_context_aware_end_to_end()
        print("✅ test_context_aware_end_to_end passed!")

        print("Running test_staged_validation_integration...")
        test_staged_validation_integration()
        print("✅ test_staged_validation_integration passed!")

        print("Running test_real_world_scenario_git_workflow...")
        test_real_world_scenario_git_workflow()
        print("✅ test_real_world_scenario_git_workflow passed!")

        print("Running test_performance_and_reliability...")
        test_performance_and_reliability()
        print("✅ test_performance_and_reliability passed!")

        print("Running test_documentation_compliance...")
        test_documentation_compliance()
        print("✅ test_documentation_compliance passed!")

        print("✅ All integration tests passed!")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
