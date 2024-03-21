from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Base


async def get_item_by_id(
    session: AsyncSession,
    id_item: int,
    model_item: Type[Base],
):
    """Получение объекта БД по его id"""
    return await session.get(model_item, id_item)


async def delete_db_item(
    session: AsyncSession,
    delete_item: Base,
):
    """Удаление объекта из таблици БД"""
    await session.delete(delete_item)
    await session.commit()
