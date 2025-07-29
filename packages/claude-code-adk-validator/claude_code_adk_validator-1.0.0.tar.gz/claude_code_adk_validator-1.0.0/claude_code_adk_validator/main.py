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

try:
    from .validator import ClaudeToolValidator
except ImportError:
    # Handle direct execution
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from hooks.adk_validator import ClaudeToolValidator


def setup_claude_hooks(validator_command: str = "uvx claude-code-adk-validator") -> None:
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
                            "timeout": 8000
                        }
                    ]
                }
            ]
        }
    }
    
    # Merge with existing configuration if present
    if settings_file.exists():
        try:
            with open(settings_file, 'r') as f:
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
        with open(settings_file, 'w') as f:
            json.dump(hook_config, f, indent=2)
        
        print(f"✅ Claude Code hooks configured successfully!")
        print(f"Configuration written to: {settings_file}")
        print(f"Hook command: {validator_command}")
        
        # Check for API key
        if not os.environ.get("GEMINI_API_KEY"):
            print("\n⚠️  Don't forget to set your GEMINI_API_KEY environment variable:")
            print("export GEMINI_API_KEY='your_gemini_api_key'")
            
    except IOError as e:
        print(f"❌ Error writing configuration: {e}")
        sys.exit(1)


def validate_hook_input() -> None:
    """Main validation function for Claude Code hooks."""
    try:
        # Read hook input from stdin
        hook_input = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        print("Invalid JSON input", file=sys.stderr)
        sys.exit(0)

    # Check for API key
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY not configured - allowing all operations", file=sys.stderr)
        sys.exit(0)

    # Initialize validator and perform validation
    validator = ClaudeToolValidator(api_key)
    validation = validator.before_tool_callback(hook_input)

    if validation is None:
        # Operation approved
        sys.exit(0)
    else:
        # Operation blocked
        print(json.dumps(validation), file=sys.stderr)
        sys.exit(2)


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
        """
    )
    
    parser.add_argument(
        "--setup",
        action="store_true",
        help="Setup Claude Code hooks configuration"
    )
    
    parser.add_argument(
        "--version",
        action="store_true", 
        help="Show version information"
    )
    
    parser.add_argument(
        "--validator-command",
        default="uvx claude-code-adk-validator",
        help="Command to use in hook configuration (default: uvx claude-code-adk-validator)"
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
        print("🔧 Setting up Claude Code hooks...")
        setup_claude_hooks(args.validator_command)
        return
    
    # Default behavior: run as validation hook
    validate_hook_input()


if __name__ == "__main__":
    main()