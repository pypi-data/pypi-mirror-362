"""Advanced Claude Code hook response models and formatting."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from enum import Enum


class DecisionType(str, Enum):
    """Hook decision types for Claude Code."""

    APPROVE = "approve"
    BLOCK = "block"


class RiskLevel(str, Enum):
    """Security risk levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ValidationStage(str, Enum):
    """Validation pipeline stages."""

    SECURITY = "security"
    TDD = "tdd"
    FILE_ANALYSIS = "file_analysis"
    TOOL_ENFORCEMENT = "tool_enforcement"


class HookResponseMetadata(BaseModel):
    """Metadata for hook responses with educational information."""

    risk_level: RiskLevel
    suggestions: List[str] = Field(default_factory=list)
    security_concerns: List[str] = Field(default_factory=list)
    educational_notes: List[str] = Field(default_factory=list)
    validation_stage: Optional[ValidationStage] = None
    tool_name: Optional[str] = None
    detected_patterns: List[str] = Field(default_factory=list)


class HookResponse(BaseModel):
    """Advanced Claude Code hook response with full schema support."""

    # Core Claude Code hook response fields
    continue_processing: bool = Field(default=True, alias="continue")
    decision: DecisionType = DecisionType.APPROVE
    reason: str = ""
    stop_reason: Optional[str] = None
    suppress_output: bool = Field(default=False, alias="suppressOutput")

    # Extended metadata for educational feedback
    metadata: HookResponseMetadata

    class Config:
        populate_by_name = True

    def to_claude_json(self) -> Dict[str, Any]:
        """Convert to Claude Code-compatible JSON format."""
        result: Dict[str, Any] = {
            "continue": self.continue_processing,
            "decision": self.decision.value,
            "reason": self.reason,
            "suppressOutput": self.suppress_output,
        }

        if self.stop_reason:
            result["stopReason"] = self.stop_reason

        # Add metadata for debugging and educational purposes
        result["metadata"] = {
            "risk_level": self.metadata.risk_level.value,
            "suggestions": self.metadata.suggestions,
            "security_concerns": self.metadata.security_concerns,
            "educational_notes": self.metadata.educational_notes,
            "validation_stage": (
                self.metadata.validation_stage.value
                if self.metadata.validation_stage
                else None
            ),
            "tool_name": self.metadata.tool_name,
            "detected_patterns": self.metadata.detected_patterns,
        }

        return result

    def get_exit_code(self) -> int:
        """Get appropriate exit code for Claude Code hooks."""
        if self.decision == DecisionType.BLOCK:
            return 2  # Block execution
        else:
            return 0  # Approve or default allows execution

    def format_for_stderr(self) -> str:
        """Format comprehensive response for stderr output including all educational content."""
        lines = [self.reason]

        # Add suggestions if available
        if self.metadata.suggestions:
            lines.append("")
            lines.append("SUGGESTIONS:")
            for suggestion in self.metadata.suggestions:
                lines.append(f"• {suggestion}")

        # Add educational notes if available
        if self.metadata.educational_notes:
            lines.append("")
            lines.append("EDUCATIONAL NOTES:")
            for note in self.metadata.educational_notes:
                if note:  # Skip empty lines
                    lines.append(f"• {note}")
                else:
                    lines.append("")  # Preserve empty lines for formatting

        # Add security concerns if available
        if self.metadata.security_concerns:
            lines.append("")
            lines.append("SECURITY CONCERNS:")
            for concern in self.metadata.security_concerns:
                lines.append(f"• {concern}")

        # Add validation stage and tool info
        if self.metadata.validation_stage:
            lines.append("")
            lines.append(f"VALIDATION STAGE: {self.metadata.validation_stage.value}")

        if self.metadata.tool_name:
            lines.append(f"TOOL: {self.metadata.tool_name}")

        # Add detected patterns if available
        if self.metadata.detected_patterns:
            lines.append("")
            lines.append("DETECTED PATTERNS:")
            for pattern in self.metadata.detected_patterns:
                lines.append(f"• {pattern}")

        return "\n".join(lines)


