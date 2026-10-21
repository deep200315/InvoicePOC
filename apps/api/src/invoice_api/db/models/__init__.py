"""Imports every model so Base.metadata (and Alembic) sees all tables."""

from invoice_api.db.models.audit_event import AuditEvent
from invoice_api.db.models.comparison import Comparison
from invoice_api.db.models.comparison_step import ComparisonStep
from invoice_api.db.models.country import Country
from invoice_api.db.models.extracted_field import ExtractedFieldRecord
from invoice_api.db.models.finding import FindingRecord
from invoice_api.db.models.invoice import Invoice
from invoice_api.db.models.template import TemplateRecord

__all__ = [
    "AuditEvent",
    "Comparison",
    "ComparisonStep",
    "Country",
    "ExtractedFieldRecord",
    "FindingRecord",
    "Invoice",
    "TemplateRecord",
]
