import json
import sys
import os
import tempfile
from typing import Optional, List

try:
    from google import genai
    from google.genai import types
    from pydantic import BaseModel
except ImportError:
    print("google-genai or pydantic not installed", file=sys.stderr)
    sys.exit(0)

try:
    from .llm_validator import LLMValidator
except ImportError:
    pass


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
        self.model_name = "gemini-2.5-flash"
        self.decision_history: List[dict] = []
        self.uploaded_files: List[dict] = []

        try:
            self.llm_validator: Optional["LLMValidator"] = LLMValidator(
                api_key=api_key, model_name=self.model_name
            )
        except Exception:
            self.llm_validator = None

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
            prompt = f"Analyze {os.path.basename(file_path)} for security issues, code quality, and potential vulnerabilities. Focus on credential leaks, unsafe operations, and malicious patterns."

            uploaded_file = self.client.files.get(file_id)
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[prompt, uploaded_file],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=FileAnalysisResponse,
                    thinking_config=types.ThinkingConfig(thinking_budget=24576),
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
        """Main validation logic using pure LLM analysis"""

        # Use LLM validator for all validation - no rule-based checks
        if self.llm_validator:
            llm_result = self.llm_validator.validate_operation(
                tool_name, tool_input, context
            )
            if not llm_result["approved"]:
                return llm_result

        # TDD validation is now handled by the main LLM validator

        # Skip further LLM-dependent analysis if no API key
        if not self.api_key:
            return {
                "approved": True,
                "risk_level": "unknown",
                "reason": "No API key - allowing operation",
            }

        # Enhanced file analysis for large files (keeping this as additional security layer)
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

        # If we reach here, all LLM validations passed - allow the operation
        return {
            "approved": True,
            "risk_level": "low",
            "reason": "All validations passed",
        }

    # TDD validation is now integrated into the main LLM validator


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
