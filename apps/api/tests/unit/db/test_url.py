from invoice_api.db.url import to_async_url

NEON = (
    "postgresql://user:secret@ep-x-pooler.c-6.us-east-2.aws.neon.tech/neondb"
    "?sslmode=require&channel_binding=require"
)


def test_neon_url_becomes_asyncpg_with_ssl_and_no_statement_cache() -> None:
    db = to_async_url(NEON)
    assert db.url.startswith("postgresql+asyncpg://user:secret@ep-x-pooler")
    assert "sslmode" not in db.url and "channel_binding" not in db.url
    assert "prepared_statement_cache_size=0" in db.url
    assert db.connect_args == {"ssl": "require", "statement_cache_size": 0}


def test_direct_postgres_url_keeps_statement_cache() -> None:
    db = to_async_url("postgresql://u:p@localhost:5432/invoice")
    assert db.url == "postgresql+asyncpg://u:p@localhost:5432/invoice"
    assert db.connect_args == {}


def test_sqlite_url_is_left_alone() -> None:
    assert to_async_url("sqlite+aiosqlite:///x.db").url == "sqlite+aiosqlite:///x.db"
