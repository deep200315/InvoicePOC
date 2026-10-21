"""Shared pytest fixtures: settings, app and HTTP client.

Owner: Deeptanush (Tech Lead) · Task: T-101
"""

from collections.abc import AsyncIterator
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient

from invoice_api.core.config import Settings
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
async def client(settings: Settings) -> AsyncIterator[AsyncClient]:
    app = create_app(settings)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
