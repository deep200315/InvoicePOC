"""FieldSpec: one global template field (id, label, priority, format, expected value).

Owner: Deeptanush (Tech Lead) · Task: T-104
"""

from pydantic import BaseModel, ConfigDict, Field, field_validator

from invoice_api.domain.enums import Priority

FIELD_FORMATS = frozenset(
    {"text", "address", "code", "licence", "date_iso", "iso_4217", "decimal_2", "decimal_3"}
)
ENUM_PREFIX = "enum:"


class FieldSpec(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str = Field(pattern=r"^[a-z][a-z0-9_]*$")
    label: str = Field(min_length=1)
    priority: Priority
    format: str
    expected_value: str | None = None

    @field_validator("format")
    @classmethod
    def _known_format(cls, value: str) -> str:
        if value in FIELD_FORMATS:
            return value
        if value.startswith(ENUM_PREFIX) and len(value.removeprefix(ENUM_PREFIX).split("|")) >= 2:
            return value
        raise ValueError(f"unknown field format '{value}'")

    @property
    def enum_options(self) -> tuple[str, ...]:
        if not self.format.startswith(ENUM_PREFIX):
            return ()
        return tuple(self.format.removeprefix(ENUM_PREFIX).split("|"))
