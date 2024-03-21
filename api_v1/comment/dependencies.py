from typing import Annotated

from fastapi import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from core.db_helper import db_helper
from core.models import Comment

from ..common.dependencies import get_item_by_id


async def get_comment_by_id(
    id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> Comment:
    return await get_item_by_id(
        id=id,
        session=session,
        model_item=Comment,
    )
