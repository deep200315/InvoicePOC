from pathlib import Path

from alembic import command
from alembic.config import Config

API_ROOT = Path(__file__).resolve().parents[3]


def _config(db_path: Path) -> Config:
    cfg = Config(str(API_ROOT / "alembic.ini"))
    cfg.set_main_option("script_location", str(API_ROOT / "migrations"))
    cfg.attributes["database_url"] = f"sqlite+aiosqlite:///{db_path}"
    return cfg


def test_upgrade_matches_models_and_downgrades(tmp_path: Path) -> None:
    cfg = _config(tmp_path / "migrate.db")
    command.upgrade(cfg, "head")
    command.check(cfg)
    command.downgrade(cfg, "base")
