"""Enums shared by the domain, the database and the API contract.

Owner: Deeptanush (Tech Lead) · Task: T-103
"""

from enum import StrEnum


class Priority(StrEnum):
    MANDATORY = "mandatory"
    STANDARD = "standard"
    ADVISORY = "advisory"
    TBC = "tbc"


class CheckType(StrEnum):
    PRESENCE = "presence"
    VALUE = "value"
    FORMAT = "format"
    LABEL = "label"
    PLACEMENT = "placement"


class RequirementType(StrEnum):
    MISSING_FIELD = "missing_field"
    MISSING_VALUE = "missing_value"
    INVALID_VALUE = "invalid_value"
    FORMAT = "format"
    LABEL = "label"
    PLACEMENT = "placement"


class Outcome(StrEnum):
    MATCH = "match"
    MISSING = "missing"
    INVALID = "invalid"
    DIFFERENT = "different"


class Verdict(StrEnum):
    MATCHES = "matches"
    DOESNT_MATCH = "doesnt_match"


class ComparisonStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class StepName(StrEnum):
    VALIDATE = "validate"
    EXTRACT = "extract"
    MAP = "map"
    CHECK = "check"
    BUILD = "build"


class StepStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    DONE = "done"
    FAILED = "failed"


class FileType(StrEnum):
    PDF = "pdf"
    XLSX = "xlsx"


PIPELINE_ORDER: tuple[StepName, ...] = (
    StepName.VALIDATE,
    StepName.EXTRACT,
    StepName.MAP,
    StepName.CHECK,
    StepName.BUILD,
)
