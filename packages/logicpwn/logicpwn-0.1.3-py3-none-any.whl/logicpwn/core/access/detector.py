from typing import List, Union, Optional
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from logicpwn.core.performance.performance_monitor import monitor_performance
from logicpwn.core.runner.async_runner_core import AsyncRequestRunner
import asyncio
from .models import AccessTestResult, AccessDetectorConfig
from .utils import (
    _validate_inputs, _sanitize_test_id, _test_single_id, _test_single_id_async, _test_single_id_with_baselines, _test_single_id_with_baselines_async
)

def _get_request_config_for_id(config: AccessDetectorConfig, test_id: Union[str, int]) -> dict:
    """Helper to get method and request data for a given test ID."""
    method = config.method or "GET"
    data = None
    if config.request_data_map and test_id in config.request_data_map:
        data = config.request_data_map[test_id]
    return {"method": method, "data": data}

@monitor_performance("idor_detection_batch")
def detect_idor_flaws(
    session: requests.Session,
    endpoint_template: str,
    test_ids: List[Union[str, int]],
    success_indicators: List[str],
    failure_indicators: List[str],
    config: Optional[AccessDetectorConfig] = None
) -> List[AccessTestResult]:
    """
    Run IDOR/access control tests for a list of IDs, supporting custom HTTP methods, per-ID data, and multiple baselines.
    """
    config = config or AccessDetectorConfig()
    _validate_inputs(endpoint_template, test_ids, success_indicators, failure_indicators)
    results: List[AccessTestResult] = []
    with ThreadPoolExecutor(max_workers=config.max_concurrent_requests) as executor:
        futures = []
        for test_id in test_ids:
            sanitized_id = _sanitize_test_id(test_id)
            url = endpoint_template.format(id=sanitized_id)
            req_cfg = _get_request_config_for_id(config, test_id)
            # Use new helper for multi-baseline support
            futures.append(executor.submit(
                _test_single_id_with_baselines,
                session,
                url,
                sanitized_id,
                req_cfg["method"],
                req_cfg["data"],
                success_indicators,
                failure_indicators,
                config.request_timeout,
                config
            ))
        for future in as_completed(futures):
            results.append(future.result())
    return results

async def detect_idor_flaws_async(
    endpoint_template: str,
    test_ids: List[Union[str, int]],
    success_indicators: List[str],
    failure_indicators: List[str],
    config: Optional[AccessDetectorConfig] = None
) -> List[AccessTestResult]:
    """
    Async version of IDOR/access control tests, supporting custom HTTP methods, per-ID data, and multiple baselines.
    """
    config = config or AccessDetectorConfig()
    _validate_inputs(endpoint_template, test_ids, success_indicators, failure_indicators)
    results: List[AccessTestResult] = []
    async with AsyncRequestRunner(max_concurrent=config.max_concurrent_requests, timeout=config.request_timeout) as runner:
        tasks = []
        for test_id in test_ids:
            sanitized_id = _sanitize_test_id(test_id)
            url = endpoint_template.format(id=sanitized_id)
            req_cfg = _get_request_config_for_id(config, test_id)
            tasks.append(_test_single_id_with_baselines_async(
                runner,
                url,
                sanitized_id,
                req_cfg["method"],
                req_cfg["data"],
                success_indicators,
                failure_indicators,
                config.request_timeout,
                config
            ))
        results = await asyncio.gather(*tasks)
    return results 