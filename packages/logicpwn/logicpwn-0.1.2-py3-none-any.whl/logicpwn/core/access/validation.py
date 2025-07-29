from typing import List, Union
from urllib.parse import urlparse
import re

def _validate_endpoint_template(template: str) -> None:
    """
    Validate that the endpoint template is a valid HTTP/HTTPS URL with an {id} placeholder.
    """
    try:
        parsed = urlparse(template.format(id='test'))
        if parsed.scheme not in ['http', 'https']:
            raise ValueError("Only HTTP/HTTPS schemes allowed in endpoint_template")
    except Exception:
        raise ValueError("Invalid endpoint_template or URL format")

def _validate_inputs(endpoint_template: str, test_ids: List[Union[str, int]], success_indicators: List[str], failure_indicators: List[str]):
    """
    Validate all required inputs for the access detector.
    """
    _validate_endpoint_template(endpoint_template)
    if not endpoint_template or '{id}' not in endpoint_template:
        raise ValueError("endpoint_template must contain '{id}' placeholder")
    if not test_ids:
        raise ValueError("test_ids cannot be empty")
    if not success_indicators:
        raise ValueError("success_indicators cannot be empty")
    if not failure_indicators:
        raise ValueError("failure_indicators cannot be empty")

def _sanitize_test_id(test_id: Union[str, int]) -> Union[str, int]:
    """
    Sanitize the test ID to remove unsafe characters.
    """
    if isinstance(test_id, str):
        return re.sub(r'[^a-zA-Z0-9_-]', '', test_id)
    return test_id 