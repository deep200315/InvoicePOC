"""GET /health - liveness/readiness for Container Apps.

Owner: Deeptanush (Tech Lead) · Task: T-101
"""

from fastapi import APIRouter

from invoice_api.core.deps import SettingsDep
from invoice_api.schemas.health import HealthOut

router = APIRouter(tags=["health"])


@router.get("/health")
async def health(settings: SettingsDep) -> HealthOut:
    return HealthOut(status="ok", version=settings.version)
