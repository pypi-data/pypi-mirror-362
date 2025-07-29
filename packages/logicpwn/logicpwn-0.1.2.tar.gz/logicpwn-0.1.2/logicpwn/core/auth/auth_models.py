"""
Authentication models for LogicPwn.
"""
from typing import Dict, Optional, List
from pydantic import BaseModel, Field, field_validator
from urllib.parse import urlparse

HTTP_METHODS = {"GET", "POST"}

class AuthConfig(BaseModel):
    """Authentication configuration model for exploit chaining workflows."""
    url: str = Field(..., description="Login endpoint URL")
    method: str = Field(default="POST", description="HTTP method for login")
    credentials: Dict[str, str] = Field(..., description="Login credentials")
    success_indicators: List[str] = Field(default_factory=list, description="Text indicators of successful login")
    failure_indicators: List[str] = Field(default_factory=list, description="Text indicators of failed login")
    headers: Optional[Dict[str, str]] = Field(default=None, description="Additional HTTP headers")
    timeout: int = Field(default=30, ge=1, le=300, description="Request timeout in seconds")
    verify_ssl: bool = Field(default=True, description="Whether to verify SSL certificates")

    @field_validator('url')
    @classmethod
    def validate_url(cls, v: str) -> str:
        parsed = urlparse(v)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError('Invalid URL format - must include scheme and netloc')
        return v

    @field_validator('credentials')
    @classmethod
    def validate_credentials(cls, v: Dict[str, str]) -> Dict[str, str]:
        if not v:
            raise ValueError('Credentials cannot be empty')
        return v

    @field_validator('method')
    @classmethod
    def validate_method(cls, v: str) -> str:
        v_up = v.upper()
        if v_up not in HTTP_METHODS:
            raise ValueError(f'method must be one of {HTTP_METHODS}')
        return v_up 