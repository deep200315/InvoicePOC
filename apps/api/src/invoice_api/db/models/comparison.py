"""comparisons table (country, invoice, template version, status, score).

Owner: Deeptanush (Tech Lead) · Task: T-102
"""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from invoice_api.db.base import Base, str_enum, utcnow
from invoice_api.db.models.comparison_step import ComparisonStep
from invoice_api.db.models.invoice import Invoice
from invoice_api.domain.enums import ComparisonStatus


class Comparison(Base):
    __tablename__ = "comparisons"
    __table_args__ = (Index("ix_comparisons_country_created", "country_code", "created_at"),)

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    country_code: Mapped[str] = mapped_column(ForeignKey("countries.code"))
    invoice_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("invoices.id"))
    template_key: Mapped[str] = mapped_column(String(64))
    template_version: Mapped[int]
    status: Mapped[ComparisonStatus] = mapped_column(
        str_enum(ComparisonStatus), default=ComparisonStatus.PENDING
    )
    matched_count: Mapped[int | None]
    total_count: Mapped[int | None]
    error_code: Mapped[str | None] = mapped_column(String(64))
    error_message: Mapped[str | None] = mapped_column(Text)
    created_by: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    invoice: Mapped[Invoice] = relationship(lazy="selectin")
    steps: Mapped[list[ComparisonStep]] = relationship(
        lazy="selectin", order_by=ComparisonStep.position, cascade="all, delete-orphan"
    )
