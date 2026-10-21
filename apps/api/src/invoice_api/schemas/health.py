"""Health check DTO.

Owner: Deeptanush (Tech Lead) · Task: T-101
"""

from invoice_api.schemas.common import ApiModel


class HealthOut(ApiModel):
    status: str
    version: str
