from pathlib import Path

import pytest

from invoice_api.storage.base import BlobNotFoundError, InvalidBlobKeyError
from invoice_api.storage.local_store import LocalBlobStore


async def test_put_get_delete_round_trip(tmp_path: Path) -> None:
    store = LocalBlobStore(tmp_path)
    await store.put("invoices/abc/RO.pdf", b"%PDF-1.7", "application/pdf")
    assert await store.get("invoices/abc/RO.pdf") == b"%PDF-1.7"
    assert await store.signed_url("invoices/abc/RO.pdf") is None
    await store.delete("invoices/abc/RO.pdf")
    await store.delete("invoices/abc/RO.pdf")
    with pytest.raises(BlobNotFoundError):
        await store.get("invoices/abc/RO.pdf")


@pytest.mark.parametrize("key", ["", "/etc/passwd", "../x", "a/../../x", "a//b"])
async def test_unsafe_keys_are_rejected(tmp_path: Path, key: str) -> None:
    with pytest.raises(InvalidBlobKeyError):
        await LocalBlobStore(tmp_path).put(key, b"x", "text/plain")
