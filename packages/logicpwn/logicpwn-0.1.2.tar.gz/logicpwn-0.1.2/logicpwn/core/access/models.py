from typing import List, Union, Optional, Dict, Any
from dataclasses import dataclass, field
import datetime
import requests

@dataclass
class AccessTestResult:
    """
    Result of a single access control/IDOR test.
    """
    id_tested: Union[str, int]
    endpoint_url: str
    status_code: int
    access_granted: bool
    vulnerability_detected: bool
    response_indicators: List[str] = field(default_factory=list)
    error_message: Optional[str] = None
    expected_access: Optional[bool] = None
    # Audit/log fields
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.utcnow)
    request_method: str = "GET"
    request_data: Optional[Dict[str, Any]] = None
    response_body: Optional[str] = None
    baseline_results: Optional[List[Dict[str, Any]]] = None  # Info from baseline sessions
    decision_log: Optional[str] = None  # Human-readable explanation

@dataclass
class AccessDetectorConfig:
    """
    Configuration for the access/IDOR detector.
    """
    max_concurrent_requests: int = 10
    request_timeout: int = 30
    retry_attempts: int = 3
    compare_unauthenticated: bool = True
    current_user_id: Optional[Union[str, int]] = None
    authorized_ids: Optional[List[Union[str, int]]] = None
    unauthorized_ids: Optional[List[Union[str, int]]] = None
    rate_limit: Optional[float] = None  # seconds between requests
    # New: allow custom HTTP method and request data per test
    method: str = "GET"
    request_data_map: Optional[Dict[Union[str, int], Dict[str, Any]]] = None  # Per-ID request data
    # New: support multiple baseline sessions (e.g., guest, user, admin)
    baseline_sessions: Optional[List[requests.Session]] = None
    baseline_names: Optional[List[str]] = None  # Names for each baseline session 