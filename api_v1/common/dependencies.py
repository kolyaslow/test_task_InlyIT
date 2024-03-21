from typing import Type

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Base

from . import crud as common_crud


async def get_item_by_id(
    id: int,
    session: AsyncSession,
    model_item: Type[Base],
):
    # олучение данных из БД
    item = await common_crud.get_item_by_id(
        id_item=id, session=session, model_item=model_item
    )

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item by id not found "
        )

    return item
