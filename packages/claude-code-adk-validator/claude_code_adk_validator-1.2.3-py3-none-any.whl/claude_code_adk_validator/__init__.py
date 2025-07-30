"""
Claude Code ADK-Inspired Validation Hooks

Advanced multi-stage validation system for Claude Code with hook chaining, context intelligence, and structured JSON responses.
"""

__version__ = "1.2.3"
__author__ = "Jihun Kim"
__email__ = "jihunkim0@noreply.github.com"

from .validator import ClaudeToolValidator

__all__ = ["ClaudeToolValidator"]
