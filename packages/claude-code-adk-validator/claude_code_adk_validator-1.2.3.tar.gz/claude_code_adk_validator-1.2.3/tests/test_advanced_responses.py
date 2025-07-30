#!/usr/bin/env python3

import json
import subprocess
import sys


def test_advanced_json_response_format():
    """Test that validator returns advanced JSON response format with full schema."""

    # Test input that should be approved
    safe_write = {
        "session_id": "test123",
        "transcript_path": "/tmp/nonexistent.jsonl",
        "hook_event_name": "PreToolUse",
        "tool_name": "Write",
        "tool_input": {"file_path": "test.txt", "content": "Hello, world!"},
    }

    # Run the validator
    process = subprocess.run(
        [sys.executable, "-m", "claude_code_adk_validator"],
        input=json.dumps(safe_write),
        text=True,
        capture_output=True,
        timeout=30,
    )

    # Should approve (exit code 0)
    assert process.returncode == 0

    # Check if we can parse any JSON output (some may be in stderr for debugging)
    output = (
        process.stderr.strip() if process.stderr.strip() else process.stdout.strip()
    )

    if output:
        try:
            response_data = json.loads(output)

            # Check for advanced response format fields
            assert "continue" in response_data or "decision" in response_data
            assert "reason" in response_data

            # Check for metadata if present
            if "metadata" in response_data:
                metadata = response_data["metadata"]
                assert "risk_level" in metadata
                assert "suggestions" in metadata

        except json.JSONDecodeError:
            # No JSON output is acceptable for approved operations
            pass


def test_advanced_blocking_response():
    """Test advanced JSON response for blocked operations."""

    # Test input that should be blocked
    dangerous_bash = {
        "session_id": "test123",
        "transcript_path": "/tmp/nonexistent.jsonl",
        "hook_event_name": "PreToolUse",
        "tool_name": "Bash",
        "tool_input": {"command": "rm -rf /"},
    }

    # Run the validator
    process = subprocess.run(
        [sys.executable, "-m", "claude_code_adk_validator"],
        input=json.dumps(dangerous_bash),
        text=True,
        capture_output=True,
        timeout=30,
    )

    # Should block (exit code 2)
    assert process.returncode == 2

    # Should have JSON output in stdout
    assert process.stdout.strip()

    response_data = json.loads(process.stdout.strip())

    # Check for advanced response format fields
    assert "continue" in response_data
    assert "decision" in response_data
    assert "reason" in response_data
    assert response_data["decision"] in ["block", "warn"]
    assert response_data["continue"] in [True, False]

    # Check for metadata
    assert "metadata" in response_data
    metadata = response_data["metadata"]
    assert "risk_level" in metadata
    assert "suggestions" in metadata
    assert metadata["risk_level"] in ["low", "medium", "high", "critical"]


def test_stage_specific_validation():
    """Test stage-specific validation with --stage parameter."""

    # Test input for stage-specific validation
    test_input = {
        "session_id": "test123",
        "transcript_path": "/tmp/nonexistent.jsonl",
        "hook_event_name": "PreToolUse",
        "tool_name": "Write",
        "tool_input": {"file_path": "test.txt", "content": "console.log('hello');"},
    }

    # Test security stage
    process = subprocess.run(
        [sys.executable, "-m", "claude_code_adk_validator", "--stage", "security"],
        input=json.dumps(test_input),
        text=True,
        capture_output=True,
        timeout=30,
    )

    # Should have some response (exit code 0 or 2)
    assert process.returncode in [0, 2]

    # If there's JSON output, check it has stage information
    if process.stdout.strip():
        try:
            response_data = json.loads(process.stdout.strip())
            if (
                "metadata" in response_data
                and "validation_stage" in response_data["metadata"]
            ):
                assert response_data["metadata"]["validation_stage"] == "security"
        except json.JSONDecodeError:
            pass


def test_warning_vs_blocking_decisions():
    """Test that medium-risk operations result in warnings, not blocks."""

    # Test input that should generate a warning (medium risk)
    medium_risk = {
        "session_id": "test123",
        "transcript_path": "/tmp/nonexistent.jsonl",
        "hook_event_name": "PreToolUse",
        "tool_name": "Bash",
        "tool_input": {"command": "git checkout -b new-feature"},
    }

    # Run the validator
    process = subprocess.run(
        [sys.executable, "-m", "claude_code_adk_validator"],
        input=json.dumps(medium_risk),
        text=True,
        capture_output=True,
        timeout=30,
    )

    # Should either approve (exit 0) or warn (exit 0 with warning in stderr)
    assert process.returncode == 0

    # Check if warning information is provided in stdout
    if process.stdout.strip():
        try:
            response_data = json.loads(process.stdout.strip())
            # If we have a decision field, it should be "warn" not "block"
            if "decision" in response_data:
                assert response_data["decision"] in ["approve", "warn"]
                assert response_data["decision"] != "block"
        except json.JSONDecodeError:
            pass


if __name__ == "__main__":
    test_advanced_json_response_format()
    test_advanced_blocking_response()
    test_stage_specific_validation()
    test_warning_vs_blocking_decisions()
    print("✅ All advanced response format tests passed!")
