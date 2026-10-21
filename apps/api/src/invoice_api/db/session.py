"""Async engine and session factory.

Owner: Deeptanush (Tech Lead) · Task: T-102
"""

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from invoice_api.core.config import Settings
from invoice_api.db.url import to_async_url


def build_engine(settings: Settings) -> AsyncEngine:
    db = to_async_url(settings.database_url)
    return create_async_engine(db.url, connect_args=db.connect_args, pool_pre_ping=True)


def build_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine, expire_on_commit=False)
