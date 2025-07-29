#!/usr/bin/env python3
"""
Entry point for running claude-code-adk-validator as a module.

This allows the package to be executed as: python -m claude_code_adk_validator
"""

import sys
import json
import os
from .validator import ClaudeToolValidator


def main() -> None:
    """Main entry point for module execution."""
    try:
        # Read JSON input from stdin
        input_data = sys.stdin.read().strip()
        if not input_data:
            print("Invalid JSON input", file=sys.stderr)
            sys.exit(1)

        tool_request = json.loads(input_data)

        # Get API key from environment
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            # No API key: run basic rule-based validation only
            print(
                "GEMINI_API_KEY not configured - running basic validation only",
                file=sys.stderr,
            )

        # Initialize validator (works with or without API key)
        validator = ClaudeToolValidator(api_key)

        # Validate the request
        result = validator.before_tool_callback(tool_request)

        if result is None:
            # Allow execution
            sys.exit(0)
        else:
            # Block execution
            print(json.dumps(result), file=sys.stderr)
            sys.exit(2)

    except json.JSONDecodeError:
        print("Invalid JSON input", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        # Fail-safe: allow execution on validator errors
        print(f"Validator error: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
