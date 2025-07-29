#!/usr/bin/env python3

import json
import sys
import os
import re
import tempfile
from typing import Optional, List

try:
    from google import genai
    from google.genai import types
    from pydantic import BaseModel
except ImportError:
    print(
        "Error: google-genai or pydantic not installed. Run: pip install google-genai pydantic",
        file=sys.stderr,
    )
    sys.exit(0)


class ValidationResponse(BaseModel):
    approved: bool
    reason: str
    risk_level: str
    suggestions: Optional[List[str]] = []


class FileAnalysisResponse(BaseModel):
    security_issues: List[str]
    code_quality_concerns: List[str]
    risk_assessment: str
    recommendations: List[str]


class ClaudeToolValidator:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.client = genai.Client(api_key=api_key) if api_key else None
        self.model_name = "gemini-2.5-pro"
        self.decision_history: List[dict] = []
        self.uploaded_files: List[dict] = []

    def upload_file_for_analysis(self, file_path: str, content: str) -> Optional[str]:
        """Upload file content to Gemini for enhanced analysis"""
        if not self.client:
            return None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=os.path.splitext(file_path)[1], delete=False
            ) as temp_file:
                temp_file.write(content)
                temp_file_path = temp_file.name

            uploaded_file = self.client.files.upload(file=temp_file_path)
            self.uploaded_files.append(
                {"file_id": uploaded_file.name, "temp_path": temp_file_path}
            )
            return str(uploaded_file.name)
        except Exception:
            return None

    def analyze_uploaded_file(self, file_id: str, file_path: str) -> Optional[dict]:
        """Perform enhanced security analysis using uploaded file"""
        if not self.client:
            return None
        try:
            prompt = f"""Perform comprehensive security analysis of this file: {os.path.basename(file_path)}

Analyze for:
1. Security vulnerabilities (injections, exposures, dangerous functions)
2. Code quality issues (complexity, maintainability, best practices)
3. Configuration security (permissions, secrets, access controls)
4. Potential attack vectors and exploitation risks
5. Compliance with security standards

Focus on:
- Malicious code patterns
- Credential leaks or hardcoded secrets
- Unsafe file operations
- Network security issues
- Input validation gaps
- Authorization/authentication flaws

Provide structured assessment with specific security concerns and actionable recommendations."""

            uploaded_file = self.client.files.get(file_id)
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[prompt, uploaded_file],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=FileAnalysisResponse,
                    thinking_config=types.ThinkingConfig(thinking_budget=32768),
                ),
            )

            if hasattr(response, "parsed") and response.parsed:
                result = response.parsed
                return {
                    "security_issues": result.security_issues,
                    "code_quality_concerns": result.code_quality_concerns,
                    "risk_assessment": result.risk_assessment,
                    "recommendations": result.recommendations,
                }
            else:
                return dict(json.loads(response.text))
        except Exception:
            return None

    def cleanup_uploaded_files(self) -> None:
        """Clean up uploaded files and temporary files"""
        for file_info in self.uploaded_files:
            try:
                if os.path.exists(file_info["temp_path"]):
                    os.unlink(file_info["temp_path"])
            except Exception:
                pass
        self.uploaded_files = []

    def before_tool_callback(self, tool_request: dict) -> Optional[dict]:
        """ADK-inspired tool validation for Claude Code hooks"""

        tool_name = tool_request.get("tool_name", "")
        tool_input = tool_request.get("tool_input", {})
        transcript_path = tool_request.get("transcript_path", "")

        try:
            context = self.extract_conversation_context(transcript_path)
            validation_result = self.validate_tool_use(tool_name, tool_input, context)

            self.cleanup_uploaded_files()

            if validation_result["approved"]:
                return None
            else:
                return {"error": validation_result["reason"]}
        except Exception:
            self.cleanup_uploaded_files()
            return None

    def extract_conversation_context(self, transcript_path: str) -> str:
        """Extract recent conversation context from transcript"""
        try:
            if os.path.exists(transcript_path):
                with open(transcript_path, "r", encoding="utf-8") as f:
                    content = f.read()
                return content
        except Exception:
            pass
        return ""

    def validate_tool_use(self, tool_name: str, tool_input: dict, context: str) -> dict:
        """Main validation logic using Gemini with ADK patterns"""

        quick_check = self.perform_quick_validation(tool_name, tool_input)
        if not quick_check["approved"]:
            return quick_check

        # Skip LLM-dependent analysis if no API key
        if not self.api_key:
            return quick_check

        file_analysis = None
        if tool_name in ["Write", "Edit", "MultiEdit"] and "content" in tool_input:
            file_path = tool_input.get("file_path", "")
            content = tool_input.get("content", "")

            if content and len(content) > 500:
                file_id = self.upload_file_for_analysis(file_path, content)
                if file_id:
                    file_analysis = self.analyze_uploaded_file(file_id, file_path)
                    if file_analysis and file_analysis.get("security_issues"):
                        return {
                            "approved": False,
                            "reason": f"File analysis detected security issues: {', '.join(file_analysis['security_issues'][:3])}",
                            "risk_level": "high",
                            "suggestions": file_analysis.get("recommendations", []),
                        }

        if quick_check["risk_level"] == "low" and not file_analysis:
            return quick_check

        try:
            prompt = self.build_validation_prompt(
                tool_name, tool_input, context, file_analysis
            )

            grounding_tool = types.Tool(google_search=types.GoogleSearch())
            thinking_config = types.ThinkingConfig(thinking_budget=24576)

            assert self.client is not None  # Type guard for mypy
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=ValidationResponse,
                    tools=[grounding_tool],
                    thinking_config=thinking_config,
                ),
            )

            if hasattr(response, "parsed") and response.parsed:
                result = response.parsed
                return {
                    "approved": result.approved,
                    "reason": result.reason,
                    "risk_level": result.risk_level,
                    "suggestions": result.suggestions or [],
                }
            else:
                result = json.loads(response.text)
                required_fields = ["approved", "reason", "risk_level"]
                if all(field in result for field in required_fields):
                    return dict(result)
                else:
                    return {
                        "approved": False,
                        "reason": "Invalid response structure from validation service",
                        "risk_level": "high",
                    }
        except Exception as e:
            return {
                "approved": True,
                "reason": f"Validation service unavailable: {str(e)}",
                "risk_level": "unknown",
            }

    def perform_quick_validation(self, tool_name: str, tool_input: dict) -> dict:
        """Fast rule-based validation (Tier 1)"""

        if tool_name == "Bash":
            return self.validate_bash_command(tool_input)
        elif tool_name in ["Write", "Edit", "MultiEdit"]:
            return self.validate_file_operation(tool_input)
        else:
            return {"approved": True, "risk_level": "low"}

    def validate_bash_command(self, tool_input: dict) -> dict:
        """Enhanced validation for bash commands"""
        command = tool_input.get("command", "")

        critical_patterns = [
            r"rm\s+-rf\s+/",
            r"sudo\s+rm.*/",
            r"mkfs",
            r"dd\s+if=.*of=.*",
            r"curl.*\|\s*bash",
            r"wget.*\|\s*(bash|sh)",
            r"> /etc/",
            r"> /bin/",
            r"> /usr/",
        ]

        for pattern in critical_patterns:
            if re.search(pattern, command, re.IGNORECASE):
                return {
                    "approved": False,
                    "reason": "Dangerous command pattern detected: potentially destructive operation",
                    "risk_level": "critical",
                }

        # Performance/tool enforcement - block inefficient commands
        tool_enforcement = [
            (
                r"^grep\b|^\s*grep\b",
                "Use 'rg' (ripgrep) instead of 'grep' for better performance and features. Command blocked to enforce best practices.",
            ),
            (
                r"^find\s+.*-name\b|^\s*find\s+.*-name\b",
                "Use 'rg --files -g pattern' or 'rg --files | rg pattern' instead of 'find -name' for better performance. Command blocked to enforce best practices.",
            ),
            (
                r"^(python|python3)\b|^\s*(python|python3)\b",
                "Use 'uv run python' instead of direct python for better dependency management and virtual environment handling. Command blocked to enforce best practices.",
            ),
        ]

        for pattern, suggestion in tool_enforcement:
            if re.search(pattern, command, re.IGNORECASE):
                return {
                    "approved": False,
                    "reason": suggestion,
                    "risk_level": "medium",
                    "suggestions": [suggestion.split(". Command blocked")[0]],
                }

        warning_patterns = [
            r"sudo",
            r"rm\s+-rf",
            r"git\s+reset\s+--hard",
            r"npm\s+uninstall",
            r"pip\s+uninstall",
        ]

        for pattern in warning_patterns:
            if re.search(pattern, command, re.IGNORECASE):
                return {
                    "approved": True,
                    "reason": "Command requires elevated privileges or has destructive potential",
                    "risk_level": "high",
                }

        return {"approved": True, "risk_level": "medium"}

    def validate_file_operation(self, tool_input: dict) -> dict:
        """Enhanced validation for file operations"""
        file_path = tool_input.get("file_path", "")
        content = tool_input.get("content", "")

        if (
            "../" in file_path
            or file_path.startswith("/etc/")
            or file_path.startswith("/bin/")
        ):
            return {
                "approved": False,
                "reason": "Potentially dangerous file path - outside project boundary or system directory",
                "risk_level": "critical",
            }

        # Let LLM handle secret detection with better context awareness
        # Only keep critical obvious patterns here if needed

        if file_path.endswith(".py") and (
            "import os" in content and "system(" in content
        ):
            return {
                "approved": False,
                "reason": "Potential shell injection pattern in Python code",
                "risk_level": "high",
            }

        return {"approved": True, "risk_level": "low"}

    def build_validation_prompt(
        self,
        tool_name: str,
        tool_input: dict,
        context: str,
        file_analysis: Optional[dict] = None,
    ) -> str:
        """Build validation prompt for Gemini with structured output and Google Search"""

        file_analysis_section = ""
        if file_analysis:
            file_analysis_section = f"""
FILE_ANALYSIS_RESULTS:
Security Issues Detected: {json.dumps(file_analysis.get('security_issues', []), indent=2)}
Code Quality Concerns: {json.dumps(file_analysis.get('code_quality_concerns', []), indent=2)}
Risk Assessment: {file_analysis.get('risk_assessment', 'Not available')}
Recommendations: {json.dumps(file_analysis.get('recommendations', []), indent=2)}
"""

        return f"""You are a critical security validator for Claude Code tool execution. Your job is to BLOCK dangerous operations and ALLOW safe ones.

TOOL: {tool_name}
INPUT: {json.dumps(tool_input, indent=2)}
RECENT_CONTEXT: {context[-800:]}
{file_analysis_section}

CRITICAL SECURITY RULES - YOU MUST BLOCK THESE:

1. **ALWAYS BLOCK Real Credentials/Secrets**:
   - AWS keys (AKIA..., 40-char base64 strings)
   - GitHub tokens (ghp_..., gho_..., ghr_...)  
   - Stripe keys (sk_live_..., pk_live_...)
   - JWT tokens (ey...ey...signature)
   - API keys that look real (long, random, not placeholders)
   - Actual passwords in configuration files
   - Private keys, certificates, or tokens

2. **ALWAYS BLOCK Dangerous Commands**:
   - System destruction (rm -rf /, mkfs, dd to devices)
   - Malicious downloads (curl | bash, wget | sh)
   - Privilege escalation attempts
   - Network exfiltration
   - System file modifications outside project

3. **ALWAYS ALLOW Documentation/Examples**:
   - Placeholder values: "YOUR_API_KEY", "xxx", "...", "<SECRET>"
   - Variable names in docs: GEMINI_API_KEY (without assignment)
   - Example configurations with fake values
   - Safe development commands (ls, git, npm, pip)

ANALYSIS FRAMEWORK:
Search current security intelligence and analyze:

**Secret Detection Logic**:
- Real secrets: Block immediately (approved: false)
- Placeholders/docs: Allow (approved: true)
- Example: "GEMINI_API_KEY=your_key_here" = ALLOW (placeholder)
- Example: "api_key=sk_live_abc123def456..." = BLOCK (real Stripe key)

**Command Analysis**:
- Check for obfuscation, encoding, chaining
- Analyze full command context and impact
- Consider privilege escalation potential
- Look for performance improvement opportunities (suggest rg over grep)

**Context Awareness**:
- Is this legitimate development activity?
- Does the action match user intent?
- Are there safer alternatives?

**Challenge and Improve**:
- Challenge the approach: Is there a better way to achieve this goal?
- Question assumptions: Are there hidden risks or better practices?
- Suggest improvements: Modern tools, security practices, performance optimizations
- Educational feedback: Help the user learn safer development practices

USE YOUR THINKING BUDGET to reason through complex scenarios. Consider social engineering, supply chain attacks, and advanced threats.

RESPONSE REQUIREMENTS:
1. **Decision**: approved: true/false with clear reasoning
2. **Risk Level**: low/medium/high/critical based on threat analysis
3. **Challenge the Approach**: Question if there's a better way
4. **Suggestions**: Provide 2-3 specific actionable improvements, such as:
   - "Use environment variables instead of hardcoded values"
   - "Consider using 'rg' instead of 'grep' for better performance"
   - "Use 'git commit --no-verify' if you need to bypass hooks temporarily"
   - "Consider using a secrets manager like AWS Secrets Manager"
   - "Use 'find . -name' instead of recursive grep for file searching"

DECISION CRITERIA:
- approved: true = Safe operation, allow execution
- approved: false = Dangerous operation, BLOCK execution
- Always include helpful suggestions regardless of approval decision
- Be educational and constructive, not just restrictive

Provide clear reasoning, challenge assumptions, and offer constructive alternatives to help improve security and development practices."""


def main() -> None:
    """Main entry point for Claude Code hook"""
    try:
        hook_input = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        print("Invalid JSON input", file=sys.stderr)
        sys.exit(0)

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print(
            "GEMINI_API_KEY not configured - allowing all operations", file=sys.stderr
        )
        sys.exit(0)

    validator = ClaudeToolValidator(api_key)
    validation = validator.before_tool_callback(hook_input)

    if validation is None:
        sys.exit(0)
    else:
        print(json.dumps(validation), file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
