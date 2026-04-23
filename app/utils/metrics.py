from collections import defaultdict
from starlette.middleware.base import BaseHTTPMiddleware
import threading

class MetricsCollector:
    def __init__(self):
        self._lock = threading.Lock()
        self._counters = defaultdict(int)

    def increment(self, key: str, value: int = 1):
        with self._lock:
            self._counters[key] += value

    def get(self, key: str, default=0):
        with self._lock:
            return self._counters.get(key, default)

metrics_collector = MetricsCollector()

class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        metrics_collector.increment("total_requests")
        response = await call_next(request)
        return response