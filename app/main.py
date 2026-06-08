"""Main FastAPI application"""

import asyncio
import os

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.routes import api_router, web_router

_SIMULATED_LATENCY_MS = int(os.getenv("SIMULATED_LATENCY_MS", "0"))

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Issue Tracker API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# Simulates remote DB + network latency — set SIMULATED_LATENCY_MS env var to enable
if _SIMULATED_LATENCY_MS > 0:
    @app.middleware("http")
    async def simulate_latency(request: Request, call_next):
        if request.url.path != "/health":
            await asyncio.sleep(_SIMULATED_LATENCY_MS / 1000)
        return await call_next(request)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routers
app.include_router(api_router)
app.include_router(web_router)


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
