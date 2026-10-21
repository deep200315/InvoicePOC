"""Alembic environment: async engine, URL from Settings (or config attribute in tests).

Owner: Deeptanush (Tech Lead) · Task: T-102
"""

import asyncio

from alembic import context
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool

from invoice_api.core.config import get_settings
from invoice_api.db import models  # noqa: F401  (registers every table)
from invoice_api.db.base import Base
from invoice_api.db.url import to_async_url

config = context.config
target_metadata = Base.metadata


def _db_url() -> str:
    url = config.attributes.get("database_url")
    return str(url) if url else get_settings().database_url


def _configure(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        render_as_batch=connection.dialect.name == "sqlite",
    )
    with context.begin_transaction():
        context.run_migrations()


async def _run_online() -> None:
    db = to_async_url(_db_url())
    engine = create_async_engine(db.url, connect_args=db.connect_args, poolclass=NullPool)
    async with engine.connect() as connection:
        await connection.run_sync(_configure)
    await engine.dispose()


if context.is_offline_mode():
    context.configure(url=to_async_url(_db_url()).url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()
else:
    asyncio.run(_run_online())
