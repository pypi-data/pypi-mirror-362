#!/usr/bin/env python3
"""
Main entry point for Claude Code ADK-Inspired Validator.

This module provides the command-line interface for the validator,
allowing it to be used with uvx and as a console script.
"""

import sys
import json
import os
import argparse
from pathlib import Path
from typing import Optional

from .hook_response import HookResponse, ResponseBuilder


def setup_claude_hooks(
    validator_command: str = "uvx claude-code-adk-validator",
) -> None:
    """Setup Claude Code hooks configuration."""
    claude_dir = Path.cwd() / ".claude"
    settings_file = claude_dir / "settings.local.json"

    # Create .claude directory if it doesn't exist
    claude_dir.mkdir(exist_ok=True)

    # Hook configuration
    hook_config = {
        "hooks": {
            "PreToolUse": [
                {
                    "matcher": "Write|Edit|Bash|MultiEdit",
                    "hooks": [
                        {
                            "type": "command",
                            "command": validator_command,
                            "timeout": 8000,
                        }
                    ],
                }
            ]
        }
    }

    # Merge with existing configuration if present
    if settings_file.exists():
        try:
            with open(settings_file, "r") as f:
                existing_config = json.load(f)

            # Merge configurations
            if "hooks" in existing_config:
                existing_config["hooks"].update(hook_config["hooks"])
            else:
                existing_config.update(hook_config)

            hook_config = existing_config
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not read existing configuration: {e}")
            print("Creating new configuration...")

    # Write configuration
    try:
        with open(settings_file, "w") as f:
            json.dump(hook_config, f, indent=2)

        print("SUCCESS: Claude Code hooks configured successfully!")
        print(f"Configuration written to: {settings_file}")
        print(f"Hook command: {validator_command}")

        # Check for API key
        if not os.environ.get("GEMINI_API_KEY"):
            print("\n⚠️  Don't forget to set your GEMINI_API_KEY environment variable:")
            print("export GEMINI_API_KEY='your_gemini_api_key'")

        # Provide setup instructions
        print("\n📋 Setup Instructions:")
        print(
            "1. Ensure the package is installed: uv tool install claude-code-adk-validator"
        )
        print("2. Set your GEMINI_API_KEY environment variable")
        print("3. Restart Claude Code for hooks to take effect")
        print("4. Test the setup with a simple Write operation")

    except IOError as e:
        print(f"ERROR: Error writing configuration: {e}")
        sys.exit(1)


def setup_claude_hooks_chaining(
    validator_command: str = "uvx claude-code-adk-validator",
) -> None:
    """Setup Claude Code hooks configuration with multi-stage chaining."""
    claude_dir = Path.cwd() / ".claude"
    settings_file = claude_dir / "settings.local.json"

    # Create .claude directory if it doesn't exist
    claude_dir.mkdir(exist_ok=True)

    # Hook configuration with chaining
    hook_config = {
        "hooks": {
            "PreToolUse": [
                {
                    "matcher": "Write|Edit|MultiEdit|Update",
                    "hooks": [
                        {
                            "type": "command",
                            "command": f"{validator_command} --stage=security",
                            "timeout": 8000,
                        },
                        {
                            "type": "command",
                            "command": f"{validator_command} --stage=tdd",
                            "timeout": 8000,
                        },
                        {
                            "type": "command",
                            "command": f"{validator_command} --stage=file-analysis",
                            "timeout": 8000,
                        },
                    ],
                },
                {
                    "matcher": "Bash",
                    "hooks": [
                        {
                            "type": "command",
                            "command": f"{validator_command} --stage=security",
                            "timeout": 8000,
                        }
                    ],
                },
            ]
        }
    }

    # Merge with existing configuration if present
    if settings_file.exists():
        try:
            with open(settings_file, "r") as f:
                existing_config = json.load(f)

            # Merge configurations
            if "hooks" in existing_config:
                existing_config["hooks"].update(hook_config["hooks"])
            else:
                existing_config.update(hook_config)

            hook_config = existing_config
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not read existing configuration: {e}")
            print("Creating new configuration...")

    # Write configuration
    try:
        with open(settings_file, "w") as f:
            json.dump(hook_config, f, indent=2)

        print("SUCCESS: Claude Code hooks with chaining configured successfully!")
        print(f"Configuration written to: {settings_file}")
        print(f"Hook command base: {validator_command}")
        print("\nChaining stages configured:")
        print("  - Security validation (all tools)")
        print("  - TDD validation (Write/Edit/MultiEdit/Update)")
        print("  - File analysis validation (Write/Edit/MultiEdit/Update)")

        # Check for API key
        if not os.environ.get("GEMINI_API_KEY"):
            print("\n⚠️  Don't forget to set your GEMINI_API_KEY environment variable:")
            print("export GEMINI_API_KEY='your_gemini_api_key'")

    except IOError as e:
        print(f"ERROR: Error writing configuration: {e}")
        sys.exit(1)


