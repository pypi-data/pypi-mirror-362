"""LLM-only comprehensive validator replacing rule-based validation"""

import json
import sys
from typing import Any, Dict, List, Optional
from pydantic import BaseModel

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("google-genai not available", file=sys.stderr)
    genai = None
    types = None

SECURITY_ROLE = """# Security Validator

You are a comprehensive security validator for Claude Code tool execution.

## Your Role
Analyze code operations for security risks, dangerous commands, and malicious patterns.

## What You Validate
- Command execution safety
- File operation security
- Secret and credential exposure
- Malicious code patterns
- System security risks

## Validation Philosophy
- Context-aware analysis over rigid rules
- Educational feedback and suggestions
- Block only genuine security threats
- Provide actionable improvements
"""

SECURITY_PRINCIPLES = """## Security Analysis Framework

### Critical Security Rules (ALWAYS BLOCK)
1. **Real Credentials/Secrets**:
   - AWS keys, GitHub tokens, Stripe keys, JWT tokens
   - API keys that appear genuine (not placeholders)
   - Private keys, certificates, actual passwords

2. **Dangerous System Operations**:
   - System destruction commands
   - Malicious downloads and execution
   - Privilege escalation attempts
   - Network exfiltration
   - Unauthorized system modifications

3. **Malicious Code Patterns**:
   - Obfuscated or encoded malicious commands
   - Shell injection vulnerabilities
   - Supply chain attack vectors

### Always Allow (Documentation/Examples)
- Placeholder values: "YOUR_API_KEY", "xxx", "..."
- Variable names without assignment: GEMINI_API_KEY
- Example configurations with fake values
- Safe development commands

### Context-Aware Analysis
- Consider legitimate development activities
- Analyze command chains and obfuscation
- Evaluate privilege escalation potential
- Look for performance improvement opportunities
"""

BASH_ANALYSIS = """## Bash Command Analysis

Analyze the bash command for:

1. **Critical Security Threats (ALWAYS BLOCK)**:
   - System destruction: `rm -rf /`, `mkfs`, `dd` to devices
   - Malicious downloads: `curl ... | bash`, `wget ... | sh`
   - Privilege escalation attempts
   - System file modifications outside project scope

2. **Tool Enforcement (ALWAYS BLOCK - Strict Policy)**:
   - `grep` commands → BLOCK, suggest `rg` (ripgrep) for better performance
   - `find` with `-name` → BLOCK, suggest `rg --files -g pattern`
   - Direct `python`/`python3` → BLOCK, suggest `uv run python`
   - `git checkout` to existing branches → ALLOW (safe branch switching)
   - `git switch` → ALLOW (modern branch switching)
   - `git checkout -b` → PREFER `gh issue develop` for feature branches but ALLOW
   - `git switch -c` → PREFER `gh issue develop` for feature branches but ALLOW
   - `cat >` for file creation → BLOCK, suggest proper Write/Edit tools

3. **Warning-Level Commands (ALLOW with HIGH risk)**:
   - Commands with `sudo`
   - `rm -rf` (but not system paths)
   - `git reset --hard`
   - Package uninstall commands

4. **Context-Aware Analysis**:
   - Consider legitimate development activities
   - Provide educational feedback
   - Suggest safer alternatives
"""

