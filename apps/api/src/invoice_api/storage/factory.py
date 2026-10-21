"""Builds the BlobStore named by settings.blob_backend.

Owner: Deeptanush (Tech Lead) · Task: T-201
"""

from invoice_api.core.config import Settings
from invoice_api.storage.base import BlobStore


def build_blob_store(settings: Settings) -> BlobStore:
    if settings.blob_backend == "azure":
        from invoice_api.storage.azure_blob_store import AzureBlobStore

        return AzureBlobStore(settings.azure_storage_connection_string, settings.azure_blob_container)
    from invoice_api.storage.local_store import LocalBlobStore

    return LocalBlobStore(settings.blob_local_dir)
