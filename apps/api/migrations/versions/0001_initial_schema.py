"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-10-21 10:28:49.261228
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:

    op.create_table(
        "audit_events",
        sa.Column("id", sa.BigInteger().with_variant(sa.Integer(), "sqlite"), nullable=False),
        sa.Column("at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("actor", sa.String(length=255), nullable=False),
        sa.Column("action", sa.String(length=64), nullable=False),
        sa.Column("entity_type", sa.String(length=32), nullable=True),
        sa.Column("entity_id", sa.String(length=64), nullable=True),
        sa.Column("ip", sa.String(length=64), nullable=True),
        sa.Column("detail", sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_audit_events")),
    )
    with op.batch_alter_table("audit_events", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_audit_events_at"), ["at"], unique=False)

    op.create_table(
        "countries",
        sa.Column("code", sa.String(length=2), nullable=False),
        sa.Column("name", sa.String(length=80), nullable=False),
        sa.Column("in_scope", sa.Boolean(), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("code", name=op.f("pk_countries")),
    )
    op.create_table(
        "templates",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("key", sa.String(length=64), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("checksum", sa.String(length=64), nullable=False),
        sa.Column("field_count", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_templates")),
        sa.UniqueConstraint("key", "version", name=op.f("uq_templates_key")),
    )
    op.create_table(
        "invoices",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("country_code", sa.String(length=2), nullable=False),
        sa.Column("filename", sa.String(length=255), nullable=False),
        sa.Column(
            "file_type", sa.Enum("pdf", "xlsx", name="filetype", native_enum=False, length=32), nullable=False
        ),
        sa.Column("size_bytes", sa.Integer(), nullable=False),
        sa.Column("sha256", sa.String(length=64), nullable=False),
        sa.Column("blob_key", sa.String(length=512), nullable=False),
        sa.Column("pages", sa.Integer(), nullable=True),
        sa.Column("uploaded_by", sa.String(length=255), nullable=False),
        sa.Column("uploaded_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["country_code"], ["countries.code"], name=op.f("fk_invoices_country_code_countries")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_invoices")),
    )
    with op.batch_alter_table("invoices", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_invoices_country_code"), ["country_code"], unique=False)
        batch_op.create_index(batch_op.f("ix_invoices_sha256"), ["sha256"], unique=False)

    op.create_table(
        "comparisons",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("country_code", sa.String(length=2), nullable=False),
        sa.Column("invoice_id", sa.Uuid(), nullable=False),
        sa.Column("template_key", sa.String(length=64), nullable=False),
        sa.Column("template_version", sa.Integer(), nullable=False),
        sa.Column(
            "status",
            sa.Enum(
                "pending",
                "running",
                "completed",
                "failed",
                name="comparisonstatus",
                native_enum=False,
                length=32,
            ),
            nullable=False,
        ),
        sa.Column("matched_count", sa.Integer(), nullable=True),
        sa.Column("total_count", sa.Integer(), nullable=True),
        sa.Column("error_code", sa.String(length=64), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_by", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["country_code"], ["countries.code"], name=op.f("fk_comparisons_country_code_countries")
        ),
        sa.ForeignKeyConstraint(
            ["invoice_id"], ["invoices.id"], name=op.f("fk_comparisons_invoice_id_invoices")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_comparisons")),
    )
    with op.batch_alter_table("comparisons", schema=None) as batch_op:
        batch_op.create_index("ix_comparisons_country_created", ["country_code", "created_at"], unique=False)

    op.create_table(
        "comparison_steps",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("comparison_id", sa.Uuid(), nullable=False),
        sa.Column(
            "name",
            sa.Enum(
                "validate", "extract", "map", "check", "build", name="stepname", native_enum=False, length=32
            ),
            nullable=False,
        ),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column(
            "status",
            sa.Enum("pending", "running", "done", "failed", name="stepstatus", native_enum=False, length=32),
            nullable=False,
        ),
        sa.Column("detail", sa.Text(), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["comparison_id"],
            ["comparisons.id"],
            name=op.f("fk_comparison_steps_comparison_id_comparisons"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_comparison_steps")),
        sa.UniqueConstraint("comparison_id", "name", name=op.f("uq_comparison_steps_comparison_id")),
    )
    op.create_table(
        "extracted_fields",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("comparison_id", sa.Uuid(), nullable=False),
        sa.Column("local_label", sa.Text(), nullable=True),
        sa.Column("local_value", sa.Text(), nullable=True),
        sa.Column("page", sa.Integer(), nullable=True),
        sa.Column("bbox", sa.JSON(), nullable=True),
        sa.Column("cell", sa.String(length=16), nullable=True),
        sa.Column("field_id", sa.String(length=64), nullable=True),
        sa.Column("matcher", sa.String(length=32), nullable=True),
        sa.Column("rule", sa.Text(), nullable=True),
        sa.Column("section_found", sa.String(length=32), nullable=True),
        sa.ForeignKeyConstraint(
            ["comparison_id"],
            ["comparisons.id"],
            name=op.f("fk_extracted_fields_comparison_id_comparisons"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_extracted_fields")),
    )
    with op.batch_alter_table("extracted_fields", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_extracted_fields_comparison_id"), ["comparison_id"], unique=False
        )

    op.create_table(
        "findings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("comparison_id", sa.Uuid(), nullable=False),
        sa.Column("requirement_id", sa.String(length=8), nullable=True),
        sa.Column("field_id", sa.String(length=64), nullable=False),
        sa.Column("section", sa.String(length=32), nullable=False),
        sa.Column(
            "check_type",
            sa.Enum(
                "presence",
                "value",
                "format",
                "label",
                "placement",
                name="checktype",
                native_enum=False,
                length=32,
            ),
            nullable=False,
        ),
        sa.Column(
            "requirement_type",
            sa.Enum(
                "missing_field",
                "missing_value",
                "invalid_value",
                "format",
                "label",
                "placement",
                name="requirementtype",
                native_enum=False,
                length=32,
            ),
            nullable=False,
        ),
        sa.Column(
            "priority",
            sa.Enum(
                "mandatory", "standard", "advisory", "tbc", name="priority", native_enum=False, length=32
            ),
            nullable=False,
        ),
        sa.Column("current", sa.Text(), nullable=True),
        sa.Column("expected", sa.Text(), nullable=False),
        sa.Column(
            "result",
            sa.Enum("match", "missing", "invalid", "different", name="outcome", native_enum=False, length=32),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["comparison_id"],
            ["comparisons.id"],
            name=op.f("fk_findings_comparison_id_comparisons"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_findings")),
    )
    with op.batch_alter_table("findings", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_findings_comparison_id"), ["comparison_id"], unique=False)


def downgrade() -> None:

    with op.batch_alter_table("findings", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_findings_comparison_id"))

    op.drop_table("findings")
    with op.batch_alter_table("extracted_fields", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_extracted_fields_comparison_id"))

    op.drop_table("extracted_fields")
    op.drop_table("comparison_steps")
    with op.batch_alter_table("comparisons", schema=None) as batch_op:
        batch_op.drop_index("ix_comparisons_country_created")

    op.drop_table("comparisons")
    with op.batch_alter_table("invoices", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_invoices_sha256"))
        batch_op.drop_index(batch_op.f("ix_invoices_country_code"))

    op.drop_table("invoices")
    op.drop_table("templates")
    op.drop_table("countries")
    with op.batch_alter_table("audit_events", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_audit_events_at"))

    op.drop_table("audit_events")
