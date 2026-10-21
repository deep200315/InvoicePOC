"""Mounts every v1 router under /api/v1.

Owner: Deeptanush (Tech Lead) · Task: T-103
"""

from fastapi import APIRouter

from invoice_api.api.v1 import health

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(health.router)
