"""Loads and validates the global template YAML from template_data/, with its checksum.

Owner: Deeptanush (Tech Lead) · Task: T-104
"""

import hashlib
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import yaml

from invoice_api.domain.template import GlobalTemplate

GLOBAL_TEMPLATE_FILE = Path("global") / "proforma_v1.yaml"


@dataclass(frozen=True)
class LoadedTemplate:
    template: GlobalTemplate
    checksum: str


@lru_cache(maxsize=8)
def load_template_file(path: Path) -> LoadedTemplate:
    raw = path.read_bytes()
    template = GlobalTemplate.model_validate(yaml.safe_load(raw))
    return LoadedTemplate(template=template, checksum=hashlib.sha256(raw).hexdigest())


def load_global_template(template_data_dir: Path) -> LoadedTemplate:
    return load_template_file((template_data_dir / GLOBAL_TEMPLATE_FILE).resolve())
