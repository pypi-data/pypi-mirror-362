"""Modular validation components for staged validation."""

import re
from typing import Dict, Any, Optional
from .hook_response import HookResponse, ResponseBuilder, RiskLevel, ValidationStage


class SecurityValidator:
    """Security-focused validator for dangerous commands and patterns."""

    def validate_operation(
        self, tool_name: str, tool_input: Dict[str, Any], context: str = ""
    ) -> HookResponse:
        """Validate operation for security threats."""

        if tool_name == "Bash":
            return self._validate_bash_security(tool_input, context)
        elif tool_name in ["Write", "Edit", "MultiEdit", "Update"]:
            return self._validate_file_security(tool_input, context)
        else:
            return ResponseBuilder.approve(
                reason="No security concerns for this tool",
                tool_name=tool_name,
                validation_stage=ValidationStage.SECURITY,
            )

    def _validate_bash_security(
        self, tool_input: Dict[str, Any], context: str
    ) -> HookResponse:
        """Validate bash commands for security threats."""
        command = tool_input.get("command", "")

        # Critical security patterns that should always be blocked
        critical_patterns = [
            (r"rm\s+-rf\s+/", "System destruction command detected"),
            (r":\(\)\{.*\|\&\}", "Fork bomb detected"),
            (r"mkfs\.", "Filesystem creation command detected"),
            (r"dd\s+.*of=/dev/", "Direct device write detected"),
            (r">\s*/etc/passwd", "System password file modification"),
            (r"curl.*\|\s*bash", "Downloading and executing remote scripts"),
            (r"wget.*\|\s*sh", "Downloading and executing remote scripts"),
            (r"chmod\s+777\s+/", "Dangerous permission change on root"),
        ]

        for pattern, reason in critical_patterns:
            if re.search(pattern, command, re.IGNORECASE):
                return ResponseBuilder.block(
                    reason=f"Critical security threat: {reason}",
                    risk_level=RiskLevel.CRITICAL,
                    security_concerns=[reason],
                    suggestions=["Avoid destructive system commands"],
                    tool_name="Bash",
                    validation_stage=ValidationStage.SECURITY,
                    detected_patterns=[pattern],
                )

        # Tool enforcement patterns (medium risk)
        tool_patterns = [
            (
                r"^grep\b|^\s*grep\b",
                "Use 'rg' (ripgrep) instead of 'grep' for better performance",
            ),
            (
                r"^find\s+.*-name\b",
                "Use 'rg --files -g pattern' instead of 'find -name'",
            ),
            (r"^(python|python3)\b", "Use 'uv run python' instead of direct python"),
            (
                r"git\s+checkout\s+-b\b",
                "Prefer 'gh issue develop' for new feature branches",
            ),
            (
                r"git\s+switch\s+-c\b",
                "Prefer 'gh issue develop' for new feature branches",
            ),
            (r"cat\s*>", "Use proper Write/Edit tools instead of 'cat >'"),
        ]

        for pattern, suggestion in tool_patterns:
            if re.search(pattern, command, re.IGNORECASE):
                return ResponseBuilder.warn(
                    reason=suggestion,
                    risk_level=RiskLevel.MEDIUM,
                    suggestions=[suggestion],
                    tool_name="Bash",
                    validation_stage=ValidationStage.SECURITY,
                    detected_patterns=[pattern],
                )

        return ResponseBuilder.approve(
            reason="No security threats detected in bash command",
            risk_level=RiskLevel.LOW,
            tool_name="Bash",
            validation_stage=ValidationStage.SECURITY,
        )

    def _validate_file_security(
        self, tool_input: Dict[str, Any], context: str
    ) -> HookResponse:
        """Validate file operations for security threats."""
        file_path = tool_input.get("file_path", "")
        content = tool_input.get("content", "")

        # Path traversal and dangerous paths
        if (
            "../" in file_path
            or file_path.startswith("/etc/")
            or file_path.startswith("/bin/")
            or file_path.startswith("/usr/bin/")
        ):
            return ResponseBuilder.block(
                reason="Dangerous file path - outside project boundary or system directory",
                risk_level=RiskLevel.CRITICAL,
                security_concerns=["Path traversal or system directory access"],
                suggestions=["Only write files within the project directory"],
                tool_name=tool_input.get("tool_name", "File"),
                validation_stage=ValidationStage.SECURITY,
            )

        # Emoji detection
        emoji_pattern = re.compile(
            "["
            "\U0001f600-\U0001f64f"  # emoticons
            "\U0001f300-\U0001f5ff"  # symbols & pictographs
            "\U0001f680-\U0001f6ff"  # transport & map symbols
            "\U0001f1e0-\U0001f1ff"  # flags
            "\U00002600-\U000027bf"  # miscellaneous symbols
            "\U0001f900-\U0001f9ff"  # supplemental symbols
            "\U00002b50-\U00002b55"  # stars
            "]+",
            re.UNICODE,
        )

        if emoji_pattern.search(content):
            return ResponseBuilder.block(
                reason="Emojis are not allowed in code or documentation",
                risk_level=RiskLevel.MEDIUM,
                security_concerns=["Emoji usage in code"],
                suggestions=["Remove all emojis from the content"],
                tool_name=tool_input.get("tool_name", "File"),
                validation_stage=ValidationStage.SECURITY,
            )

        # Simple secret detection for obvious cases
        if re.search(r"sk_live_[a-zA-Z0-9]{24,}", content):
            return ResponseBuilder.block(
                reason="Real Stripe API key detected",
                risk_level=RiskLevel.CRITICAL,
                security_concerns=["Real API key exposure"],
                suggestions=["Use environment variables for API keys"],
                tool_name=tool_input.get("tool_name", "File"),
                validation_stage=ValidationStage.SECURITY,
            )

        # Documentation file validation
        if file_path.endswith((".md", ".rst", ".txt")):
            if (
                "documentation" in file_path.lower()
                or "feature" in content.lower()
                or content.startswith("# New Feature")
            ):
                return ResponseBuilder.block(
                    reason="Unauthorized documentation file creation detected",
                    risk_level=RiskLevel.MEDIUM,
                    security_concerns=["Unauthorized documentation creation"],
                    suggestions=["Only create documentation when explicitly requested"],
                    tool_name=tool_input.get("tool_name", "File"),
                    validation_stage=ValidationStage.SECURITY,
                )

        return ResponseBuilder.approve(
            reason="No security threats detected in file operation",
            risk_level=RiskLevel.LOW,
            tool_name=tool_input.get("tool_name", "File"),
            validation_stage=ValidationStage.SECURITY,
        )


