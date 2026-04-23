import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import api_router
from app.logging_config import setup_logging
from app.utils.metrics import MetricsMiddleware
from app.utils.rate_limiter import RateLimitMiddleware
from config import settings

def create_app() -> FastAPI:
    setup_logging()
    app = FastAPI(
        title="AI Business Agent",
        version="2.0.0",
        docs_url="/docs",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(MetricsMiddleware)
    app.add_middleware(RateLimitMiddleware)
    app.include_router(api_router, prefix="/api/v1")
    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)