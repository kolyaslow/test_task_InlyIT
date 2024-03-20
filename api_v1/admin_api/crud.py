from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User


async def set_user_an_admin(
    new_admin_data: User,
    session: AsyncSession,
):
    new_admin_data.is_superuser = True
    await session.commit()
