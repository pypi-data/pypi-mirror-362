"""
Echo Sync Protocol API

This package provides the API implementation for the Echo Sync Protocol,
enabling bidirectional state synchronization between EchoNodes across the multiverse.
"""

from fastapi import FastAPI
from .routes import router as echo_sync_router

app = FastAPI(
    title="Echo Sync Protocol API",
    description="API for bidirectional state synchronization between EchoNodes",
    version="0.1.0"
)

app.include_router(echo_sync_router, prefix="/api/v1/echo-sync", tags=["echo-sync"]) 