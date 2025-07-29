"""
Session cache for LogicPwn.
"""
from typing import Any, Optional
from .cache_manager import CacheManager

class SessionCache:
    def __init__(self, max_size: int = 100, default_ttl: int = 3600):
        self.cache_manager = CacheManager(max_size, default_ttl)

    def get_session(self, session_id: str) -> Optional[Any]:
        return self.cache_manager.get(session_id)

    def set_session(self, session_id: str, session: Any, ttl: Optional[int] = None) -> None:
        self.cache_manager.set(session_id, session, ttl)

    def invalidate_session(self, session_id: str) -> bool:
        return self.cache_manager.invalidate(session_id) 