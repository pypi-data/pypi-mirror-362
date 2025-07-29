"""
Authentication session logic for LogicPwn.
"""
import requests
from typing import Dict, Any, Optional, Union
from loguru import logger
from logicpwn.exceptions import (
    AuthenticationError,
    LoginFailedException,
    NetworkError,
    ValidationError,
    TimeoutError
)
from logicpwn.core.utils import prepare_request_kwargs, validate_config
from logicpwn.core.performance import monitor_performance
from logicpwn.core.cache import session_cache
from .auth_models import AuthConfig
from .auth_utils import _sanitize_credentials, _create_session, _handle_response_indicators
from .auth_constants import DEFAULT_SESSION_TIMEOUT

@monitor_performance("authentication")
def authenticate_session(auth_config: Union[AuthConfig, Dict[str, Any]]) -> requests.Session:
    try:
        config = validate_config(auth_config, AuthConfig)
        session_id = f"{config.url}_{config.method}_{hash(str(config.credentials))}"
        cached_session = session_cache.get_session(session_id)
        if cached_session:
            logger.debug(f"Using cached session for {config.url}")
            return cached_session
        sanitized_creds = _sanitize_credentials(config.credentials)
        logger.info(f"Attempting authentication to {config.url} with method {config.method}")
        logger.debug(f"Credentials: {sanitized_creds}")
        session = _create_session(config)
        request_kwargs = prepare_request_kwargs(
            method=config.method,
            url=config.url,
            credentials=config.credentials,
            headers=config.headers,
            timeout=config.timeout,
            verify_ssl=config.verify_ssl
        )
        logger.debug(f"Sending {config.method} request to {config.url}")
        response = session.request(config.method, config.url, **request_kwargs)
        response.raise_for_status()
        _handle_response_indicators(response, config)
        if not session.cookies:
            logger.warning("No cookies received during authentication")
        session_cache.set_session(session_id, session)
        logger.info("Authentication successful - session created with persistent cookies")
        return session
    except requests.exceptions.Timeout as e:
        logger.error(f"Authentication request timed out after {config.timeout} seconds")
        raise TimeoutError(
            message=f"Authentication request timed out after {config.timeout} seconds",
            timeout_seconds=config.timeout
        ) from e
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Network connection error during authentication: {e}")
        raise NetworkError(
            message="Network connection error during authentication",
            original_exception=e
        ) from e
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error during authentication: {e}")
        raise NetworkError(
            message=f"Request error during authentication: {e}",
            original_exception=e
        ) from e
    except ValueError as e:
        logger.error(f"Configuration validation error: {e}")
        raise ValidationError(
            message=f"Configuration validation error: {e}",
            field="configuration",
            value=str(e)
        ) from e
    except LoginFailedException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error during authentication: {e}")
        raise AuthenticationError(f"Unexpected error during authentication: {e}") from e

def validate_session(session: requests.Session, test_url: str) -> bool:
    try:
        response = session.get(test_url, timeout=DEFAULT_SESSION_TIMEOUT)
        return response.status_code == 200
    except (requests.exceptions.RequestException, requests.exceptions.Timeout) as e:
        logger.warning(f"Session validation failed: {e}")
        return False

def logout_session(session: requests.Session, logout_url: str) -> bool:
    try:
        response = session.get(logout_url, timeout=DEFAULT_SESSION_TIMEOUT)
        session.cookies.clear()
        logger.info("Session logged out successfully")
        return True
    except (requests.exceptions.RequestException, requests.exceptions.Timeout) as e:
        logger.error(f"Logout failed: {e}")
        return False 