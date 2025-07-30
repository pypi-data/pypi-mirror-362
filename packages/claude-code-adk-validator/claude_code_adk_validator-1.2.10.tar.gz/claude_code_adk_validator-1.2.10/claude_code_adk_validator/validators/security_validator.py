"""Security-focused validator inspired by tdd-guard's modular approach."""

import re
import os
import sys
from typing import Dict, Any, Optional
from ..hook_response import HookResponse, ResponseBuilder, RiskLevel, ValidationStage
from ..context_analyzer import ContextAnalyzer

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None


class SecurityValidator:
    """Dedicated security validation with operation-specific analysis."""

    def __init__(
        self, enable_context_analysis: bool = True, api_key: Optional[str] = None
    ):
        """Initialize security validator with optional context analysis and LLM."""
        self.context_analyzer = ContextAnalyzer() if enable_context_analysis else None
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        self.client = (
            genai.Client(api_key=self.api_key) if self.api_key and genai else None
        )

    # Security patterns from our existing LLM validator
    CRITICAL_PATTERNS = [
        (r"rm\s+-rf\s+/", "System destruction command detected"),
        (r"curl.*\|.*bash", "Malicious download and execution pattern"),
        (r"wget.*\|.*sh", "Dangerous download pipe to shell"),
        (r">\s*/etc/", "Unauthorized system file modification"),
        (r">\s*/bin/", "Unauthorized system binary modification"),
    ]

    CREDENTIAL_PATTERNS = [
        (r"sk_live_[a-zA-Z0-9]{24,}", "Real Stripe API key detected"),
        (r"ghp_[a-zA-Z0-9]{36}", "GitHub personal access token detected"),
        (r"AKIA[0-9A-Z]{16}", "AWS access key detected"),
        (r"-----BEGIN [A-Z ]+PRIVATE KEY-----", "Private key detected"),
    ]

    TOOL_ENFORCEMENT_PATTERNS = [
        (r"^grep\b|^\s*grep\b", "Use 'rg' (ripgrep) instead of 'grep'"),
        (r"^find\s+.*-name\b", "Use 'rg --files -g pattern' instead of 'find -name'"),
        (r"^(python|python3)\b", "Use 'uv run python' instead of direct python"),
        (r"cat\s*>", "Use proper Write/Edit tools instead of 'cat >'"),
        (r"git checkout -b\b", "Use 'gh issue develop' for feature branch creation"),
    ]

    def analyze_with_llm(
        self, command: str, tool_name: str, context: str = ""
    ) -> Optional[HookResponse]:
        """Use LLM for deep security analysis."""
        if not self.client:
            return None

        try:
            prompt = f"""Analyze this {tool_name} operation for security threats:

Command/Operation: {command}
Context: {context or 'No additional context'}

Check for:
1. Security vulnerabilities (injection, privilege escalation, data exposure)
2. Malicious patterns or suspicious behavior
3. Compliance violations (PII handling, credentials)
4. Best practice violations

Respond with:
- threat_level: critical/high/medium/low/none
- reason: Brief explanation if threat found
- suggestions: List of recommendations
"""

            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.1,
                    max_output_tokens=500,
                ),
            )

            # Parse response and determine action
            response_text = response.text.lower()

            if (
                "threat_level: critical" in response_text
                or "threat_level: high" in response_text
            ):
                reason_match = re.search(
                    r"reason:\s*(.+?)(?:\n|$)", response.text, re.IGNORECASE
                )
                reason = (
                    reason_match.group(1).strip()
                    if reason_match
                    else "Security threat detected by AI analysis"
                )

                return ResponseBuilder.block(
                    reason=f"LLM Security Analysis: {reason}",
                    risk_level=RiskLevel.HIGH,
                    security_concerns=[reason],
                    suggestions=["Review operation for security implications"],
                    validation_stage=ValidationStage.SECURITY,
                    tool_name=tool_name,
                    educational_notes=[
                        "AI-powered security analysis detected potential threat"
                    ],
                )

        except Exception as e:
            # Log but don't fail on LLM errors
            print(f"LLM analysis error: {e}", file=sys.stderr)

        return None

    def validate_bash_operation(self, command: str, context: str = "") -> HookResponse:
        """Validate bash commands for security threats with defense in depth."""

        # Layer 1: Check critical security patterns (rule-based)
        for pattern, reason in self.CRITICAL_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                return ResponseBuilder.block(
                    reason=f"Critical security threat: {reason}",
                    risk_level=RiskLevel.CRITICAL,
                    security_concerns=[reason],
                    suggestions=["Avoid destructive system commands"],
                    validation_stage=ValidationStage.SECURITY,
                    tool_name="Bash",
                    detected_patterns=[pattern],
                )

        # Check tool enforcement patterns
        for pattern, suggestion in self.TOOL_ENFORCEMENT_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                return ResponseBuilder.block(
                    reason=f"Tool enforcement violation: {suggestion}",
                    risk_level=RiskLevel.MEDIUM,
                    suggestions=[suggestion],
                    educational_notes=[
                        "Modern tools provide better performance and features",
                        "Consistent tooling improves development workflow",
                    ],
                    validation_stage=ValidationStage.TOOL_ENFORCEMENT,
                    tool_name="Bash",
                    detected_patterns=[pattern],
                )

        # Check for sudo usage (warning level)
        if re.search(r"\bsudo\b", command, re.IGNORECASE):
            return ResponseBuilder.warn(
                reason="Command requires elevated privileges - ensure necessity",
                risk_level=RiskLevel.HIGH,
                suggestions=[
                    "Verify if sudo is truly required",
                    "Consider user-level alternatives",
                ],
                educational_notes=["Elevated privileges increase security risk"],
                validation_stage=ValidationStage.SECURITY,
                tool_name="Bash",
                detected_patterns=["sudo"],
            )

        # Layer 2: LLM analysis for defense in depth
        llm_response = self.analyze_with_llm(command, "Bash", context)
        if llm_response:
            return llm_response

        return ResponseBuilder.approve(
            reason="Command passed security validation",
            risk_level=RiskLevel.LOW,
            validation_stage=ValidationStage.SECURITY,
            tool_name="Bash",
        )

    def validate_file_operation(
        self, file_path: str, content: str, operation: str, context: str = ""
    ) -> HookResponse:
        """Validate file operations for security concerns."""

        # Path traversal detection
        if (
            "../" in file_path
            or file_path.startswith("/etc/")
            or file_path.startswith("/bin/")
        ):
            return ResponseBuilder.block(
                reason="Path traversal or system directory access detected",
                risk_level=RiskLevel.CRITICAL,
                security_concerns=["Path traversal attack", "System directory access"],
                suggestions=["Use relative paths within project boundary"],
                validation_stage=ValidationStage.SECURITY,
                tool_name=operation,
                detected_patterns=["path_traversal"],
            )

        # Credential detection in content
        for pattern, reason in self.CREDENTIAL_PATTERNS:
            if re.search(pattern, content):
                return ResponseBuilder.block(
                    reason=f"Real credential detected: {reason}",
                    risk_level=RiskLevel.CRITICAL,
                    security_concerns=[reason],
                    suggestions=["Use environment variables", "Use placeholder values"],
                    educational_notes=[
                        "Never commit real credentials to version control",
                        "Use configuration files with .env patterns",
                    ],
                    validation_stage=ValidationStage.SECURITY,
                    tool_name=operation,
                    detected_patterns=[pattern],
                )

        # Emoji detection (policy enforcement) - comprehensive coverage
        emoji_pattern = re.compile(
            "["
            "\U0001f600-\U0001f64f"  # emoticons
            "\U0001f300-\U0001f5ff"  # symbols & pictographs
            "\U0001f680-\U0001f6ff"  # transport & map symbols
            "\U0001f1e0-\U0001f1ff"  # flags
            "\U00002600-\U000027bf"  # miscellaneous symbols
            "\U0001f900-\U0001f9ff"  # supplemental symbols
            "\U00002b50-\U00002b55"  # stars
            "\U000023e9-\U000023ec"  # additional media symbols
            "\U000023f0-\U000023f3"  # timer/clock symbols (includes ⏳)
            "\U0000231a-\U0000231b"  # watch symbols
            "\U00002194-\U00002199"  # arrow symbols
            "\U000021a9-\U000021aa"  # hooked arrows
            "\U00002139"  # information source
            "\U0000203c"  # double exclamation
            "\U00002049"  # exclamation question
            "\U000025aa-\U000025ab"  # small squares
            "\U000025b6"  # play button
            "\U000025c0"  # reverse button
            "\U000025fb-\U000025fe"  # medium squares
            "\U00002702"  # scissors
            "\U000027a1"  # right arrow
            "\U000027b0"  # curly loop
            "\U00002934-\U00002935"  # curved arrows
            "\U0001f004"  # mahjong red dragon
            "\U0001f0cf"  # playing card joker
            "\U0001f170-\U0001f251"  # enclosed characters
            "\U0001f980-\U0001f9ff"  # additional pictographs
            "]+",
            re.UNICODE,
        )

        if emoji_pattern.search(content):
            return ResponseBuilder.block(
                reason="Emojis are not allowed in code or documentation",
                risk_level=RiskLevel.MEDIUM,
                suggestions=["Remove all emojis from content"],
                educational_notes=[
                    "Professional code should avoid Unicode decorations"
                ],
                validation_stage=ValidationStage.SECURITY,
                tool_name=operation,
                detected_patterns=["emoji"],
            )

        # Unauthorized documentation file detection
        if file_path.endswith((".md", ".rst", ".txt")):
            if (
                "documentation" in file_path.lower()
                or "feature" in content.lower()
                or content.startswith("# New Feature")
            ):
                return ResponseBuilder.block(
                    reason="Unauthorized documentation file creation detected",
                    risk_level=RiskLevel.MEDIUM,
                    suggestions=["Only create documentation when explicitly requested"],
                    educational_notes=[
                        "Maintain project hygiene by avoiding generic docs"
                    ],
                    validation_stage=ValidationStage.SECURITY,
                    tool_name=operation,
                    detected_patterns=["unauthorized_docs"],
                )

        # Layer 2: LLM analysis for defense in depth
        llm_response = self.analyze_with_llm(
            f"File: {file_path}\nContent preview: {content[:200]}", operation, context
        )
        if llm_response:
            return llm_response

        return ResponseBuilder.approve(
            reason="File operation passed security validation",
            risk_level=RiskLevel.LOW,
            validation_stage=ValidationStage.SECURITY,
            tool_name=operation,
        )

    def validate_operation(
        self, tool_name: str, tool_input: Dict[str, Any], context: str = ""
    ) -> HookResponse:
        """Main entry point for security validation with context awareness."""

        # Perform base security validation
        base_response = self._perform_base_validation(tool_name, tool_input, context)

        # Record tool usage for context analysis
        if self.context_analyzer:
            outcome = base_response.decision.value
            self.context_analyzer.record_tool_usage(tool_name, tool_input, outcome)

            # Get context-aware enhanced response
            enhanced_response = self.context_analyzer.get_context_aware_response(
                tool_name, tool_input, base_response
            )
            return enhanced_response

        return base_response

    def _perform_base_validation(
        self, tool_name: str, tool_input: Dict[str, Any], context: str = ""
    ) -> HookResponse:
        """Perform base security validation without context awareness."""

        if tool_name == "Bash":
            command = tool_input.get("command", "")
            return self.validate_bash_operation(command, context)

        elif tool_name == "Write":
            file_path = tool_input.get("file_path", "")
            content = tool_input.get("content", "")
            return self.validate_file_operation(file_path, content, tool_name, context)

        elif tool_name == "Edit":
            file_path = tool_input.get("file_path", "")
            # For Edit, check both old_string and new_string for security issues
            old_string = tool_input.get("old_string", "")
            new_string = tool_input.get("new_string", "")
            # Combine both strings for comprehensive security checking
            combined_content = old_string + "\n" + new_string
            return self.validate_file_operation(
                file_path, combined_content, tool_name, context
            )

        elif tool_name == "MultiEdit":
            file_path = tool_input.get("file_path", "")
            # For MultiEdit, check all edit content
            edits = tool_input.get("edits", [])
            combined_content = ""
            for edit in edits:
                old_str = edit.get("old_string", "")
                new_str = edit.get("new_string", "")
                combined_content += old_str + "\n" + new_str + "\n"
            return self.validate_file_operation(
                file_path, combined_content, tool_name, context
            )

        elif tool_name == "Update":
            file_path = tool_input.get("file_path", "")
            content = tool_input.get("content", "")
            return self.validate_file_operation(file_path, content, tool_name, context)

        else:
            return ResponseBuilder.approve(
                reason="Tool not covered by security validation",
                risk_level=RiskLevel.LOW,
                validation_stage=ValidationStage.SECURITY,
                tool_name=tool_name,
            )
