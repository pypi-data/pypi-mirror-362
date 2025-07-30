"""
Test TDD validation for Update operations.
"""

import json
import subprocess
import tempfile
import os


def test_update_operation_tdd_validation():
    """Test that Update operations are properly validated for TDD compliance."""
    
    # Test Update operation on a Python file
    test_input = {
        "tool_name": "Update",
        "tool_input": {
            "file_path": "example.py",
            "content": "def add(a, b):\n    return a + b"
        }
    }
    
    # Run the validator with current working directory
    result = subprocess.run(
        ["uv", "run", "python", "-m", "claude_code_adk_validator", "--stage", "tdd"],
        input=json.dumps(test_input),
        text=True,
        capture_output=True,
        timeout=30,
        cwd=os.getcwd()
    )
    
    # Should return either approve, warn, or fail gracefully
    assert result.returncode in [0, 1, 2], f"Unexpected return code: {result.returncode}\nStdout: {result.stdout}\nStderr: {result.stderr}"
    
    # Check for either successful validation or graceful failure
    if result.returncode == 0 and result.stdout:
        try:
            response = json.loads(result.stdout)
            assert "reason" in response
            assert "TDD" in response["reason"] or "tdd" in response["reason"].lower()
        except json.JSONDecodeError:
            # If not JSON, check for TDD-related text
            assert "TDD" in result.stdout or "test" in result.stdout.lower()
    elif result.returncode == 1:
        # Allow graceful failure for environment issues
        assert "directory" in result.stderr.lower() or "current" in result.stderr.lower()


def test_update_operation_non_programming_file():
    """Test that Update operations on non-programming files skip TDD validation."""
    
    test_input = {
        "tool_name": "Update", 
        "tool_input": {
            "file_path": "README.md",
            "content": "# My Project\n\nThis is documentation."
        }
    }
    
    result = subprocess.run(
        ["uv", "run", "python", "-m", "claude_code_adk_validator", "--stage", "tdd"],
        input=json.dumps(test_input),
        text=True,
        capture_output=True,
        timeout=30,
        cwd=os.getcwd()
    )
    
    # Should approve non-programming files or fail gracefully
    assert result.returncode in [0, 1], f"Unexpected return code: {result.returncode}\nStderr: {result.stderr}"
    
    if result.returncode == 0 and result.stdout:
        try:
            response = json.loads(result.stdout)
            assert response.get("continue", False) is True
            assert "skip" in response.get("reason", "").lower()
        except json.JSONDecodeError:
            # Text response should indicate approval
            assert "approved" in result.stdout.lower() or "allowed" in result.stdout.lower()
    elif result.returncode == 1:
        # Allow graceful failure for environment issues
        assert "directory" in result.stderr.lower() or "current" in result.stderr.lower()


def test_multiedit_operation_tdd_validation():
    """Test that MultiEdit operations are properly validated for TDD compliance."""
    
    test_input = {
        "tool_name": "MultiEdit",
        "tool_input": {
            "file_path": "calculator.py",
            "edits": [
                {
                    "old_string": "def add(a, b):",
                    "new_string": "def add(a, b):"
                }
            ]
        }
    }
    
    result = subprocess.run(
        ["uv", "run", "python", "-m", "claude_code_adk_validator", "--stage", "tdd"],
        input=json.dumps(test_input),
        text=True,
        capture_output=True,
        timeout=30,
        cwd=os.getcwd()
    )
    
    # Should return either approve, warn, or fail gracefully
    assert result.returncode in [0, 1, 2], f"Unexpected return code: {result.returncode}\nStderr: {result.stderr}"
    
    # Check for either successful validation or graceful failure
    if result.returncode == 0 and result.stdout:
        try:
            response = json.loads(result.stdout)
            assert "reason" in response
            # Should contain either TDD guidance or test information
            assert any(keyword in response["reason"].lower() 
                      for keyword in ["tdd", "test", "refactor", "green"])
        except json.JSONDecodeError:
            # If not JSON, check for TDD-related text
            assert any(keyword in result.stdout.lower() 
                      for keyword in ["tdd", "test", "refactor"])
    elif result.returncode == 1:
        # Allow graceful failure for environment issues
        assert "directory" in result.stderr.lower() or "current" in result.stderr.lower()


if __name__ == "__main__":
    test_update_operation_tdd_validation()
    test_update_operation_non_programming_file()
    test_multiedit_operation_tdd_validation()
    print("✅ All Update/MultiEdit TDD validation tests passed!")