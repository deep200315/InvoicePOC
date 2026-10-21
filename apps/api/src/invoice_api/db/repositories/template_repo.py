"""Global template version persistence.

Owner: Deeptanush (Tech Lead) · Task: T-104
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from invoice_api.db.models import TemplateRecord
from invoice_api.services.template_service import LoadedTemplate


class TemplateRepo:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, key: str, version: int) -> TemplateRecord | None:
        stmt = select(TemplateRecord).where(TemplateRecord.key == key, TemplateRecord.version == version)
        return await self.session.scalar(stmt)

    async def upsert(self, loaded: LoadedTemplate) -> TemplateRecord:
        t = loaded.template
        record = await self.get(t.id, t.version)
        if record is None:
            record = TemplateRecord(key=t.id, version=t.version)
            self.session.add(record)
        record.title = t.title
        record.checksum = loaded.checksum
        record.field_count = t.field_count
        return record
