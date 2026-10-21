"""Country persistence.

Owner: Deeptanush (Tech Lead) · Task: T-102
"""

from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from invoice_api.db.models import Country


class CountryRepo:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_all(self) -> Sequence[Country]:
        result = await self.session.scalars(select(Country).order_by(Country.sort_order))
        return result.all()

    async def get(self, code: str) -> Country | None:
        return await self.session.get(Country, code.upper())

    async def upsert(self, code: str, name: str, sort_order: int, in_scope: bool = True) -> None:
        await self.session.merge(Country(code=code, name=name, sort_order=sort_order, in_scope=in_scope))
