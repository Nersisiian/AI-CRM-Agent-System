from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.middleware.base import BaseHTTPMiddleware
from config import settings

limiter = Limiter(key_func=get_remote_address, default_limits=[f"{settings.RATE_LIMIT_PER_SECOND}/second"])

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Используем slowapi в качестве middleware
        return await call_next(request)

# В реальном приложении limiter подключается через app.add_middleware(SlowAPIMiddleware)