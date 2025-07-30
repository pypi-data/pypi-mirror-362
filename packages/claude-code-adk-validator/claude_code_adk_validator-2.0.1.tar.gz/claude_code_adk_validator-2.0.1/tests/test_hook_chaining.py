#!/usr/bin/env python3

import json
import subprocess
import sys
import os
import tempfile
from pathlib import Path


def test_hook_chaining_config_generation():
    """Test that --setup-chaining generates proper hook chaining configuration."""

    with tempfile.TemporaryDirectory() as temp_dir:
        # Change to temp directory
        original_cwd = os.getcwd()
        os.chdir(temp_dir)

        try:
            # Run setup with chaining
            process = subprocess.run(
                [sys.executable, "-m", "claude_code_adk_validator", "--setup-chaining"],
                capture_output=True,
                text=True,
                timeout=30,
            )

            # Should succeed
            assert process.returncode == 0

            # Check that .claude/settings.local.json was created
            settings_file = Path(".claude/settings.local.json")
            assert settings_file.exists()

            # Check configuration content
            with open(settings_file, "r") as f:
                config = json.load(f)

            assert "hooks" in config
            assert "PreToolUse" in config["hooks"]

            # Check for chained hooks
            pre_tool_hooks = config["hooks"]["PreToolUse"]
            assert len(pre_tool_hooks) > 0

            # Find the multi-stage hook configuration
            chained_hook = None
            for hook_config in pre_tool_hooks:
                if len(hook_config.get("hooks", [])) > 1:
                    chained_hook = hook_config
                    break

            assert chained_hook is not None, "No chained hook configuration found"

            # Check for multiple stages
            hooks = chained_hook["hooks"]
            assert len(hooks) >= 3, "Should have at least 3 validation stages"

            # Check for stage-specific commands
            stage_commands = [hook["command"] for hook in hooks]
            assert any("--stage=security" in cmd for cmd in stage_commands)
            assert any("--stage=tdd" in cmd for cmd in stage_commands)
            assert any("--stage=file-analysis" in cmd for cmd in stage_commands)

        finally:
            os.chdir(original_cwd)


def test_stage_specific_validation():
    """Test that stage-specific validation works correctly."""

    # Test input for security stage
    test_input = {
        "session_id": "test123",
        "transcript_path": "/tmp/nonexistent.jsonl",
        "hook_event_name": "PreToolUse",
        "tool_name": "Bash",
        "tool_input": {"command": "echo hello"},
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


def test_multiple_stage_pipeline():
    """Test that multiple stages can be run in sequence."""

    test_input = {
        "session_id": "test123",
        "transcript_path": "/tmp/nonexistent.jsonl",
        "hook_event_name": "PreToolUse",
        "tool_name": "Write",
        "tool_input": {"file_path": "test.py", "content": "print('hello')"},
    }

    stages = ["security", "tdd", "file-analysis"]
    results = []

    for stage in stages:
        process = subprocess.run(
            [sys.executable, "-m", "claude_code_adk_validator", "--stage", stage],
            input=json.dumps(test_input),
            text=True,
            capture_output=True,
            timeout=30,
        )

        results.append(
            {
                "stage": stage,
                "exit_code": process.returncode,
                "stdout": process.stdout,
                "stderr": process.stderr,
            }
        )

    # All stages should complete (exit code 0 or 2)
    for result in results:
        assert result["exit_code"] in [
            0,
            2,
        ], f"Stage {result['stage']} failed unexpectedly"


def test_hook_chaining_early_termination():
    """Test that hook chaining terminates early on block decisions."""

    # Test input that should be blocked by security stage
    dangerous_input = {
        "session_id": "test123",
        "transcript_path": "/tmp/nonexistent.jsonl",
        "hook_event_name": "PreToolUse",
        "tool_name": "Bash",
        "tool_input": {"command": "rm -rf /"},
    }

    # Security stage should block this
    process = subprocess.run(
        [sys.executable, "-m", "claude_code_adk_validator", "--stage", "security"],
        input=json.dumps(dangerous_input),
        text=True,
        capture_output=True,
        timeout=30,
    )

    # Should be blocked (exit code 2)
    assert process.returncode == 2

    # Should have JSON output in stdout
    assert process.stdout.strip()

    # Parse the JSON response
    response_data = json.loads(process.stdout.strip())
    assert "continue" in response_data
    assert "decision" in response_data
    assert response_data["decision"] == "block"


if __name__ == "__main__":
    test_hook_chaining_config_generation()
    test_stage_specific_validation()
    test_multiple_stage_pipeline()
    test_hook_chaining_early_termination()
    print("✅ All hook chaining tests passed!")
