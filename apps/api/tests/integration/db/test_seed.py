from sqlalchemy.ext.asyncio import AsyncSession

from invoice_api.db.repositories.country_repo import CountryRepo


async def test_seed_creates_six_countries_in_display_order(db_session: AsyncSession) -> None:
    countries = await CountryRepo(db_session).list_all()
    assert [c.code for c in countries] == ["RO", "NO", "RU", "UA", "NP", "IN"]
    assert all(c.in_scope for c in countries)
