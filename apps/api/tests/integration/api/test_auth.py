import time
from typing import Any

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi import FastAPI
from httpx import AsyncClient

from invoice_api.core.security import EntraVerifier

TENANT, AUDIENCE, GROUP = "tenant-1", "api://invoice", "pilot-users"
KEY = rsa.generate_private_key(public_exponent=65537, key_size=2048)


def _token(**overrides: Any) -> str:
    claims = {
        "iss": f"https://login.microsoftonline.com/{TENANT}/v2.0",
        "aud": AUDIENCE,
        "exp": int(time.time()) + 300,
        "oid": "u-42",
        "preferred_username": "kuhu@example.com",
        "name": "Kuhu",
        "groups": [GROUP],
    } | overrides
    return jwt.encode(claims, KEY, algorithm="RS256")


@pytest.fixture
def entra_app(app: FastAPI) -> FastAPI:
    app.state.entra_verifier = EntraVerifier(TENANT, AUDIENCE, GROUP, key_resolver=lambda _: KEY.public_key())
    return app


async def test_dev_mode_uses_header_user(client: AsyncClient) -> None:
    response = await client.get("/api/v1/me", headers={"X-Dev-User": "WW12345"})
    assert response.json() == {
        "id": "WW12345",
        "email": "WW12345@dev.local",
        "name": "WW12345",
        "roles": ["dev"],
    }


async def test_entra_valid_token(entra_app: FastAPI, client: AsyncClient) -> None:
    response = await client.get("/api/v1/me", headers={"Authorization": f"Bearer {_token()}"})
    assert response.status_code == 200
    assert response.json()["email"] == "kuhu@example.com"


@pytest.mark.parametrize(
    ("headers", "status", "code"),
    [
        ({}, 401, "UNAUTHORIZED"),
        ({"Authorization": "Bearer not-a-jwt"}, 401, "UNAUTHORIZED"),
        ({"Authorization": f"Bearer {_token(aud='api://other')}"}, 401, "UNAUTHORIZED"),
        ({"Authorization": f"Bearer {_token(exp=int(time.time()) - 10)}"}, 401, "UNAUTHORIZED"),
        ({"Authorization": f"Bearer {_token(groups=['someone-else'])}"}, 403, "FORBIDDEN"),
    ],
)
async def test_entra_rejects_bad_requests(
    entra_app: FastAPI, client: AsyncClient, headers: dict[str, str], status: int, code: str
) -> None:
    response = await client.get("/api/v1/me", headers=headers)
    assert response.status_code == status
    assert response.json()["code"] == code


async def test_health_stays_public(entra_app: FastAPI, client: AsyncClient) -> None:
    assert (await client.get("/api/v1/health")).status_code == 200
