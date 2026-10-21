"""BlobStore on a mounted volume (local dev / pilot fallback).

Owner: Deeptanush (Tech Lead) · Task: T-201
"""

import asyncio
from datetime import timedelta
from pathlib import Path

from invoice_api.storage.base import DEFAULT_LINK_TTL, BlobNotFoundError, InvalidBlobKeyError, check_key


class LocalBlobStore:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()

    def _path(self, key: str) -> Path:
        path = (self.root / check_key(key)).resolve()
        if not path.is_relative_to(self.root):
            raise InvalidBlobKeyError(f"blob key escapes the store: {key!r}")
        return path

    async def put(self, key: str, data: bytes, content_type: str) -> None:
        path = self._path(key)
        path.parent.mkdir(parents=True, exist_ok=True)
        await asyncio.to_thread(path.write_bytes, data)

    async def get(self, key: str) -> bytes:
        path = self._path(key)
        if not path.is_file():
            raise BlobNotFoundError(f"Blob not found: {key}")
        return await asyncio.to_thread(path.read_bytes)

    async def signed_url(self, key: str, expires_in: timedelta = DEFAULT_LINK_TTL) -> str | None:
        return None

    async def delete(self, key: str) -> None:
        self._path(key).unlink(missing_ok=True)
