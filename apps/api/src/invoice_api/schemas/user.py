"""Signed-in user DTO.

Owner: Deeptanush (Tech Lead) · Task: T-205
"""

from invoice_api.schemas.common import ApiModel


class UserOut(ApiModel):
    id: str
    email: str
    name: str
    roles: list[str]
