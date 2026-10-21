"""BlobStore protocol: put, get, signed_url, delete. Keys look like 'invoices/<id>/<file>'.

Owner: Deeptanush (Tech Lead) · Task: T-201
"""

from datetime import timedelta
from typing import Protocol

from invoice_api.core.errors import NotFoundError

DEFAULT_LINK_TTL = timedelta(minutes=10)


class BlobNotFoundError(NotFoundError):
    code = "BLOB_NOT_FOUND"


class InvalidBlobKeyError(ValueError):
    pass


class BlobStore(Protocol):
    async def put(self, key: str, data: bytes, content_type: str) -> None: ...

    async def get(self, key: str) -> bytes: ...

    async def signed_url(self, key: str, expires_in: timedelta = DEFAULT_LINK_TTL) -> str | None:
        """A short-lived download link, or None when files are served through the API."""
        ...

    async def delete(self, key: str) -> None: ...


def check_key(key: str) -> str:
    parts = key.split("/")
    if not key or key.startswith("/") or any(p in ("", ".", "..") for p in parts):
        raise InvalidBlobKeyError(f"invalid blob key: {key!r}")
    return key
