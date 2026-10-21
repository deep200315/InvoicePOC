"""Seed countries and the global template into the database named by DATABASE_URL.

Owner: Deeptanush (Tech Lead) · Task: T-102
Run from apps/api: .venv/bin/python ../../scripts/seed_dev.py
"""

import asyncio

from invoice_api.core.config import get_settings
from invoice_api.db.seed import seed_all
from invoice_api.db.session import build_engine, build_session_factory


async def main() -> None:
    settings = get_settings()
    engine = build_engine(settings)
    async with build_session_factory(engine)() as session:
        summary = await seed_all(session, settings.template_data_dir)
        await session.commit()
    await engine.dispose()
    print(f"Seeded: {summary}")


if __name__ == "__main__":
    asyncio.run(main())
