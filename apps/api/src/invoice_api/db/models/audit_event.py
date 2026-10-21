"""audit_events table (append-only).

Owner: Deeptanush (Tech Lead) · Task: T-102
"""

from datetime import datetime
from typing import Any

from sqlalchemy import JSON, BigInteger, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from invoice_api.db.base import Base, utcnow


class AuditEvent(Base):
    __tablename__ = "audit_events"

    id: Mapped[int] = mapped_column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, index=True)
    actor: Mapped[str] = mapped_column(String(255))
    action: Mapped[str] = mapped_column(String(64))
    entity_type: Mapped[str | None] = mapped_column(String(32))
    entity_id: Mapped[str | None] = mapped_column(String(64))
    ip: Mapped[str | None] = mapped_column(String(64))
    detail: Mapped[dict[str, Any] | None] = mapped_column(JSON)
