"""
Validation check helpers for LogicPwn response validation.
"""
from typing import List, Dict, Any, Tuple, Optional
import re
import requests

def _check_regex_patterns(response_text: str, patterns: List[str]) -> Tuple[bool, List[str], Dict[str, Any]]:
    """Check if response matches regex patterns.
    This function performs regex pattern matching against response content
    and extracts matching groups for data extraction.
    Args:
        response_text: Response text to check
        patterns: List of regex patterns to match
    Returns:
        Tuple of (has_matches, matched_patterns, extracted_data)
    """
    if not patterns:
        return False, [], {}
    matched_patterns = []
    extracted_data = {}
    group_counter = 1
    for pattern in patterns:
        try:
            matches = list(re.finditer(pattern, response_text, re.IGNORECASE | re.MULTILINE))
            if matches:
                matched_patterns.append(pattern)
                match = matches[0]
                # Extract named groups if present
                if match.groupdict():
                    extracted_data.update(match.groupdict())
                else:
                    # Extract all groups
                    for i, group in enumerate(match.groups(), 1):
                        extracted_data[f"group_{group_counter}"] = group
                        group_counter += 1
        except re.error:
            continue
    return bool(matched_patterns), matched_patterns, extracted_data

def _check_status_codes(response: requests.Response, status_codes: List[int]) -> bool:
    """Check if response status code is in the list of acceptable codes."""
    if not status_codes:
        return True
    return response.status_code in status_codes

def _check_headers_criteria(response: requests.Response, headers_criteria: Dict[str, str]) -> Tuple[bool, List[str]]:
    """Check if all response headers match required criteria.
    Returns (True, list of matched header keys) if all criteria are matched.
    Returns (False, []) if any are missing or do not match.
    """
    if not headers_criteria:
        return True, []
    matched = []
    for key, value in headers_criteria.items():
        if key in response.headers and value.lower() in response.headers[key].lower():
            matched.append(key)
        else:
            return False, []  # As soon as one does not match, fail
    return True, matched

def _calculate_confidence_score(
    success_matches: List[str],
    failure_matches: List[str],
    regex_matches: List[str],
    status_match: bool,
    headers_match: bool
) -> float:
    """Calculate confidence score for validation result."""
    score = 0.0
    if success_matches:
        score += 0.3
    if regex_matches:
        score += 0.3
    if status_match:
        score += 0.2
    if headers_match:
        score += 0.1
    if failure_matches:
        score -= 0.5
    return max(0.0, min(1.0, score)) 