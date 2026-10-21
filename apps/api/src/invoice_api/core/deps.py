"""Shared FastAPI dependencies: settings, DB session, current user, blob store.

Owner: Deeptanush (Tech Lead) · Task: T-101
"""

from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from invoice_api.core.config import Settings, get_settings
from invoice_api.storage.base import BlobStore

SettingsDep = Annotated[Settings, Depends(get_settings)]


def get_session_factory(request: Request) -> async_sessionmaker[AsyncSession]:
    factory: async_sessionmaker[AsyncSession] = request.app.state.session_factory
    return factory


async def get_session(request: Request) -> AsyncIterator[AsyncSession]:
    async with get_session_factory(request)() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]
SessionFactoryDep = Annotated[async_sessionmaker[AsyncSession], Depends(get_session_factory)]


def get_blob_store(request: Request) -> BlobStore:
    store: BlobStore = request.app.state.blob_store
    return store


BlobStoreDep = Annotated[BlobStore, Depends(get_blob_store)]
