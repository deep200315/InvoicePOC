"""Country DTOs (Home table, country picker).

Owner: Deeptanush (Tech Lead) · Task: T-103
"""

from datetime import datetime
from uuid import UUID

from invoice_api.domain.enums import ComparisonStatus, Verdict
from invoice_api.schemas.common import ApiModel


class LatestComparison(ApiModel):
    comparison_id: UUID
    invoice_filename: str
    status: ComparisonStatus
    score_percent: int | None
    verdict: Verdict | None
    compared_at: datetime


class CountryOut(ApiModel):
    code: str
    name: str
    in_scope: bool
    latest: LatestComparison | None
