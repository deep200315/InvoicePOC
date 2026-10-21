"""Shared Pydantic DTOs for the API contract.

Owner: Deeptanush (Tech Lead) · Task: T-103
"""

from pydantic import BaseModel, ConfigDict, Field


class ApiModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, frozen=True)


class ErrorBody(ApiModel):
    code: str = Field(examples=["NOT_FOUND"])
    message: str = Field(examples=["Comparison not found"])


class BBox(ApiModel):
    """Field position on a PDF page, in PDF points from the top-left corner."""

    x0: float
    y0: float
    x1: float
    y1: float
