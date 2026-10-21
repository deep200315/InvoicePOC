"""Requirement DTOs: the gap list R-01..R-n (screens 07 / 07a).

Owner: Deeptanush (Tech Lead) · Task: T-103
"""

from uuid import UUID

from invoice_api.domain.enums import Outcome, Priority, RequirementType
from invoice_api.schemas.common import ApiModel


class RequirementOut(ApiModel):
    id: str
    field_id: str
    field_label: str
    section: str
    current: str | None
    expected: str
    type: RequirementType
    priority: Priority
    result: Outcome


class RequirementSummary(ApiModel):
    fields_matched: int
    fields_total: int
    missing_or_different: int
    mandatory: int
    standard: int
    advisory: int
    percent: int


class RequirementsOut(ApiModel):
    comparison_id: UUID
    country_code: str
    summary: RequirementSummary
    items: list[RequirementOut]
    matching_field_labels: list[str]
