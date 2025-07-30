"""Context-aware response analyzer for tool combinations and workflow patterns."""

import json
import os
import time
from typing import Dict, List, Any, Optional, cast
from dataclasses import dataclass, asdict
from .hook_response import HookResponse, ResponseBuilder, ValidationStage


@dataclass
class ToolUsageEvent:
    """Record of a tool usage event."""

    timestamp: float
    tool_name: str
    tool_input: Dict[str, Any]
    file_path: Optional[str] = None
    outcome: str = "unknown"  # approved, warned, blocked


class ContextAnalyzer:
    """Analyzes tool usage patterns and provides context-aware recommendations."""

    def __init__(self, history_file: Optional[str] = None):
        """Initialize context analyzer with optional history file."""
        self.history_file = history_file or ".claude_tool_history.json"
        self.max_history_size = 100
        self.context_window_minutes = 30

    def record_tool_usage(
        self, tool_name: str, tool_input: Dict[str, Any], outcome: str
    ) -> None:
        """Record a tool usage event for context analysis."""
        event = ToolUsageEvent(
            timestamp=time.time(),
            tool_name=tool_name,
            tool_input=tool_input,
            file_path=self._extract_file_path(tool_input),
            outcome=outcome,
        )

        history = self._load_history()
        history.append(asdict(event))

        # Trim history to max size
        if len(history) > self.max_history_size:
            history = history[-self.max_history_size :]

        self._save_history(history)

    def get_context_aware_response(
        self, tool_name: str, tool_input: Dict[str, Any], base_response: HookResponse
    ) -> HookResponse:
        """Enhance base response with context-aware recommendations."""

        # Get recent tool usage context
        recent_tools = self._get_recent_tool_usage()
        current_file = self._extract_file_path(tool_input)

        # Analyze patterns and enhance response
        enhancements = []

        # Pattern 1: Rapid file editing without testing
        if self._detect_edit_without_test_pattern(recent_tools, tool_name):
            enhancements.append("Consider running tests after making changes")

        # Pattern 2: Writing code without imports/dependencies
        if self._detect_missing_imports_pattern(tool_name, tool_input, recent_tools):
            enhancements.append("Check if required imports/dependencies are included")

        # Pattern 3: Multiple bash commands - suggest script
        if self._detect_multiple_bash_pattern(recent_tools, tool_name):
            enhancements.append("Consider creating a script for repeated bash commands")

        # Pattern 4: Working on same file repeatedly
        if self._detect_file_focus_pattern(recent_tools, current_file):
            enhancements.append(
                "Frequent edits to same file - consider breaking into smaller functions"
            )

        # Pattern 5: Test-driven development workflow
        if self._detect_tdd_pattern(recent_tools, tool_name, tool_input):
            enhancements.append("Great TDD workflow! Red -> Green -> Refactor")

        # Pattern 6: Code review preparation
        if self._detect_review_prep_pattern(recent_tools, tool_name):
            enhancements.append(
                "Changes ready for review - consider running final tests and formatting"
            )

        # Add context-aware enhancements to the response
        if enhancements:
            enhanced_suggestions = list(base_response.metadata.suggestions)
            enhanced_notes = list(base_response.metadata.educational_notes)
            enhanced_notes.extend(enhancements)

            # Create enhanced response
            if base_response.decision.value == "approve":
                return ResponseBuilder.approve(
                    reason=base_response.reason + " (with context insights)",
                    risk_level=base_response.metadata.risk_level,
                    suggestions=enhanced_suggestions,
                    educational_notes=enhanced_notes,
                    validation_stage=ValidationStage.SECURITY,
                    tool_name=tool_name,
                )
            elif base_response.decision.value == "warn":
                return ResponseBuilder.warn(
                    reason=base_response.reason + " (with context insights)",
                    risk_level=base_response.metadata.risk_level,
                    suggestions=enhanced_suggestions,
                    educational_notes=enhanced_notes,
                    validation_stage=ValidationStage.SECURITY,
                    tool_name=tool_name,
                )

        return base_response

    def _load_history(self) -> List[Dict[str, Any]]:
        """Load tool usage history from file."""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, "r") as f:
                    return cast(List[Dict[str, Any]], json.load(f))
        except (json.JSONDecodeError, IOError):
            pass
        return []

    def _save_history(self, history: List[Dict[str, Any]]) -> None:
        """Save tool usage history to file."""
        try:
            with open(self.history_file, "w") as f:
                json.dump(history, f, indent=2)
        except IOError:
            pass  # Fail silently for history tracking

    def _get_recent_tool_usage(self) -> List[ToolUsageEvent]:
        """Get recent tool usage within context window."""
        history = self._load_history()
        current_time = time.time()
        window_seconds = self.context_window_minutes * 60

        recent_events = []
        for event_dict in history:
            if current_time - event_dict["timestamp"] <= window_seconds:
                event = ToolUsageEvent(**event_dict)
                recent_events.append(event)

        return sorted(recent_events, key=lambda x: x.timestamp)

    def _extract_file_path(self, tool_input: Dict[str, Any]) -> Optional[str]:
        """Extract file path from tool input."""
        return tool_input.get("file_path") or tool_input.get("path")

    def _detect_edit_without_test_pattern(
        self, recent_tools: List[ToolUsageEvent], current_tool: str
    ) -> bool:
        """Detect if user is editing code without running tests."""
        if current_tool not in ["Write", "Edit", "MultiEdit"]:
            return False

        # Look for recent file modifications without test runs
        recent_edits = [
            t
            for t in recent_tools[-5:]
            if t.tool_name in ["Write", "Edit", "MultiEdit"]
        ]
        recent_tests = [
            t
            for t in recent_tools[-5:]
            if "test" in str(t.tool_input).lower()
            or "pytest" in str(t.tool_input).lower()
        ]

        return len(recent_edits) >= 2 and len(recent_tests) == 0

    def _detect_missing_imports_pattern(
        self,
        tool_name: str,
        tool_input: Dict[str, Any],
        recent_tools: List[ToolUsageEvent],
    ) -> bool:
        """Detect if writing code that might need imports."""
        if tool_name != "Write":
            return False

        content = tool_input.get("content", "")
        file_path = tool_input.get("file_path", "")

        # Check if writing Python code with function calls but no imports
        if file_path.endswith(".py") and content:
            # Look for function calls that might need imports
            import_indicators = [
                "requests.",
                "numpy.",
                "pandas.",
                "json.",
                "os.",
                "sys.",
                "subprocess.",
            ]
            has_indicators = any(
                indicator in content for indicator in import_indicators
            )
            has_imports = "import " in content or "from " in content

            return has_indicators and not has_imports

        return False

    def _detect_multiple_bash_pattern(
        self, recent_tools: List[ToolUsageEvent], current_tool: str
    ) -> bool:
        """Detect repeated bash commands that could be scripted."""
        if current_tool != "Bash":
            return False

        recent_bash = [t for t in recent_tools[-5:] if t.tool_name == "Bash"]
        return len(recent_bash) >= 3

    def _detect_file_focus_pattern(
        self, recent_tools: List[ToolUsageEvent], current_file: Optional[str]
    ) -> bool:
        """Detect repeated edits to the same file."""
        if not current_file:
            return False

        recent_same_file = [
            t
            for t in recent_tools[-5:]
            if t.file_path == current_file
            and t.tool_name in ["Write", "Edit", "MultiEdit"]
        ]
        return len(recent_same_file) >= 3

    def _detect_tdd_pattern(
        self,
        recent_tools: List[ToolUsageEvent],
        current_tool: str,
        tool_input: Dict[str, Any],
    ) -> bool:
        """Detect test-driven development workflow patterns."""
        # Look for test-first, then implementation pattern
        recent_events = recent_tools[-3:]

        test_related = [
            "test_" in str(event.tool_input).lower()
            or "test" in str(event.file_path or "").lower()
            for event in recent_events
        ]

        return any(test_related) and current_tool in ["Write", "Edit"]

    def _detect_review_prep_pattern(
        self, recent_tools: List[ToolUsageEvent], current_tool: str
    ) -> bool:
        """Detect code review preparation pattern."""
        # Look for formatting, linting, testing sequence
        recent_bash = [t for t in recent_tools[-5:] if t.tool_name == "Bash"]

        formatting_commands = ["black", "ruff", "mypy", "pytest", "test"]
        recent_formatting = any(
            any(cmd in str(event.tool_input).lower() for cmd in formatting_commands)
            for event in recent_bash
        )

        return recent_formatting and len(recent_bash) >= 2
