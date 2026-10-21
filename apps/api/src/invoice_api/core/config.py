"""Settings via pydantic-settings, read from the environment and the repo-root .env.

Owner: Deeptanush (Tech Lead) · Task: T-101
"""

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

API_ROOT = Path(__file__).resolve().parents[3]
REPO_ROOT = API_ROOT.parents[1]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=(REPO_ROOT / ".env", API_ROOT / ".env"), extra="ignore")

    app_name: str = "Global Invoice Transformation API"
    version: str = "0.1.0"
    database_url: str = "sqlite+aiosqlite:///./local.db"

    auth_mode: Literal["dev", "entra"] = "dev"
    entra_tenant_id: str = ""
    entra_client_id: str = ""
    entra_audience: str = ""
    entra_allowed_group: str = ""

    blob_backend: Literal["local", "azure"] = "local"
    blob_local_dir: Path = API_ROOT / ".data" / "blobs"
    azure_storage_connection_string: str = ""
    azure_blob_container: str = "invoices"

    max_upload_mb: int = Field(default=20, gt=0)
    template_data_dir: Path = API_ROOT / "template_data"
    spa_dist_dir: Path = REPO_ROOT / "apps" / "web" / "dist"
    cors_origins: list[str] = ["http://localhost:5173"]

    @property
    def max_upload_bytes(self) -> int:
        return self.max_upload_mb * 1024 * 1024


@lru_cache
def get_settings() -> Settings:
    return Settings()