def validate_hook_input(stage: Optional[str] = None) -> None:
    """Main validation function with optional staging support."""
    try:
        # Read hook input from stdin
        hook_input = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        # Invalid JSON - write to stderr and exit with code 2
        print("Invalid JSON input provided to validator", file=sys.stderr)
        print(
            "Ensure the validator is being called by Claude Code hooks", file=sys.stderr
        )
        sys.exit(2)
    except Exception as e:
        # General error reading input
        print(f"Error reading hook input: {str(e)}", file=sys.stderr)
        print("This validator should be called by Claude Code hooks", file=sys.stderr)
        sys.exit(2)

    # Extract tool information (support both old and new formats)
    tool_name = hook_input.get("tool_name", "unknown")
    tool_input = hook_input.get("tool_input", {})

    # Handle legacy format from tests (has session_id, transcript_path, hook_event_name)
    if "session_id" in hook_input and "hook_event_name" in hook_input:
        # Legacy format - extract tool info from the structure
        tool_name = hook_input.get("tool_name", "unknown")
        tool_input = hook_input.get("tool_input", {})
    context = ""  # Could be enhanced to extract transcript context

    # Check for API key
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print(
            "GEMINI_API_KEY not configured - running basic validation only",
            file=sys.stderr,
        )

    try:
        # Run stage-specific or full validation
        if stage:
            response = run_staged_validation(
                stage, tool_name, tool_input, context, api_key
            )
        else:
            response = run_full_validation(tool_name, tool_input, context, api_key)

        # Output response based on decision
        if response.decision == "block":
            # For blocking: write to stderr and exit with code 2
            print(response.reason, file=sys.stderr)
            sys.exit(2)
        else:
            # For approve: write JSON to stdout and exit with code 0
            claude_json = response.to_claude_json()
            print(json.dumps(claude_json))
            sys.exit(0)

    except Exception as e:
        # Unexpected error - write to stderr and exit with code 2
        print(f"Validator error: {str(e)}", file=sys.stderr)
        sys.exit(2)


def run_staged_validation(
    stage: str, tool_name: str, tool_input: dict, context: str, api_key: Optional[str]
) -> HookResponse:
    """Run validation for specific stage."""
    from .validators import SecurityValidator, TDDValidator, FileAnalysisValidator

    if stage == "security":
        security_validator = SecurityValidator(api_key=api_key)
        return security_validator.validate_operation(tool_name, tool_input, context)

    elif stage == "tdd":
        tdd_validator = TDDValidator(api_key=api_key)
        return tdd_validator.validate_operation(tool_name, tool_input, context)

    elif stage == "file-analysis":
        file_validator = FileAnalysisValidator(api_key)
        return file_validator.validate_operation(tool_name, tool_input, context)

    else:
        return ResponseBuilder.approve(
            reason=f"Unknown stage: {stage}", tool_name=tool_name
        )


def run_full_validation(
    tool_name: str, tool_input: dict, context: str, api_key: Optional[str]
) -> HookResponse:
    """Run full validation pipeline with all stages."""
    from .validators import SecurityValidator, TDDValidator, FileAnalysisValidator

    # Run security validation first (highest priority)
    security_validator = SecurityValidator(api_key=api_key)
    security_response = security_validator.validate_operation(
        tool_name, tool_input, context
    )

    if security_response.decision == "block":
        return security_response

    # Run TDD validation
    tdd_validator = TDDValidator(api_key=api_key)
    tdd_response = tdd_validator.validate_operation(tool_name, tool_input, context)

    if tdd_response.decision == "block":
        return tdd_response

    # Run file analysis validation if API key available
    if api_key:
        file_validator = FileAnalysisValidator(api_key)
        file_response = file_validator.validate_operation(
            tool_name, tool_input, context
        )

        if file_response.decision == "block":
            return file_response

        # Return highest warning or approval
        if file_response.decision == "warn":
            return file_response
        if tdd_response.decision == "warn":
            return tdd_response
        if security_response.decision == "warn":
            return security_response

        return file_response

    # Return highest warning or approval
    if tdd_response.decision == "warn":
        return tdd_response
    if security_response.decision == "warn":
        return security_response

    return ResponseBuilder.approve(
        reason="All validation stages passed", tool_name=tool_name
    )


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Claude Code ADK-Inspired Validation Hooks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Setup Claude Code hooks configuration
  uvx claude-code-adk-validator --setup
  
  # Run as validation hook (used by Claude Code)
  uvx claude-code-adk-validator < hook_input.json
  
  # Show version information
  uvx claude-code-adk-validator --version
        """,
    )

    parser.add_argument(
        "--setup", action="store_true", help="Setup Claude Code hooks configuration"
    )

    parser.add_argument(
        "--setup-chaining",
        action="store_true",
        help="Setup Claude Code hooks with multi-stage chaining",
    )

    parser.add_argument(
        "--version", action="store_true", help="Show version information"
    )

    parser.add_argument(
        "--validator-command",
        default="uvx claude-code-adk-validator",
        help="Command to use in hook configuration (default: uvx claude-code-adk-validator)",
    )

    parser.add_argument(
        "--stage",
        choices=["security", "tdd", "file-analysis"],
        help="Run specific validation stage (enables modular hook chaining)",
    )

    # Parse arguments
    args = parser.parse_args()

    if args.version:
        from . import __version__

        print(f"claude-code-adk-validator {__version__}")
        print("Intelligent security validation for Claude Code tool execution")
        print("Using Google Gemini and ADK-inspired patterns")
        return

    if args.setup:
        print("INFO: Setting up Claude Code hooks...")
        setup_claude_hooks(args.validator_command)
        return

    if args.setup_chaining:
        print("INFO: Setting up Claude Code hooks with chaining...")
        setup_claude_hooks_chaining(args.validator_command)
        return

    # Default behavior: run as validation hook
    validate_hook_input(args.stage)


if __name__ == "__main__":
    main()
