"""Who is calling: Entra ID JWT validation, or a dev sign-in header when AUTH_MODE=dev.

Owner: Deeptanush (Tech Lead) · Task: T-205
"""

import asyncio
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

import jwt
from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from invoice_api.core.config import Settings
from invoice_api.core.errors import ForbiddenError, UnauthorizedError

DEV_USER_HEADER = "X-Dev-User"
DEFAULT_DEV_USER = "dev.user@local"
bearer_scheme = HTTPBearer(auto_error=False)

KeyResolver = Callable[[str], Any]


@dataclass(frozen=True)
class CurrentUser:
    id: str
    email: str
    name: str
    roles: tuple[str, ...]


def dev_user(header_value: str | None) -> CurrentUser:
    value = (header_value or DEFAULT_DEV_USER).strip()
    email = value if "@" in value else f"{value}@dev.local"
    return CurrentUser(id=value, email=email, name=value, roles=("dev",))


class EntraVerifier:
    def __init__(
        self, tenant_id: str, audience: str, allowed_group: str = "", key_resolver: KeyResolver | None = None
    ) -> None:
        self.issuer = f"https://login.microsoftonline.com/{tenant_id}/v2.0"
        self.audience = audience
        self.allowed_group = allowed_group
        if key_resolver is None:
            jwks = jwt.PyJWKClient(f"https://login.microsoftonline.com/{tenant_id}/discovery/v2.0/keys")
            key_resolver = lambda token: jwks.get_signing_key_from_jwt(token).key  # noqa: E731
        self._resolve_key = key_resolver

    async def verify(self, token: str) -> CurrentUser:
        try:
            key = await asyncio.to_thread(self._resolve_key, token)
            claims = jwt.decode(token, key, algorithms=["RS256"], audience=self.audience, issuer=self.issuer)
        except (jwt.InvalidTokenError, jwt.PyJWKClientError) as exc:
            raise UnauthorizedError("Invalid or expired sign-in token.") from exc
        if self.allowed_group and self.allowed_group not in claims.get("groups", []):
            raise ForbiddenError("You are not in the pilot user group.")
        email = str(claims.get("preferred_username") or claims.get("email") or "")
        return CurrentUser(
            id=str(claims["oid"]),
            email=email,
            name=str(claims.get("name") or email),
            roles=tuple(claims.get("roles", [])),
        )


def build_verifier(settings: Settings) -> EntraVerifier | None:
    if settings.auth_mode != "entra":
        return None
    audience = settings.entra_audience or settings.entra_client_id
    return EntraVerifier(settings.entra_tenant_id, audience, settings.entra_allowed_group)


async def authenticate(
    request: Request, credentials: HTTPAuthorizationCredentials | None
) -> CurrentUser:
    verifier: EntraVerifier | None = request.app.state.entra_verifier
    if verifier is None:
        return dev_user(request.headers.get(DEV_USER_HEADER))
    if credentials is None:
        raise UnauthorizedError("Sign in required.")
    return await verifier.verify(credentials.credentials)
