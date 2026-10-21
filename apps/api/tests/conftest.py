"""Shared pytest fixtures: settings, app, HTTP client and a seeded database session.

Owner: Deeptanush (Tech Lead) · Task: T-101
"""

from collections.abc import AsyncIterator
from pathlib import Path

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from invoice_api.core.config import Settings
from invoice_api.db import models  # noqa: F401  (registers every table)
from invoice_api.db.base import Base
from invoice_api.db.seed import seed_all
from invoice_api.main import create_app


@pytest.fixture
def settings(tmp_path: Path) -> Settings:
    return Settings(
        _env_file=None,
        database_url=f"sqlite+aiosqlite:///{tmp_path / 'test.db'}",
        blob_local_dir=tmp_path / "blobs",
        spa_dist_dir=tmp_path / "no-spa",
        auth_mode="dev",
    )


@pytest.fixture
async def app(settings: Settings) -> AsyncIterator[FastAPI]:
    application = create_app(settings)
    yield application
    await application.state.engine.dispose()


@pytest.fixture
async def client(app: FastAPI) -> AsyncIterator[AsyncClient]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c


@pytest.fixture
async def db_session(app: FastAPI, settings: Settings) -> AsyncIterator[AsyncSession]:
    """Creates all tables on the test database, seeds reference data, yields a session."""
    async with app.state.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with app.state.session_factory() as session:
        await seed_all(session, settings.template_data_dir)
        await session.commit()
        yield session
