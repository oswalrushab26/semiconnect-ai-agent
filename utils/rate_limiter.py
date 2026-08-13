# utils/rate_limiter.py
from datetime import datetime, timedelta
from collections import defaultdict
from typing import List

class RateLimiter:
    def __init__(self, max_calls: int = 10, period: int = 60):
        self.max_calls = max_calls
        self.period = period
        self.calls = defaultdict(list)
    
    def allow_request(self, client_id: str = "default") -> bool:
        now = datetime.now()
        self.calls[client_id] = [
            call for call in self.calls[client_id] 
            if call > now - timedelta(seconds=self.period)
        ]
        
        if len(self.calls[client_id]) < self.max_calls:
            self.calls[client_id].append(now)
            return True
        return False
    
    def get_remaining(self, client_id: str = "default") -> int:
        now = datetime.now()
        self.calls[client_id] = [
            call for call in self.calls[client_id] 
            if call > now - timedelta(seconds=self.period)
        ]
        return max(0, self.max_calls - len(self.calls[client_id]))

class TieredRateLimiter:
    def __init__(self):
        self.limiters = {
            "free": RateLimiter(max_calls=10, period=60),
            "pro": RateLimiter(max_calls=50, period=60),
            "enterprise": RateLimiter(max_calls=200, period=60)
        }
    
    def allow_request(self, tier: str, client_id: str = "default") -> bool:
        limiter = self.limiters.get(tier, self.limiters["free"])
        return limiter.allow_request(client_id)
    
    def get_remaining(self, tier: str, client_id: str = "default") -> int:
        limiter = self.limiters.get(tier, self.limiters["free"])
        return limiter.get_remaining(client_id)
    