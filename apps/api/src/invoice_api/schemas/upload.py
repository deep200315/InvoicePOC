"""Upload response DTO (screens 03 / 04).

Owner: Deeptanush (Tech Lead) · Task: T-103
"""

from datetime import datetime
from uuid import UUID

from invoice_api.domain.enums import FileType
from invoice_api.schemas.common import ApiModel


class UploadOut(ApiModel):
    invoice_id: UUID
    country_code: str
    filename: str
    file_type: FileType
    size_bytes: int
    sha256: str
    pages: int | None
    uploaded_at: datetime
