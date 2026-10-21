"""Mounts every v1 router under /api/v1. Everything except /health needs a signed-in user.

Owner: Deeptanush (Tech Lead) · Task: T-103
"""

from fastapi import APIRouter, Depends

from invoice_api.api.v1 import health, me
from invoice_api.core.deps import get_current_user

protected = APIRouter(dependencies=[Depends(get_current_user)])
protected.include_router(me.router)

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(health.router)
api_router.include_router(protected)
