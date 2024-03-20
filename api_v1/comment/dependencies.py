from typing import Annotated

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.db_helper import db_helper
from core.models import Comment

from ..comment import crud as comment_crud


async def get_comment_by_id(
    id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> Comment:
    comment = await comment_crud.get_comment_by_id(
        id=id,
        session=session,
    )

    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )

    return comment
