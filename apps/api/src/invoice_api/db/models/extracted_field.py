"""extracted_fields table (label, value, bbox, matched field, matcher).

Owner: Deeptanush (Tech Lead) · Task: T-102
"""

import uuid
from typing import Any

from sqlalchemy import JSON, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from invoice_api.db.base import Base


class ExtractedFieldRecord(Base):
    __tablename__ = "extracted_fields"

    id: Mapped[int] = mapped_column(primary_key=True)
    comparison_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("comparisons.id", ondelete="CASCADE"), index=True
    )
    local_label: Mapped[str | None] = mapped_column(Text)
    local_value: Mapped[str | None] = mapped_column(Text)
    page: Mapped[int | None]
    bbox: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    cell: Mapped[str | None] = mapped_column(String(16))
    field_id: Mapped[str | None] = mapped_column(String(64))
    matcher: Mapped[str | None] = mapped_column(String(32))
    rule: Mapped[str | None] = mapped_column(Text)
    section_found: Mapped[str | None] = mapped_column(String(32))