class ResponseBuilder:
    """Builder class for creating structured hook responses."""

    @staticmethod
    def approve(
        reason: str = "Operation approved",
        risk_level: RiskLevel = RiskLevel.LOW,
        suggestions: Optional[List[str]] = None,
        educational_notes: Optional[List[str]] = None,
        validation_stage: Optional[ValidationStage] = None,
        tool_name: Optional[str] = None,
    ) -> HookResponse:
        """Create an approval response."""
        return HookResponse(
            continue_processing=True,
            decision=DecisionType.APPROVE,
            reason=reason,
            metadata=HookResponseMetadata(
                risk_level=risk_level,
                suggestions=suggestions or [],
                educational_notes=educational_notes or [],
                validation_stage=validation_stage,
                tool_name=tool_name,
            ),
        )

    @staticmethod
    def warn(
        reason: str,
        risk_level: RiskLevel = RiskLevel.MEDIUM,
        suggestions: Optional[List[str]] = None,
        security_concerns: Optional[List[str]] = None,
        educational_notes: Optional[List[str]] = None,
        validation_stage: Optional[ValidationStage] = None,
        tool_name: Optional[str] = None,
        detected_patterns: Optional[List[str]] = None,
    ) -> HookResponse:
        """Create a warning response (allows execution with educational feedback)."""
        # Warnings are implemented as approvals with educational content
        # since Claude Code only supports approve/block decisions
        return HookResponse(
            continue_processing=True,
            decision=DecisionType.APPROVE,
            reason=f"{reason} (with recommendations)",
            metadata=HookResponseMetadata(
                risk_level=risk_level,
                suggestions=suggestions or [],
                security_concerns=security_concerns or [],
                educational_notes=educational_notes or [],
                validation_stage=validation_stage,
                tool_name=tool_name,
                detected_patterns=detected_patterns or [],
            ),
        )

    @staticmethod
    def block(
        reason: str,
        risk_level: RiskLevel = RiskLevel.HIGH,
        suggestions: Optional[List[str]] = None,
        security_concerns: Optional[List[str]] = None,
        educational_notes: Optional[List[str]] = None,
        validation_stage: Optional[ValidationStage] = None,
        tool_name: Optional[str] = None,
        detected_patterns: Optional[List[str]] = None,
        stop_reason: Optional[str] = None,
    ) -> HookResponse:
        """Create a blocking response."""
        return HookResponse(
            continue_processing=False,
            decision=DecisionType.BLOCK,
            reason=reason,
            stop_reason=stop_reason or reason,
            metadata=HookResponseMetadata(
                risk_level=risk_level,
                suggestions=suggestions or [],
                security_concerns=security_concerns or [],
                educational_notes=educational_notes or [],
                validation_stage=validation_stage,
                tool_name=tool_name,
                detected_patterns=detected_patterns or [],
            ),
        )

    @staticmethod
    def from_legacy_response(
        legacy_response: Dict[str, Any], tool_name: str
    ) -> HookResponse:
        """Convert legacy response format to new HookResponse."""
        approved = legacy_response.get("approved", True)
        reason = legacy_response.get("reason", "")
        risk_level_str = legacy_response.get("risk_level", "low")

        # Map string risk level to enum
        risk_level = RiskLevel.LOW
        if risk_level_str == "medium":
            risk_level = RiskLevel.MEDIUM
        elif risk_level_str == "high":
            risk_level = RiskLevel.HIGH
        elif risk_level_str == "critical":
            risk_level = RiskLevel.CRITICAL

        suggestions = legacy_response.get("suggestions", [])
        security_concerns = legacy_response.get("security_concerns", [])
        educational_notes = legacy_response.get("educational_notes", [])

        if approved:
            return ResponseBuilder.approve(
                reason=reason,
                risk_level=risk_level,
                suggestions=suggestions,
                educational_notes=educational_notes,
                tool_name=tool_name,
            )
        else:
            # Determine if this should be a warning or block based on risk level
            if risk_level in [RiskLevel.CRITICAL, RiskLevel.HIGH]:
                return ResponseBuilder.block(
                    reason=reason,
                    risk_level=risk_level,
                    suggestions=suggestions,
                    security_concerns=security_concerns,
                    educational_notes=educational_notes,
                    tool_name=tool_name,
                )
            else:
                return ResponseBuilder.warn(
                    reason=reason,
                    risk_level=risk_level,
                    suggestions=suggestions,
                    security_concerns=security_concerns,
                    educational_notes=educational_notes,
                    tool_name=tool_name,
                )
