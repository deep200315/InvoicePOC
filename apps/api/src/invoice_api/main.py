"""FastAPI app factory. Run with: uvicorn invoice_api.main:create_app --factory

Owner: Deeptanush (Tech Lead) · Task: T-101
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from invoice_api.api.v1.router import api_router
from invoice_api.core.config import Settings, get_settings
from invoice_api.core.errors import register_error_handlers
from invoice_api.core.security import build_verifier
from invoice_api.core.spa import mount_spa
from invoice_api.db.session import build_engine, build_session_factory
from invoice_api.storage.factory import build_blob_store


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    engine = build_engine(settings)

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        yield
        await engine.dispose()

    app = FastAPI(
        title=settings.app_name,
        version=settings.version,
        openapi_url="/api/v1/openapi.json",
        lifespan=lifespan,
    )
    app.state.engine = engine
    app.state.session_factory = build_session_factory(engine)
    app.state.blob_store = build_blob_store(settings)
    app.state.entra_verifier = build_verifier(settings)
    app.dependency_overrides[get_settings] = lambda: settings
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    register_error_handlers(app)
    app.include_router(api_router)
    mount_spa(app, settings.spa_dist_dir)
    return app
