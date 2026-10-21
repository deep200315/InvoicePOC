"""BlobStore on Azure Blob Storage: private container, short-lived SAS download links.

Owner: Deeptanush (Tech Lead) · Task: T-201
"""

import asyncio
from datetime import UTC, datetime, timedelta

from azure.core.exceptions import ResourceNotFoundError
from azure.storage.blob import BlobSasPermissions, BlobServiceClient, ContentSettings, generate_blob_sas

from invoice_api.storage.base import DEFAULT_LINK_TTL, BlobNotFoundError, check_key


class AzureBlobStore:
    def __init__(self, connection_string: str, container: str) -> None:
        self._service = BlobServiceClient.from_connection_string(connection_string)
        self._container = self._service.get_container_client(container)
        self._container_name = container

    async def put(self, key: str, data: bytes, content_type: str) -> None:
        blob = self._container.get_blob_client(check_key(key))
        settings = ContentSettings(content_type=content_type)
        await asyncio.to_thread(blob.upload_blob, data, overwrite=True, content_settings=settings)

    async def get(self, key: str) -> bytes:
        blob = self._container.get_blob_client(check_key(key))
        try:
            downloader = await asyncio.to_thread(blob.download_blob)
        except ResourceNotFoundError as exc:
            raise BlobNotFoundError(f"Blob not found: {key}") from exc
        return await asyncio.to_thread(downloader.readall)

    async def signed_url(self, key: str, expires_in: timedelta = DEFAULT_LINK_TTL) -> str | None:
        account_key = self._service.credential.account_key
        sas = generate_blob_sas(
            account_name=self._service.account_name or "",
            container_name=self._container_name,
            blob_name=check_key(key),
            account_key=account_key,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.now(UTC) + expires_in,
        )
        return f"{self._container.get_blob_client(key).url}?{sas}"

    async def delete(self, key: str) -> None:
        blob = self._container.get_blob_client(check_key(key))
        try:
            await asyncio.to_thread(blob.delete_blob)
        except ResourceNotFoundError:
            return
