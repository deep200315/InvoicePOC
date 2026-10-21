"""Shared FastAPI dependencies: settings, DB session, current user, blob store.

Owner: Deeptanush (Tech Lead) · Task: T-101
"""

from typing import Annotated

from fastapi import Depends

from invoice_api.core.config import Settings, get_settings

SettingsDep = Annotated[Settings, Depends(get_settings)]
