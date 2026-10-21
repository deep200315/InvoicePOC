"""countries table.

Owner: Deeptanush (Tech Lead) · Task: T-102
"""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from invoice_api.db.base import Base


class Country(Base):
    __tablename__ = "countries"

    code: Mapped[str] = mapped_column(String(2), primary_key=True)
    name: Mapped[str] = mapped_column(String(80))
    in_scope: Mapped[bool] = mapped_column(default=True)
    sort_order: Mapped[int] = mapped_column(default=0)
