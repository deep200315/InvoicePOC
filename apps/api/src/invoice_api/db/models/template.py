"""templates table: one row per global template version, with the YAML checksum.

Owner: Deeptanush (Tech Lead) · Task: T-102
"""

from datetime import datetime

from sqlalchemy import DateTime, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from invoice_api.db.base import Base, utcnow


class TemplateRecord(Base):
    __tablename__ = "templates"
    __table_args__ = (UniqueConstraint("key", "version"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column(String(64))
    version: Mapped[int]
    title: Mapped[str] = mapped_column(String(200))
    checksum: Mapped[str] = mapped_column(String(64))
    field_count: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
