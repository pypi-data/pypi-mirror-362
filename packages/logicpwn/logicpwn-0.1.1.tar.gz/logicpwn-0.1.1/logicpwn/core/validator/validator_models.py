"""
Validation data models and enums for LogicPwn response validation.
"""
from typing import Dict, Optional, List, Any, Union
from dataclasses import dataclass, field
from enum import Enum
from pydantic import BaseModel, Field, field_validator

class ValidationType(Enum):
    """Types of validation criteria."""
    SUCCESS_CRITERIA = "success_criteria"
    FAILURE_CRITERIA = "failure_criteria"
    REGEX_PATTERN = "regex_pattern"
    STATUS_CODE = "status_code"
    HEADER_CRITERIA = "header_criteria"
    JSON_PATH = "json_path"

@dataclass
class ValidationResult:
    """Structured result from response validation.
    This dataclass provides a comprehensive validation result including
    the validation outcome, matched patterns, extracted data, and
    confidence scoring for exploit chaining workflows.
    """
    is_valid: bool = False
    matched_patterns: List[str] = field(default_factory=list)
    extracted_data: Dict[str, Any] = field(default_factory=dict)
    confidence_score: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    validation_type: Optional[ValidationType] = None
    error_message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert validation result to dictionary."""
        return {
            "is_valid": self.is_valid,
            "matched_patterns": self.matched_patterns,
            "extracted_data": self.extracted_data,
            "confidence_score": self.confidence_score,
            "metadata": self.metadata,
            "validation_type": self.validation_type.value if self.validation_type else None,
            "error_message": self.error_message
        }

    def __str__(self) -> str:
        return f"ValidationResult(valid={self.is_valid}, confidence={self.confidence_score:.2f})"

class ValidationConfig(BaseModel):
    """Configuration model for response validation.
    This model validates and stores validation configuration parameters
    including success/failure criteria, regex patterns, and other
    validation settings for exploit chaining workflows.
    """
    success_criteria: List[str] = Field(default_factory=list, description="Text indicators of successful validation")
    failure_criteria: List[str] = Field(default_factory=list, description="Text indicators of failed validation")
    regex_patterns: List[str] = Field(default_factory=list, description="Regex patterns to match against response content")
    status_codes: List[int] = Field(default_factory=list, description="Acceptable HTTP status codes")
    headers_criteria: Dict[str, str] = Field(default_factory=dict, description="Required headers and their values")
    json_paths: List[str] = Field(default_factory=list, description="JSON path expressions for JSON responses")
    return_structured: bool = Field(default=False, description="Return ValidationResult object instead of boolean")
    confidence_threshold: float = Field(default=0.3, ge=0.0, le=1.0, description="Minimum confidence score for validation")

    @field_validator('regex_patterns')
    @classmethod
    def validate_regex_patterns(cls, v: List[str]) -> List[str]:
        """Validate regex patterns are compilable."""
        import re
        for pattern in v:
            try:
                re.compile(pattern)
            except re.error as e:
                raise ValueError(f"Invalid regex pattern '{pattern}': {e}")
        return v

    @field_validator('status_codes')
    @classmethod
    def validate_status_codes(cls, v: List[int]) -> List[int]:
        """Validate HTTP status codes are in valid range."""
        for code in v:
            if not (100 <= code <= 599):
                raise ValueError(f"Invalid HTTP status code: {code}")
        return v 