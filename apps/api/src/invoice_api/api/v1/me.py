"""GET /me - the signed-in user.

Owner: Deeptanush (Tech Lead) · Task: T-205
"""

from fastapi import APIRouter

from invoice_api.core.deps import CurrentUserDep
from invoice_api.schemas.user import UserOut

router = APIRouter(tags=["auth"])


@router.get("/me")
async def me(user: CurrentUserDep) -> UserOut:
    return UserOut(id=user.id, email=user.email, name=user.name, roles=list(user.roles))
