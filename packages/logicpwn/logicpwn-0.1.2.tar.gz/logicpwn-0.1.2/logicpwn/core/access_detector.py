"""
This module has been split for modularity. Please use logicpwn.core.access.detector, logicpwn.core.access.models, and logicpwn.core.access.utils instead.
"""
from logicpwn.core.access.detector import detect_idor_flaws, detect_idor_flaws_async
from logicpwn.core.access.models import AccessTestResult, AccessDetectorConfig
from logicpwn.core.access.utils import (
    _validate_inputs, _sanitize_test_id, _test_single_id, _test_single_id_async
) 