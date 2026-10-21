"""FastAPI app factory. Run with: uvicorn invoice_api.main:create_app --factory

Owner: Deeptanush (Tech Lead) · Task: T-101
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from invoice_api.api.v1.router import api_router
from invoice_api.core.config import Settings, get_settings
from invoice_api.core.errors import register_error_handlers
from invoice_api.core.spa import mount_spa


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    app = FastAPI(title=settings.app_name, version=settings.version, openapi_url="/api/v1/openapi.json")
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
