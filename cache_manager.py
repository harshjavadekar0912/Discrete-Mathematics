"""
Cache Manager - In-Memory TTL Cache for Tourist Guide Assistant
Provides thread-safe caching with expiration for API responses,
geocoding, places searches, and road networks.
"""

import time
import threading
from typing import Any, Optional

class SimpleTTLCache:
    def __init__(self, default_ttl: int = 3600):
        self.default_ttl = default_ttl
        self._cache = {}
        self._lock = threading.Lock()

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            if key not in self._cache:
                return None
            val, expire_time = self._cache[key]
            if time.time() > expire_time:
                del self._cache[key]
                return None
            return val

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        if ttl is None:
            ttl = self.default_ttl
        with self._lock:
            self._cache[key] = (value, time.time() + ttl)

    def clear(self) -> None:
        with self._lock:
            self._cache.clear()

    def size(self) -> int:
        with self._lock:
            # clean expired on size check
            now = time.time()
            expired_keys = [k for k, (_, exp) in self._cache.items() if now > exp]
            for k in expired_keys:
                del self._cache[k]
            return len(self._cache)

# Global caches with custom TTLs
geo_cache = SimpleTTLCache(default_ttl=86400)      # 24 hours for geocoding
places_cache = SimpleTTLCache(default_ttl=7200)    # 2 hours for places searches
routes_cache = SimpleTTLCache(default_ttl=7200)    # 2 hours for routes
network_cache = SimpleTTLCache(default_ttl=86400)  # 24 hours for road networks

