"""
Claude Code ADK-Inspired Validation Hooks

Intelligent security validation for Claude Code tool execution using Google Gemini and ADK-inspired patterns.
"""

__version__ = "1.0.0"
__author__ = "Jihun Kim"
__email__ = "jihunkim0@noreply.github.com"

from .validator import ClaudeToolValidator

__all__ = ["ClaudeToolValidator"]