class TDDValidator:
    """Test-Driven Development validator."""

    def validate_operation(
        self, tool_name: str, tool_input: Dict[str, Any], context: str = ""
    ) -> HookResponse:
        """Validate operation for TDD compliance."""

        if tool_name in ["Write", "Edit", "MultiEdit", "Update"]:
            return self._validate_tdd_compliance(tool_input, context)
        else:
            return ResponseBuilder.approve(
                reason="TDD validation not applicable for this tool",
                tool_name=tool_name,
                validation_stage=ValidationStage.TDD,
            )

    def _validate_tdd_compliance(
        self, tool_input: Dict[str, Any], context: str
    ) -> HookResponse:
        """Validate TDD compliance for file operations."""
        file_path = tool_input.get("file_path", "")
        content = tool_input.get("content", "")

        # Simple TDD validation - check if it's a test file
        if (
            "test" in file_path.lower()
            or file_path.endswith("_test.py")
            or file_path.startswith("test_")
            or "import pytest" in content
            or "import unittest" in content
            or "def test_" in content
        ):
            return ResponseBuilder.approve(
                reason="Test file creation/modification - following TDD practices",
                risk_level=RiskLevel.LOW,
                educational_notes=["Writing tests first is good TDD practice"],
                tool_name=tool_input.get("tool_name", "File"),
                validation_stage=ValidationStage.TDD,
            )

        # Check for implementation without tests (simplified check)
        if file_path.endswith(".py") and ("def " in content or "class " in content):
            return ResponseBuilder.warn(
                reason="Implementation code detected - ensure corresponding tests exist",
                risk_level=RiskLevel.MEDIUM,
                suggestions=[
                    "Consider writing tests first (Red phase)",
                    "Ensure test coverage for new functionality",
                    "Follow Red-Green-Refactor cycle",
                ],
                educational_notes=[
                    "TDD cycle: Red (failing test) → Green (minimal implementation) → Refactor"
                ],
                tool_name=tool_input.get("tool_name", "File"),
                validation_stage=ValidationStage.TDD,
            )

        return ResponseBuilder.approve(
            reason="No TDD concerns for this file type",
            tool_name=tool_input.get("tool_name", "File"),
            validation_stage=ValidationStage.TDD,
        )


