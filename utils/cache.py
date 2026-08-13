# utils/cache.py
from datetime import datetime, timedelta
from typing import Any, Dict, Optional
import hashlib
import json

class CacheManager:
    def __init__(self):
        self.cache = {}
        self.default_ttl = 3600  # 1 hour
    
    def get(self, key: str) -> Optional[Any]:
        if key in self.cache:
            entry = self.cache[key]
            if datetime.now() < entry['expires_at']:
                return entry['data']
            else:
                del self.cache[key]
        return None
    
    def set(self, key: str, data: Any, ttl: int = None):
        if ttl is None:
            ttl = self.default_ttl
        self.cache[key] = {
            'data': data,
            'expires_at': datetime.now() + timedelta(seconds=ttl)
        }
    
    def get_or_set(self, key: str, func, ttl: int = None):
        cached = self.get(key)
        if cached is not None:
            return cached
        result = func()
        self.set(key, result, ttl)
        return result
    
    def clear(self, prefix: str = None):
        if prefix:
            keys = [k for k in self.cache.keys() if k.startswith(prefix)]
            for key in keys:
                del self.cache[key]
        else:
            self.cache.clear()
    
    def get_stats(self) -> Dict:
        total = len(self.cache)
        expired = sum(1 for v in self.cache.values() 
                     if datetime.now() >= v['expires_at'])
        return {
            "total_entries": total,
            "expired_entries": expired,
            "active_entries": total - expired
        }
    