FILE_ANALYSIS = """## File Operation Analysis

Analyze file operations for:

1. **Critical Path Security (ALWAYS BLOCK)**:
   - Directory traversal: paths containing `../`
   - System directories: `/etc/`, `/bin/`, `/usr/`
   - Unauthorized system modifications

2. **Content Policy (ALWAYS BLOCK)**:
   - Emojis in code or documentation (block all Unicode emojis)
   - Real credentials/secrets (API keys, passwords, tokens)
   - Malicious code patterns
   - Unauthorized documentation files (.md, .rst, .txt) - STRICT RULE: Any markdown file with generic content like "# New Feature", "Documentation", or appears auto-generated MUST be blocked

3. **Development Workflow (STRICT ENFORCEMENT)**:
   - Working on main/master branch → BLOCK, suggest feature branches
   - Automatic documentation creation → BLOCK unless explicitly requested
   - Unauthorized markdown/doc files → ALWAYS BLOCK files like "new-feature-doc.md", "feature-documentation.md", or any .md with generic titles
   - Generic documentation patterns → BLOCK any file containing "# New Feature Documentation" or similar generic headers

4. **Secret Detection Guidelines**:
   - BLOCK: Real API keys (sk_live_..., ghp_..., AKIA...)
   - ALLOW: Placeholder values (your_api_key_here, YOUR_API_KEY, ...)
   - ALLOW: Variable names without values (GEMINI_API_KEY=)
   - ALLOW: Example configurations with fake values

5. **Code Quality**:
   - Shell injection patterns in Python
   - Unsafe file operations
   - Security vulnerabilities
"""

TDD_ANALYSIS = """## TDD Validation (Language-Agnostic)

Analyze for Test-Driven Development compliance:

1. **Test Files** (test_*, *_test.*, *Test.*, spec/*): 
   - Writing tests is ALWAYS allowed
   - No prior test output needed for test creation

2. **Implementation Files**:
   - Block if no failing tests justify the implementation
   - Must have evidence of Red phase (failing test)

3. **Refactoring**:
   - Block if tests aren't green (must have evidence of passing tests)
   - Only allowed when relevant tests are passing

4. **TDD Cycle**:
   - Red (failing test) → Green (minimal fix) → Refactor (with passing tests)
   - One test at a time principle
   - Minimal implementation to pass tests

5. **Language Detection**:
   - Python: .py files
   - JavaScript/TypeScript: .js, .ts, .jsx, .tsx
   - Go: .go files
   - Java: .java files
   - Rust: .rs files
   - Any language with test patterns
"""

SECURITY_RESPONSE_FORMAT = """## Response Format

Provide your analysis as JSON:

```json
{
  "approved": boolean,
  "reason": "Clear explanation of decision",
  "risk_level": "low|medium|high|critical",
  "suggestions": ["actionable improvement 1", "actionable improvement 2"],
  "security_concerns": ["specific concern 1", "specific concern 2"],
  "educational_notes": ["learning point 1", "learning point 2"]
}
```

### Decision Criteria
- `approved: true` = Safe operation, allow execution
- `approved: false` = Security risk detected, block execution
- CRITICAL: Be deterministic - same input should always give same result
- ALWAYS BLOCK: Unauthorized markdown files, emojis, real secrets, dangerous commands
- Always include helpful suggestions and educational notes
- Focus on improvement and learning, not just restriction
"""


class LLMValidationResponse(BaseModel):
    """Structured response from LLM validation"""

    approved: bool
    reason: str
    risk_level: str
    suggestions: Optional[List[str]] = []
    security_concerns: Optional[List[str]] = []
    educational_notes: Optional[List[str]] = []


