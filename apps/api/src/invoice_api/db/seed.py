"""Idempotent seed of reference data: countries in scope (template rows added in T-104).

Owner: Deeptanush (Tech Lead) · Task: T-102
"""

from pathlib import Path

import yaml
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from invoice_api.db.repositories.country_repo import CountryRepo


class _CountrySeed(BaseModel):
    code: str
    name: str


class _CountriesFile(BaseModel):
    countries: list[_CountrySeed]


async def seed_countries(session: AsyncSession, template_data_dir: Path) -> int:
    raw = yaml.safe_load((template_data_dir / "countries_in_scope.yaml").read_text())
    data = _CountriesFile.model_validate(raw)
    repo = CountryRepo(session)
    for order, country in enumerate(data.countries):
        await repo.upsert(country.code, country.name, sort_order=order)
    return len(data.countries)


async def seed_all(session: AsyncSession, template_data_dir: Path) -> dict[str, int]:
    return {"countries": await seed_countries(session, template_data_dir)}