class FileAnalysisValidator:
    """Advanced file analysis validator using LLM when available."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key

        # Import LLM validator if available
        try:
            from .llm_validator import LLMValidator

            self.llm_validator = LLMValidator(api_key=api_key) if api_key else None
        except ImportError:
            self.llm_validator = None

    def validate_operation(
        self, tool_name: str, tool_input: Dict[str, Any], context: str = ""
    ) -> HookResponse:
        """Validate operation using advanced file analysis."""

        if tool_name in ["Write", "Edit", "MultiEdit", "Update"]:
            return self._validate_file_content(tool_input, context)
        else:
            return ResponseBuilder.approve(
                reason="File analysis not applicable for this tool",
                tool_name=tool_name,
                validation_stage=ValidationStage.FILE_ANALYSIS,
            )

    def _validate_file_content(
        self, tool_input: Dict[str, Any], context: str
    ) -> HookResponse:
        """Validate file content using LLM analysis if available."""

        # If LLM validator is available, use it for advanced analysis
        if self.llm_validator:
            try:
                result = self.llm_validator.validate_operation(
                    tool_input.get("tool_name", "File"), tool_input, context
                )

                # Convert LLM result to HookResponse
                if result.get("approved", True):
                    return ResponseBuilder.approve(
                        reason=result.get("reason", "LLM analysis passed"),
                        risk_level=RiskLevel.LOW,
                        suggestions=result.get("suggestions", []),
                        educational_notes=result.get("educational_notes", []),
                        tool_name=tool_input.get("tool_name", "File"),
                        validation_stage=ValidationStage.FILE_ANALYSIS,
                    )
                else:
                    risk_level_map = {
                        "low": RiskLevel.LOW,
                        "medium": RiskLevel.MEDIUM,
                        "high": RiskLevel.HIGH,
                        "critical": RiskLevel.CRITICAL,
                    }
                    risk_level = risk_level_map.get(
                        result.get("risk_level", "medium"), RiskLevel.MEDIUM
                    )

                    if risk_level in [RiskLevel.CRITICAL, RiskLevel.HIGH]:
                        return ResponseBuilder.block(
                            reason=result.get("reason", "LLM analysis failed"),
                            risk_level=risk_level,
                            security_concerns=result.get("security_concerns", []),
                            suggestions=result.get("suggestions", []),
                            educational_notes=result.get("educational_notes", []),
                            tool_name=tool_input.get("tool_name", "File"),
                            validation_stage=ValidationStage.FILE_ANALYSIS,
                        )
                    else:
                        return ResponseBuilder.warn(
                            reason=result.get("reason", "LLM analysis raised concerns"),
                            risk_level=risk_level,
                            security_concerns=result.get("security_concerns", []),
                            suggestions=result.get("suggestions", []),
                            educational_notes=result.get("educational_notes", []),
                            tool_name=tool_input.get("tool_name", "File"),
                            validation_stage=ValidationStage.FILE_ANALYSIS,
                        )

            except Exception as e:
                return ResponseBuilder.warn(
                    reason=f"LLM analysis error: {str(e)}",
                    risk_level=RiskLevel.MEDIUM,
                    suggestions=["Manual review recommended"],
                    tool_name=tool_input.get("tool_name", "File"),
                    validation_stage=ValidationStage.FILE_ANALYSIS,
                )

        # Fallback to basic analysis
        return ResponseBuilder.approve(
            reason="Basic file analysis passed - no LLM analysis available",
            risk_level=RiskLevel.LOW,
            educational_notes=["Advanced analysis requires GEMINI_API_KEY"],
            tool_name=tool_input.get("tool_name", "File"),
            validation_stage=ValidationStage.FILE_ANALYSIS,
        )
