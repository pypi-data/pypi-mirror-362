"""
Main API functions for LogicPwn response validation.
"""
from typing import Dict, Optional, List, Any, Union
import requests
from .validator_models import ValidationResult, ValidationConfig, ValidationType
from .validator_checks import (
    _check_regex_patterns,
    _check_status_codes,
    _check_headers_criteria,
    _calculate_confidence_score
)
from .validator_patterns import VulnerabilityPatterns
from .validator_utils import _sanitize_response_text
from logicpwn.core.performance import monitor_performance, performance_context
from logicpwn.core.config.config_utils import get_max_log_body_size, get_redaction_string
from logicpwn.core.utils import check_indicators, validate_config
import re
import json
from logicpwn.exceptions import ValidationError

@monitor_performance("response_validation")
def validate_response(
    response: requests.Response,
    success_criteria: Optional[List[str]] = None,
    failure_criteria: Optional[List[str]] = None,
    regex_patterns: Optional[List[str]] = None,
    status_codes: Optional[List[int]] = None,
    headers_criteria: Optional[Dict[str, str]] = None,
    json_paths: Optional[List[str]] = None,
    return_structured: bool = False,
    confidence_threshold: float = 0.3
) -> Union[bool, ValidationResult]:
    try:
        config_dict = {
            "success_criteria": success_criteria or [],
            "failure_criteria": failure_criteria or [],
            "regex_patterns": regex_patterns or [],
            "status_codes": status_codes or [],
            "headers_criteria": headers_criteria or {},
            "json_paths": json_paths or [],
            "return_structured": return_structured,
            "confidence_threshold": confidence_threshold
        }
        config = validate_config(config_dict, ValidationConfig)
        try:
            response_text = response.text
        except Exception as e:
            response_text = ""
        safe_text = _sanitize_response_text(response_text)
        success_match, success_matches = check_indicators(response_text, config.success_criteria, "success")
        failure_match, failure_matches = check_indicators(response_text, config.failure_criteria, "failure")
        regex_match, regex_matches, extracted_data = _check_regex_patterns(response_text, config.regex_patterns)
        status_match = _check_status_codes(response, config.status_codes)
        headers_match, header_matches = _check_headers_criteria(response, config.headers_criteria)
        is_valid = (
            (not config.success_criteria or success_match) and
            (not config.failure_criteria or not failure_match) and
            (not config.status_codes or status_match) and
            (not config.headers_criteria or headers_match)
        )
        confidence_score = _calculate_confidence_score(
            success_matches, failure_matches, regex_matches, status_match, headers_match
        )
        if confidence_score < config.confidence_threshold:
            is_valid = False
        metadata = {
            "response_status": response.status_code,
            "response_size": len(response_text),
            "headers_count": len(response.headers),
            "validation_criteria_count": (
                len(config.success_criteria) + len(config.failure_criteria) + 
                len(config.regex_patterns) + len(config.status_codes) + 
                len(config.headers_criteria)
            )
        }
        result = ValidationResult(
            is_valid=is_valid,
            matched_patterns=success_matches + failure_matches + regex_matches + header_matches,
            extracted_data=extracted_data,
            confidence_score=confidence_score,
            metadata=metadata
        )
        if return_structured:
            return result
        else:
            return is_valid
    except Exception as e:
        if return_structured:
            return ValidationResult(
                is_valid=False,
                error_message=str(e),
                confidence_score=0.0
            )
        else:
            return False

def extract_from_response(
    response: requests.Response,
    regex: str,
    group_names: Optional[List[str]] = None,
    extract_all: bool = False
) -> Union[List[str], Dict[str, str]]:
    try:
        compiled_regex = re.compile(regex, re.IGNORECASE | re.MULTILINE)
    except re.error as e:
        raise ValidationError(
            message=f"Invalid regex pattern: {e}",
            field="regex",
            value=regex
        )
    try:
        response_text = response.text
        if hasattr(response_text, '__call__'):
            response_text = response_text()
        if not isinstance(response_text, str):
            response_text = str(response_text) if response_text else ""
    except Exception:
        return [] if not group_names else {}
    matches = list(compiled_regex.finditer(response_text))
    if not matches:
        return [] if not group_names else {}
    if group_names:
        result = {}
        for match in matches:
            for group_name in group_names:
                if group_name in match.groupdict():
                    value = match.group(group_name)
                    if value:
                        if group_name not in result:
                            result[group_name] = []
                        result[group_name].append(value)
        if not extract_all:
            result = {k: v[0] if v else "" for k, v in result.items()}
        return result
    else:
        if extract_all:
            return [match.group(0) for match in matches]
        else:
            return [matches[0].group(0)] if matches else []

