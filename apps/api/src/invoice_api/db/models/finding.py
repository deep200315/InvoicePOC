"""findings table (requirement id, type, priority, current, expected, result).

Owner: Deeptanush (Tech Lead) · Task: T-102
"""

import uuid

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from invoice_api.db.base import Base, str_enum
from invoice_api.domain.enums import CheckType, Outcome, Priority, RequirementType


class FindingRecord(Base):
    __tablename__ = "findings"

    id: Mapped[int] = mapped_column(primary_key=True)
    comparison_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("comparisons.id", ondelete="CASCADE"), index=True
    )
    requirement_id: Mapped[str | None] = mapped_column(String(8))
    field_id: Mapped[str] = mapped_column(String(64))
    section: Mapped[str] = mapped_column(String(32))
    check_type: Mapped[CheckType] = mapped_column(str_enum(CheckType))
    requirement_type: Mapped[RequirementType] = mapped_column(str_enum(RequirementType))
    priority: Mapped[Priority] = mapped_column(str_enum(Priority))
    current: Mapped[str | None] = mapped_column(Text)
    expected: Mapped[str] = mapped_column(Text)
    result: Mapped[Outcome] = mapped_column(str_enum(Outcome))
