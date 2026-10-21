"""Comparison DTOs: create request, progress (screen 05), full result (screens 06 / 08).

Owner: Deeptanush (Tech Lead) · Task: T-103
"""

from datetime import datetime
from uuid import UUID

from pydantic import Field

from invoice_api.domain.enums import ComparisonStatus, Outcome, Priority, StepName, StepStatus, Verdict
from invoice_api.schemas.common import ApiModel, BBox
from invoice_api.schemas.upload import UploadOut


class ComparisonCreate(ApiModel):
    country_code: str = Field(min_length=2, max_length=2, examples=["RO"])
    invoice_id: UUID


class StepOut(ApiModel):
    name: StepName
    status: StepStatus
    detail: str | None
    started_at: datetime | None
    finished_at: datetime | None


class ComparisonStatusOut(ApiModel):
    id: UUID
    status: ComparisonStatus
    steps: list[StepOut]
    error_code: str | None
    error_message: str | None


class ScoreOut(ApiModel):
    matched: int
    total: int
    percent: int
    verdict: Verdict


class FieldResultOut(ApiModel):
    field_id: str
    label: str
    section: str
    priority: Priority
    local_label: str | None
    local_value: str | None
    page: int | None
    bbox: BBox | None
    cell: str | None
    matched_by: str | None
    result: Outcome
    requirement_id: str | None


class ComparisonOut(ApiModel):
    id: UUID
    country_code: str
    country_name: str
    invoice: UploadOut
    template_id: str
    template_version: int
    status: ComparisonStatus
    score: ScoreOut | None
    fields: list[FieldResultOut]
    created_at: datetime
    completed_at: datetime | None
