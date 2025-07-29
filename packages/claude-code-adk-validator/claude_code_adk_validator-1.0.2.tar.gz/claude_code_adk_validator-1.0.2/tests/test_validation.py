#!/usr/bin/env python3

import json
import subprocess
import sys
import os

def test_validator(test_name, hook_input, expected_exit_code=0):
    """Test the ADK validator with sample input"""
    print(f"\n=== Testing: {test_name} ===")
    print(f"Input: {json.dumps(hook_input, indent=2)}")
    
    try:
        # Run the validator via package
        process = subprocess.run(
            [sys.executable, '-m', 'claude_code_adk_validator'],
            input=json.dumps(hook_input),
            text=True,
            capture_output=True,
            timeout=10
        )
        
        print(f"Exit Code: {process.returncode}")
        if process.stdout:
            print(f"Stdout: {process.stdout}")
        if process.stderr:
            print(f"Stderr: {process.stderr}")
        
        if process.returncode == expected_exit_code:
            print("✅ Test PASSED")
        else:
            print(f"❌ Test FAILED - Expected exit code {expected_exit_code}, got {process.returncode}")
            
        return process.returncode == expected_exit_code
        
    except subprocess.TimeoutExpired:
        print("❌ Test FAILED - Timeout")
        return False
    except Exception as e:
        print(f"❌ Test FAILED - Error: {e}")
        return False

def main():
    """Run validation tests"""
    print("Testing Google ADK-inspired Claude Code Validator")
    print("=" * 50)
    
    # Test 1: Safe file write (should pass)
    safe_write = {
        "session_id": "test123",
        "transcript_path": "/tmp/nonexistent.jsonl",
        "hook_event_name": "PreToolUse",
        "tool_name": "Write",
        "tool_input": {
            "file_path": "test.txt",
            "content": "Hello, world!"
        }
    }
    
    # Test 2: Dangerous bash command (should be blocked)
    dangerous_bash = {
        "session_id": "test123",
        "transcript_path": "/tmp/nonexistent.jsonl",
        "hook_event_name": "PreToolUse",
        "tool_name": "Bash",
        "tool_input": {
            "command": "rm -rf /"
        }
    }
    
    # Test 3: File with potential sensitive content (LLM will decide based on context)
    sensitive_file = {
        "session_id": "test123",
        "transcript_path": "/tmp/nonexistent.jsonl", 
        "hook_event_name": "PreToolUse",
        "tool_name": "Write",
        "tool_input": {
            "file_path": ".env",
            "content": "api_key = \"sk_live_1234567890abcdefghijklmnop\"\npassword = \"realLongPasswordValue123456\""
        }
    }
    
    # Test 4: Safe bash command (should pass)
    safe_bash = {
        "session_id": "test123",
        "transcript_path": "/tmp/nonexistent.jsonl",
        "hook_event_name": "PreToolUse", 
        "tool_name": "Bash",
        "tool_input": {
            "command": "ls -la"
        }
    }
    
    # Test 5: Grep command (should suggest ripgrep)
    grep_command = {
        "session_id": "test123",
        "transcript_path": "/tmp/nonexistent.jsonl",
        "hook_event_name": "PreToolUse",
        "tool_name": "Bash",
        "tool_input": {
            "command": "grep pattern file.txt"
        }
    }
    
    # Test 6: Find command (should suggest ripgrep alternative)
    find_command = {
        "session_id": "test123",
        "transcript_path": "/tmp/nonexistent.jsonl",
        "hook_event_name": "PreToolUse",
        "tool_name": "Bash", 
        "tool_input": {
            "command": "find . -name '*.py'"
        }
    }
    
    # Test 7: Python command (should suggest uv run python)
    python_command = {
        "session_id": "test123",
        "transcript_path": "/tmp/nonexistent.jsonl",
        "hook_event_name": "PreToolUse",
        "tool_name": "Bash",
        "tool_input": {
            "command": "python script.py"
        }
    }
    
    # Run tests
    tests = [
        ("Safe file write", safe_write, 0),
        ("Dangerous bash command", dangerous_bash, 2),
        ("File with potential sensitive content", sensitive_file, 0),
        ("Safe bash command", safe_bash, 0),
        ("Grep command (should be blocked, suggest rg)", grep_command, 2),
        ("Find command (should be blocked, suggest rg)", find_command, 2),
        ("Python command (should be blocked, suggest uv)", python_command, 2)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, hook_input, expected_exit in tests:
        if test_validator(test_name, hook_input, expected_exit):
            passed += 1
    
    print(f"\n{'=' * 50}")
    print(f"Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())