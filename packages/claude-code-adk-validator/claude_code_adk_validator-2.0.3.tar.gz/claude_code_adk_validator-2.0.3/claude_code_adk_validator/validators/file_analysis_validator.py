"""File analysis validator for large file security scanning."""

import tempfile
import os
from typing import Dict, Any, Optional, List, cast
from ..hook_response import HookResponse, ResponseBuilder, RiskLevel, ValidationStage

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None


class FileAnalysisValidator:
    """Enhanced file analysis using Gemini Files API for large files."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.client = genai.Client(api_key=api_key) if api_key and genai else None
        self.uploaded_files: List[Dict[str, str]] = []

    def should_analyze_file(self, content: str, file_path: str) -> bool:
        """Determine if file needs enhanced analysis."""
        # Analyze files larger than 500 chars or sensitive file types
        return (
            len(content) > 500
            or file_path.endswith(
                (".env", ".key", ".pem", ".p12", ".pfx", ".json", ".yaml", ".yml")
            )
            or "secret" in file_path.lower()
            or "config" in file_path.lower()
        )

    def upload_file_for_analysis(self, file_path: str, content: str) -> Optional[str]:
        """Upload file content to Gemini for enhanced analysis."""
        if not self.client:
            return None

        try:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=os.path.splitext(file_path)[1], delete=False
            ) as temp_file:
                temp_file.write(content)
                temp_file_path = temp_file.name

            uploaded_file = self.client.files.upload(path=temp_file_path)
            self.uploaded_files.append(
                {"file_id": uploaded_file.name, "temp_path": temp_file_path}
            )

            return str(uploaded_file.name)

        except Exception:
            return None

    def analyze_uploaded_file(
        self, file_id: str, file_path: str
    ) -> Optional[Dict[str, Any]]:
        """Perform enhanced security analysis using uploaded file."""
        if not self.client:
            return None

        try:
            prompt = f"""Analyze {os.path.basename(file_path)} for security issues, code quality, and potential vulnerabilities.

Focus on:
1. Credential leaks (API keys, passwords, tokens, certificates)
2. Unsafe operations and malicious patterns
3. Configuration security issues
4. Code quality concerns
5. Potential vulnerabilities

Provide analysis in JSON format:
{{
    "security_issues": ["list of specific security issues found"],
    "code_quality_concerns": ["list of code quality issues"],
    "risk_assessment": "low|medium|high|critical",
    "recommendations": ["list of actionable recommendations"]
}}"""

            uploaded_file = self.client.files.get(file_id)
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[prompt, uploaded_file],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json", temperature=0.1
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
                import json

                return cast(Dict[str, Any], json.loads(response.text))

        except Exception:
            return None

    def cleanup_uploaded_files(self) -> None:
        """Clean up uploaded files and temporary files."""
        for file_info in self.uploaded_files:
            try:
                # Delete from Gemini
                if self.client:
                    self.client.files.delete(file_info["file_id"])
                # Delete temp file
                os.unlink(file_info["temp_path"])
            except Exception:
                pass
        self.uploaded_files = []

    def validate_operation(
        self, tool_name: str, tool_input: Dict[str, Any], context: str = ""
    ) -> HookResponse:
        """Validate file operations with enhanced analysis for large files."""

        if tool_name not in ["Write", "Edit", "MultiEdit", "Update"]:
            return ResponseBuilder.approve(
                reason="Tool not applicable for file analysis",
                risk_level=RiskLevel.LOW,
                validation_stage=ValidationStage.FILE_ANALYSIS,
                tool_name=tool_name,
            )

        file_path = tool_input.get("file_path", "")
        content = tool_input.get("content", "")

        if not content or not self.should_analyze_file(content, file_path):
            return ResponseBuilder.approve(
                reason="File does not require enhanced analysis",
                risk_level=RiskLevel.LOW,
                validation_stage=ValidationStage.FILE_ANALYSIS,
                tool_name=tool_name,
            )

        if not self.client:
            return ResponseBuilder.approve(
                reason="File analysis requires Gemini API - skipping enhanced analysis",
                risk_level=RiskLevel.LOW,
                suggestions=["Set GEMINI_API_KEY for enhanced file analysis"],
                validation_stage=ValidationStage.FILE_ANALYSIS,
                tool_name=tool_name,
            )

        try:
            # Upload and analyze file
            file_id = self.upload_file_for_analysis(file_path, content)
            if not file_id:
                return ResponseBuilder.approve(
                    reason="File upload failed - allowing operation",
                    risk_level=RiskLevel.LOW,
                    validation_stage=ValidationStage.FILE_ANALYSIS,
                    tool_name=tool_name,
                )

            analysis = self.analyze_uploaded_file(file_id, file_path)
            if not analysis:
                return ResponseBuilder.approve(
                    reason="File analysis failed - allowing operation",
                    risk_level=RiskLevel.LOW,
                    validation_stage=ValidationStage.FILE_ANALYSIS,
                    tool_name=tool_name,
                )

            # Process analysis results
            security_issues = analysis.get("security_issues", [])
            code_quality_concerns = analysis.get("code_quality_concerns", [])
            risk_assessment = analysis.get("risk_assessment", "low")
            recommendations = analysis.get("recommendations", [])

            # Map risk assessment to RiskLevel
            risk_level_map = {
                "low": RiskLevel.LOW,
                "medium": RiskLevel.MEDIUM,
                "high": RiskLevel.HIGH,
                "critical": RiskLevel.CRITICAL,
            }
            risk_level = risk_level_map.get(risk_assessment, RiskLevel.LOW)

            if security_issues:
                return ResponseBuilder.block(
                    reason=f"File analysis detected security issues: {', '.join(security_issues[:3])}",
                    risk_level=risk_level,
                    security_concerns=security_issues,
                    suggestions=recommendations,
                    educational_notes=[
                        "Enhanced file analysis using Gemini AI",
                        "Large files and sensitive file types require thorough review",
                    ],
                    validation_stage=ValidationStage.FILE_ANALYSIS,
                    tool_name=tool_name,
                    detected_patterns=["ai_detected_security_issues"],
                )

            if code_quality_concerns and risk_level in [
                RiskLevel.HIGH,
                RiskLevel.CRITICAL,
            ]:
                return ResponseBuilder.warn(
                    reason=f"File analysis found code quality concerns: {', '.join(code_quality_concerns[:2])}",
                    risk_level=risk_level,
                    suggestions=recommendations,
                    educational_notes=["AI-powered code quality analysis"],
                    validation_stage=ValidationStage.FILE_ANALYSIS,
                    tool_name=tool_name,
                )

            return ResponseBuilder.approve(
                reason="File passed enhanced security analysis",
                risk_level=risk_level,
                suggestions=recommendations if recommendations else [],
                educational_notes=[
                    "File analyzed using Gemini AI for security and quality"
                ],
                validation_stage=ValidationStage.FILE_ANALYSIS,
                tool_name=tool_name,
            )

        finally:
            self.cleanup_uploaded_files()

    def __del__(self) -> None:
        """Cleanup on destruction."""
        self.cleanup_uploaded_files()
