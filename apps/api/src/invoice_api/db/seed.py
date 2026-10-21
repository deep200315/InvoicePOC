"""Idempotent seed of reference data: countries in scope and the global template version.

Owner: Deeptanush (Tech Lead) · Task: T-102
"""

from pathlib import Path

import yaml
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from invoice_api.db.repositories.country_repo import CountryRepo
from invoice_api.db.repositories.template_repo import TemplateRepo
from invoice_api.services.template_service import load_global_template


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


async def seed_template(session: AsyncSession, template_data_dir: Path) -> int:
    await TemplateRepo(session).upsert(load_global_template(template_data_dir))
    return 1


async def seed_all(session: AsyncSession, template_data_dir: Path) -> dict[str, int]:
    return {
        "countries": await seed_countries(session, template_data_dir),
        "templates": await seed_template(session, template_data_dir),
    }
