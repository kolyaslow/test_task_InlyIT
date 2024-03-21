from typing import Annotated

from fastapi import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from core.db_helper import db_helper
from core.models import Announcement

from ..common.dependencies import get_item_by_id


async def get_announcement_by_id(
    id_announcement: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> Announcement:
    """
    Получения экземпляра модели Announcement по его id
    """
    return await get_item_by_id(
        id=id_announcement,
        session=session,
        model_item=Announcement,
    )
