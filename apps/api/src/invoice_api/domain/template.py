"""GlobalTemplate and Section models (pure, no I/O).

Owner: Deeptanush (Tech Lead) · Task: T-104
"""

from functools import cached_property

from pydantic import BaseModel, ConfigDict, Field, model_validator

from invoice_api.domain.field_spec import FieldSpec


class Section(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str = Field(pattern=r"^[a-z][a-z0-9_]*$")
    fields: list[FieldSpec] = Field(min_length=1)


class GlobalTemplate(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    version: int = Field(ge=1)
    title: str
    sections: list[Section] = Field(min_length=1)

    @model_validator(mode="after")
    def _unique_ids(self) -> "GlobalTemplate":
        section_ids = [s.id for s in self.sections]
        field_ids = [f.id for s in self.sections for f in s.fields]
        for kind, ids in (("section", section_ids), ("field", field_ids)):
            duplicates = sorted({i for i in ids if ids.count(i) > 1})
            if duplicates:
                raise ValueError(f"duplicate {kind} ids: {', '.join(duplicates)}")
        return self

    @property
    def field_count(self) -> int:
        return len(self.ordered_fields)

    @cached_property
    def ordered_fields(self) -> tuple[FieldSpec, ...]:
        """Every field in template order: the order R-IDs and reports follow."""
        return tuple(f for s in self.sections for f in s.fields)

    @cached_property
    def _section_by_field(self) -> dict[str, str]:
        return {f.id: s.id for s in self.sections for f in s.fields}

    def field(self, field_id: str) -> FieldSpec:
        for spec in self.ordered_fields:
            if spec.id == field_id:
                return spec
        raise KeyError(field_id)

    def section_of(self, field_id: str) -> str:
        return self._section_by_field[field_id]
