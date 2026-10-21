"""invoices table (blob key, sha256, type, pages).

Owner: Deeptanush (Tech Lead) · Task: T-102
"""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from invoice_api.db.base import Base, str_enum, utcnow
from invoice_api.domain.enums import FileType


class Invoice(Base):
    __tablename__ = "invoices"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    country_code: Mapped[str] = mapped_column(ForeignKey("countries.code"), index=True)
    filename: Mapped[str] = mapped_column(String(255))
    file_type: Mapped[FileType] = mapped_column(str_enum(FileType))
    size_bytes: Mapped[int]
    sha256: Mapped[str] = mapped_column(String(64), index=True)
    blob_key: Mapped[str] = mapped_column(String(512))
    pages: Mapped[int | None]
    uploaded_by: Mapped[str] = mapped_column(String(255))
    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