def validate_json_response(
    response: requests.Response,
    json_schema: Optional[Dict] = None,
    required_keys: Optional[List[str]] = None,
    forbidden_keys: Optional[List[str]] = None
) -> ValidationResult:
    try:
        content_type = response.headers.get("content-type", "").lower()
        if "json" not in content_type:
            return ValidationResult(
                is_valid=False,
                error_message="Response is not JSON",
                confidence_score=0.0
            )
        try:
            json_data = response.json()
        except json.JSONDecodeError as e:
            return ValidationResult(
                is_valid=False,
                error_message=f"Invalid JSON: {e}",
                confidence_score=0.0
            )
        missing_keys = []
        if required_keys:
            for key in required_keys:
                if key not in json_data:
                    missing_keys.append(key)
        found_forbidden_keys = []
        if forbidden_keys:
            for key in forbidden_keys:
                if key in json_data:
                    found_forbidden_keys.append(key)
        is_valid = len(missing_keys) == 0 and len(found_forbidden_keys) == 0
        confidence_score = 1.0 if is_valid else 0.0
        metadata = {
            "json_keys_count": len(json_data) if isinstance(json_data, dict) else 0,
            "missing_keys": missing_keys,
            "forbidden_keys_found": found_forbidden_keys
        }
        return ValidationResult(
            is_valid=is_valid,
            extracted_data={"json_data": json_data},
            confidence_score=confidence_score,
            metadata=metadata,
            validation_type=ValidationType.JSON_PATH
        )
    except Exception as e:
        return ValidationResult(
            is_valid=False,
            error_message=str(e),
            confidence_score=0.0
        )

def validate_html_response(
    response: requests.Response,
    css_selectors: Optional[List[str]] = None,
    xpath_expressions: Optional[List[str]] = None,
    title_patterns: Optional[List[str]] = None
) -> ValidationResult:
    try:
        content_type = response.headers.get("content-type", "").lower()
        if "html" not in content_type:
            return ValidationResult(
                is_valid=False,
                error_message="Response is not HTML",
                confidence_score=0.0
            )
        try:
            html_text = response.text
        except Exception as e:
            return ValidationResult(
                is_valid=False,
                error_message=f"Failed to read response: {e}",
                confidence_score=0.0
            )
        validation_results = []
        extracted_data = {}
        if title_patterns:
            title_match = re.search(r"<title[^>]*>(.*?)</title>", html_text, re.IGNORECASE | re.DOTALL)
            if title_match:
                title_text = title_match.group(1).strip()
                for pattern in title_patterns:
                    if pattern.lower() in title_text.lower():
                        validation_results.append(f"title_pattern: {pattern}")
                        extracted_data["title"] = title_text
                        break
        if "<html" in html_text.lower():
            validation_results.append("html_structure")
        confidence_score = min(len(validation_results) * 0.3, 1.0)
        is_valid = len(validation_results) > 0
        return ValidationResult(
            is_valid=is_valid,
            matched_patterns=validation_results,
            extracted_data=extracted_data,
            confidence_score=confidence_score,
            metadata={"html_size": len(html_text)},
            validation_type=ValidationType.REGEX_PATTERN
        )
    except Exception as e:
        return ValidationResult(
            is_valid=False,
            error_message=str(e),
            confidence_score=0.0
        )

def chain_validations(
    response: requests.Response,
    validation_chain: List[Dict[str, Any]]
) -> List[ValidationResult]:
    results = []
    for i, validation_config in enumerate(validation_chain):
        try:
            validation_config["return_structured"] = True
            result = validate_response(response, **validation_config)
            results.append(result)
        except Exception as e:
            results.append(ValidationResult(
                is_valid=False,
                error_message=str(e),
                confidence_score=0.0
            ))
    return results 