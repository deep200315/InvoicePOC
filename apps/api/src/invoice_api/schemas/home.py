"""Home overview and recent activity DTOs (screens 02 / 09).

Owner: Deeptanush (Tech Lead) · Task: T-103
"""

from datetime import datetime
from enum import StrEnum
from uuid import UUID

from invoice_api.schemas.common import ApiModel


class HomeOverview(ApiModel):
    countries_in_scope: int
    compared: int
    missing_or_different: int
    matching: int


class ActivityKind(StrEnum):
    COMPARED = "compared"
    VERDICT = "verdict"


class ActivityItem(ApiModel):
    kind: ActivityKind
    comparison_id: UUID
    country_code: str
    title: str
    detail: str
    at: datetime
