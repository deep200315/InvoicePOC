"""Turns a plain Postgres URL (e.g. Neon's) into SQLAlchemy asyncpg URL + connect args.

Owner: Deeptanush (Tech Lead) · Task: T-102
"""

from dataclasses import dataclass, field

from sqlalchemy.engine import make_url

_SYNC_POSTGRES = {"postgres", "postgresql", "postgresql+psycopg2", "postgresql+psycopg"}


@dataclass(frozen=True)
class AsyncDbUrl:
    url: str
    connect_args: dict[str, object] = field(default_factory=dict)


def to_async_url(raw: str) -> AsyncDbUrl:
    parsed = make_url(raw)
    if parsed.drivername in _SYNC_POSTGRES:
        parsed = parsed.set(drivername="postgresql+asyncpg")
    if parsed.drivername != "postgresql+asyncpg":
        return AsyncDbUrl(parsed.render_as_string(hide_password=False))

    query = dict(parsed.query)
    sslmode = query.pop("sslmode", None)
    query.pop("channel_binding", None)
    connect_args: dict[str, object] = {}
    if sslmode and sslmode != "disable":
        connect_args["ssl"] = "require"
    if parsed.host and "-pooler" in parsed.host:
        connect_args["statement_cache_size"] = 0
        query["prepared_statement_cache_size"] = "0"
    parsed = parsed.set(query=query)
    return AsyncDbUrl(parsed.render_as_string(hide_password=False), connect_args)
