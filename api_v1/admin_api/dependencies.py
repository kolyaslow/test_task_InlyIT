from typing import Annotated

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.db_helper import db_helper
from core.models import User

from ..auth.crud import get_user_by_user_name


async def get_user_by_id(
    user_name_new_admin: Annotated[str, Path],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> User:
    user = await get_user_by_user_name(
        user_name=user_name_new_admin,
        session=session,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user
