from typing import Annotated

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.db_helper import db_helper
from core.models import Announcement

from . import crud as announcement_crud


async def get_announcement_by_id(
    id_announcement: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> Announcement:
    """
    Получения экземпляра модели Announcement по его id
    """
    announcement = await announcement_crud.get_announcement_by_id(
        id=id_announcement,
        session=session,
    )

    if not announcement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Ad by id not found"
        )

    return announcement
