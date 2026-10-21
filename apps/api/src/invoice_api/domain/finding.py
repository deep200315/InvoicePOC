"""Finding: one rule's result for one template field (pure, no I/O).

Owner: Deeptanush (Tech Lead) · Task: T-103
"""

from pydantic import BaseModel, ConfigDict

from invoice_api.domain.enums import CheckType, Outcome, RequirementType


class Finding(BaseModel):
    model_config = ConfigDict(frozen=True)

    field_id: str
    section: str
    check: CheckType
    type: RequirementType
    current: str | None
    expected: str
    result: Outcome
