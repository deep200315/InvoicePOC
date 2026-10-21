from sqlalchemy.ext.asyncio import AsyncSession

from invoice_api.db.repositories.country_repo import CountryRepo
from invoice_api.db.repositories.template_repo import TemplateRepo


async def test_seed_creates_six_countries_in_display_order(db_session: AsyncSession) -> None:
    countries = await CountryRepo(db_session).list_all()
    assert [c.code for c in countries] == ["RO", "NO", "RU", "UA", "NP", "IN"]
    assert all(c.in_scope for c in countries)


async def test_seed_records_global_template_version(db_session: AsyncSession) -> None:
    record = await TemplateRepo(db_session).get("global_proforma", 1)
    assert record is not None
    assert record.field_count == 31
    assert record.title == "Global Proforma Invoice"
