from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Announcement

from .schemas import CreateAnnouncement


async def create_announcement(
    session: AsyncSession,
    announcement_data: CreateAnnouncement,
    user_id: int,
) -> Announcement:
    announcement = Announcement(user_id=user_id, **announcement_data.model_dump())
    session.add(announcement)
    await session.commit()
    return announcement


async def get_not_user_ads(
    type: str | None,
    session: AsyncSession,
    user_id: int,
    page: int,
    size: int,
) -> list[Announcement] | list[None]:
    """
    Получение всех обявлений, которые не выставял пользователь
    """

    offset_min = page * size
    offset_max = (page + 1) * size

    # объевления которые не выставлял пользователь
    filter = Announcement.user_id != user_id
    if type:
        # объявления определенного типа
        filter = filter & (Announcement.type == type)

    stmt = (
        select(Announcement)
        .filter(filter)
        .offset(offset_min)
        .limit(offset_max - offset_min + 1)
    )

    announcements = await session.scalars(stmt)

    return list(announcements)
