"""Serves the built React app from FastAPI, falling back to index.html for client routes.

Owner: Deeptanush (Tech Lead) · Task: T-101
"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException
from starlette.responses import Response
from starlette.types import Scope


class SpaStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope: Scope) -> Response:
        try:
            return await super().get_response(path, scope)
        except HTTPException as exc:
            if exc.status_code != 404 or path.startswith("api/"):
                raise
            return await super().get_response("index.html", scope)


def mount_spa(app: FastAPI, dist_dir: Path) -> None:
    if (dist_dir / "index.html").is_file():
        app.mount("/", SpaStaticFiles(directory=dist_dir, html=True), name="spa")
