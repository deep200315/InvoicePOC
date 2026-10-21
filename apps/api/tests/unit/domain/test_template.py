from typing import Any

import pytest
import yaml
from pydantic import ValidationError

from invoice_api.core.config import API_ROOT
from invoice_api.domain.enums import Priority
from invoice_api.domain.template import GlobalTemplate
from invoice_api.services.template_service import GLOBAL_TEMPLATE_FILE, load_global_template

TEMPLATE_DATA = API_ROOT / "template_data"


def _raw() -> dict[str, Any]:
    data: dict[str, Any] = yaml.safe_load((TEMPLATE_DATA / GLOBAL_TEMPLATE_FILE).read_text())
    return data


def test_global_template_has_31_fields_in_five_sections() -> None:
    loaded = load_global_template(TEMPLATE_DATA)
    t = loaded.template
    assert t.field_count == 31
    assert [(s.id, len(s.fields)) for s in t.sections] == [
        ("header", 6),
        ("parties", 8),
        ("licences", 2),
        ("order", 4),
        ("line_items", 11),
    ]
    assert len(loaded.checksum) == 64


def test_lookup_by_field_id() -> None:
    t = load_global_template(TEMPLATE_DATA).template
    assert t.field("currency").priority is Priority.MANDATORY
    assert t.section_of("remit_to") == "parties"
    assert t.field("copy_status").enum_options == ("Original", "Copy")
    with pytest.raises(KeyError):
        t.field("nope")


def test_duplicate_field_id_is_rejected() -> None:
    raw = _raw()
    raw["sections"][1]["fields"].append(raw["sections"][0]["fields"][0])
    with pytest.raises(ValidationError, match="duplicate field ids: document_title"):
        GlobalTemplate.model_validate(raw)


@pytest.mark.parametrize(
    ("key", "value"), [("priority", "urgent"), ("format", "date_us"), ("format", "enum:One")]
)
def test_unknown_priority_or_format_is_rejected(key: str, value: str) -> None:
    raw = _raw()
    raw["sections"][0]["fields"][0][key] = value
    with pytest.raises(ValidationError):
        GlobalTemplate.model_validate(raw)


def test_loader_is_cached() -> None:
    assert load_global_template(TEMPLATE_DATA) is load_global_template(TEMPLATE_DATA)
