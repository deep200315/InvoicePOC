"""Report DTOs. The report itself is returned as an .xlsx download.

Owner: Deeptanush (Tech Lead) · Task: T-103
"""

from enum import StrEnum


class ReportKind(StrEnum):
    GAP = "gap"
    MATCH = "match"
