"""Pytest configuration for TDD reporter plugin."""

import pytest
from claude_code_adk_validator.pytest_reporter import PytestReporter


# Create a global reporter instance with proper data directory
_reporter = PytestReporter(data_dir=".claude/claude-code-adk-validator/data")


def pytest_configure(config):
    """Register the TDD reporter plugin."""
    config.pluginmanager.register(_reporter, "tdd-reporter")


def pytest_unconfigure(config):
    """Unregister the TDD reporter plugin."""
    config.pluginmanager.unregister(_reporter)