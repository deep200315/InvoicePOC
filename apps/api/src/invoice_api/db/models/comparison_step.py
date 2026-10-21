"""comparison_steps table (step, status, detail) for progress.

Owner: Deeptanush (Tech Lead) · Task: T-102
"""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from invoice_api.db.base import Base, str_enum
from invoice_api.domain.enums import StepName, StepStatus


class ComparisonStep(Base):
    __tablename__ = "comparison_steps"
    __table_args__ = (UniqueConstraint("comparison_id", "name"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    comparison_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("comparisons.id", ondelete="CASCADE"))
    name: Mapped[StepName] = mapped_column(str_enum(StepName))
    position: Mapped[int]
    status: Mapped[StepStatus] = mapped_column(str_enum(StepStatus), default=StepStatus.PENDING)
    detail: Mapped[str | None] = mapped_column(Text)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