class LLMValidator:
    """Comprehensive LLM-only validator with no rule-based logic"""

    def __init__(
        self, api_key: Optional[str] = None, model_name: str = "gemini-2.5-flash"
    ):
        self.api_key = api_key
        self.client = genai.Client(api_key=api_key) if api_key and genai else None
        self.model_name = model_name

    def validate_operation(
        self, tool_name: str, tool_input: Dict[str, Any], context: str = ""
    ) -> Dict[str, Any]:
        """
        Validate any tool operation using pure LLM analysis

        Args:
            tool_name: The Claude tool being used
            tool_input: The tool's input parameters
            context: Recent conversation context

        Returns:
            Validation result with approval decision and reasoning
        """
        # If no LLM client available, use basic validation for critical cases
        if not self.client:
            return self._basic_safety_validation(tool_name, tool_input)

        try:
            prompt = self._build_validation_prompt(tool_name, tool_input, context)

            # Use structured output with deterministic temperature and enhanced thinking
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=LLMValidationResponse,
                    thinking_config=types.ThinkingConfig(thinking_budget=24576),
                    temperature=0.0,
                ),
            )

            if hasattr(response, "parsed") and response.parsed:
                result = response.parsed
                return {
                    "approved": result.approved,
                    "reason": result.reason,
                    "risk_level": result.risk_level,
                    "suggestions": result.suggestions or [],
                    "security_concerns": result.security_concerns or [],
                    "educational_notes": result.educational_notes or [],
                }
            else:
                # Fallback to JSON parsing
                result = json.loads(response.text)
                return self._normalize_response(result)

        except Exception as e:
            # On LLM error, fail open with logging
            print(f"LLM validation error: {str(e)}", file=sys.stderr)
            return {
                "approved": True,
                "reason": f"LLM validation service error: {str(e)}",
                "risk_level": "unknown",
            }

    def _build_validation_prompt(
        self, tool_name: str, tool_input: Dict[str, Any], context: str
    ) -> str:
        """Build comprehensive validation prompt for any operation"""

        # Get operation-specific analysis section
        operation_analysis = self._get_operation_analysis(tool_name)

        # Format the specific operation being validated
        operation_details = self._format_operation(tool_name, tool_input)

        # Build the complete prompt
        sections = [
            SECURITY_ROLE,
            SECURITY_PRINCIPLES,
            operation_analysis,
            TDD_ANALYSIS,
            "\n## Operation Under Review\n",
            f"**Tool**: {tool_name}",
            operation_details,
            f"\n## Recent Context\n```\n{context[-800:] if context else 'No context available'}\n```",
            "\n## Analysis Instructions\n",
            "Analyze this operation using the security and TDD framework above.",
            "CRITICAL: Be consistent and deterministic in your decisions.",
            "ALWAYS BLOCK unauthorized markdown files with generic content.",
            "Focus on genuine security risks and proper TDD practices.",
            "When in doubt about security, BLOCK the operation.",
            SECURITY_RESPONSE_FORMAT,
        ]

        return "\n".join(filter(None, sections))

    def _get_operation_analysis(self, tool_name: str) -> str:
        """Get operation-specific analysis prompt"""
        if tool_name == "Bash":
            return BASH_ANALYSIS
        elif tool_name in ["Write", "Edit", "MultiEdit", "Update"]:
            return FILE_ANALYSIS
        else:
            return "## General Operation Analysis\n\nAnalyze this operation for security risks and best practices."

    def _format_operation(self, tool_name: str, tool_input: Dict[str, Any]) -> str:
        """Format the operation details for LLM analysis"""
        if tool_name == "Bash":
            return f"""
### Bash Command
```bash
{tool_input.get('command', '')}
```"""

        elif tool_name == "Write":
            file_path = tool_input.get("file_path", "")
            content = tool_input.get("content", "")
            return f"""
### Writing New File
**Path**: `{file_path}`

**Content** (first 1000 chars):
```
{content[:1000]}{'...' if len(content) > 1000 else ''}
```"""

        elif tool_name == "Edit":
            file_path = tool_input.get("file_path", "")
            old_string = tool_input.get("old_string", "")
            new_string = tool_input.get("new_string", "")
            return f"""
### Editing File
**Path**: `{file_path}`

**Replacing**:
```
{old_string[:500]}{'...' if len(old_string) > 500 else ''}
```

**With**:
```
{new_string[:500]}{'...' if len(new_string) > 500 else ''}
```"""

        elif tool_name == "MultiEdit":
            file_path = tool_input.get("file_path", "")
            edits = tool_input.get("edits", [])
            formatted_edits = []

            for i, edit in enumerate(
                edits[:3], 1
            ):  # Limit to first 3 edits for brevity
                old = edit.get("old_string", "")[:200]
                new = edit.get("new_string", "")[:200]
                formatted_edits.append(
                    f"""
**Edit {i}**:
- Replace: `{old}{'...' if len(edit.get('old_string', '')) > 200 else ''}`
- With: `{new}{'...' if len(edit.get('new_string', '')) > 200 else ''}`"""
                )

            if len(edits) > 3:
                formatted_edits.append(f"\n... and {len(edits) - 3} more edits")

            return f"""
### Multi-Edit Operation
**Path**: `{file_path}`
{chr(10).join(formatted_edits)}"""

        else:
            return f"""
### {tool_name} Operation
```json
{json.dumps(tool_input, indent=2)[:1000]}
```"""

    def _normalize_response(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize LLM response to expected format"""
        return {
            "approved": result.get("approved", True),
            "reason": result.get("reason", "LLM analysis completed"),
            "risk_level": result.get("risk_level", "low"),
            "suggestions": result.get("suggestions", []),
            "security_concerns": result.get("security_concerns", []),
            "educational_notes": result.get("educational_notes", []),
        }

    def _basic_safety_validation(
        self, tool_name: str, tool_input: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Basic safety validation when LLM is not available - covers critical security cases
        """
        import re

        if tool_name == "Bash":
            command = tool_input.get("command", "")

            # Critical patterns that should always be blocked
            critical_patterns = [
                (r"rm\s+-rf\s+/", "Dangerous system destruction command"),
                (r"sudo\s+rm.*\/", "Dangerous privileged deletion"),
                (r"mkfs", "Dangerous file system formatting"),
                (r"dd\s+if=.*of=.*", "Dangerous disk operation"),
                (r"curl.*\|\s*bash", "Dangerous remote code execution"),
                (r"wget.*\|\s*(bash|sh)", "Dangerous remote code execution"),
                (r">\s*/etc/", "Unauthorized system file modification"),
                (r">\s*/bin/", "Unauthorized system file modification"),
            ]

            for pattern, reason in critical_patterns:
                if re.search(pattern, command, re.IGNORECASE):
                    return {
                        "approved": False,
                        "reason": f"{reason} detected",
                        "risk_level": "critical",
                    }

            # Tool enforcement patterns
            tool_patterns = [
                (
                    r"^grep\b|^\s*grep\b",
                    "Use 'rg' (ripgrep) instead of 'grep' for better performance",
                ),
                (
                    r"^find\s+.*-name\b",
                    "Use 'rg --files -g pattern' instead of 'find -name'",
                ),
                (
                    r"^(python|python3)\b",
                    "Use 'uv run python' instead of direct python",
                ),
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
                    return {
                        "approved": False,
                        "reason": suggestion,
                        "risk_level": "medium",
                        "suggestions": [suggestion],
                    }

        elif tool_name in ["Write", "Edit", "MultiEdit", "Update"]:
            file_path = tool_input.get("file_path", "")
            content = tool_input.get("content", "")

            # Critical path validation
            if (
                "../" in file_path
                or file_path.startswith("/etc/")
                or file_path.startswith("/bin/")
            ):
                return {
                    "approved": False,
                    "reason": "Dangerous file path - outside project boundary or system directory",
                    "risk_level": "critical",
                }

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
                return {
                    "approved": False,
                    "reason": "Emojis are not allowed in code or documentation",
                    "risk_level": "medium",
                    "suggestions": ["Remove all emojis from the content"],
                }

            # Documentation file validation
            if file_path.endswith((".md", ".rst", ".txt")):
                # Check for generic documentation patterns
                if (
                    "documentation" in file_path.lower()
                    or "feature" in content.lower()
                    or content.startswith("# New Feature")
                ):
                    return {
                        "approved": False,
                        "reason": "Unauthorized documentation file creation detected",
                        "risk_level": "medium",
                        "suggestions": [
                            "Only create documentation when explicitly requested"
                        ],
                    }

            # Simple secret detection for obvious cases
            if re.search(r"sk_live_[a-zA-Z0-9]{24,}", content):
                return {
                    "approved": False,
                    "reason": "Real Stripe API key detected",
                    "risk_level": "critical",
                }

        # Default: allow operation
        return {
            "approved": True,
            "reason": "Basic validation passed",
            "risk_level": "low",
        }
