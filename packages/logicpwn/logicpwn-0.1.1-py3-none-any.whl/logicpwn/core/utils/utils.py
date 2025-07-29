"""
Shared utility functions for LogicPwn core modules.

This module provides reusable logic for indicator/criteria checking and request kwargs preparation,
used by auth, runner, and validator modules to avoid redundancy and improve interoperability.
"""

from typing import List, Dict, Any, Tuple, Optional, Union, Type
import re


def check_indicators(
    text: str,
    indicators: List[str],
    indicator_type: str = "indicator"
) -> Tuple[bool, List[str]]:
    """
    Check if any of the given indicators are present in the text (case-insensitive).
    Returns (is_match, matched_indicators).
    """
    if not indicators or not text:
                                            return False, []
    text_lower = text.lower()
    matched = [i for i in indicators if i.lower() in text_lower]
    return bool(matched), matched


def prepare_request_kwargs(
    method: str,
    url: str,
    credentials: Optional[Dict[str, str]] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: Optional[int] = None,
    verify_ssl: Optional[bool] = True,
    data: Optional[Any] = None,
    params: Optional[Dict[str, Any]] = None,
    json_data: Optional[Dict[str, Any]] = None,
    raw_body: Optional[str] = None
) -> Dict[str, Any]:
    """
    Prepare kwargs for requests.Session.request() or similar, supporting form, JSON, and raw body.
    Used by both auth and runner modules.
    """
    kwargs = {
                                            'method': method.upper(),
                                            'url': url,
                                            'timeout': timeout,
                                            'verify': verify_ssl
    }
    if headers:
                                            kwargs['headers'] = headers
    # Only one body type allowed
    if data is not None:
                                            kwargs['data'] = data
    elif json_data is not None:
                                            kwargs['json'] = json_data
    elif raw_body is not None:
                                            kwargs['data'] = raw_body
    # For GET with credentials as params
    if method.upper() == "GET" and credentials:
                                            kwargs['params'] = credentials
    # For POST with credentials as form data
    if method.upper() == "POST" and credentials:
                                            kwargs['data'] = credentials
    # Additional params
    if params:
                                            kwargs['params'] = params
    return kwargs


def validate_config(config: Union[dict, Any], model_class: Type) -> Any:
    """
    Validate and convert a configuration dict or model instance to a model instance.
    Args:
                                            config: dict or model instance
                                            model_class: the Pydantic model class to use
    Returns:
                                            Validated model instance
    Raises:
                                            ValueError: if config is not valid
    """
    if isinstance(config, model_class):
                                            return config
    if isinstance(config, dict):
                                            return model_class(**config)
    raise ValueError(f"Configuration must be dict or {model_class.__name__}, got {type(config)}") 