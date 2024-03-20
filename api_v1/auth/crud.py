import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User

from .schemas import AuthUser, ShowUser
from .security import hash_password

logger = logging.getLogger(__name__)


async def get_user_by_user_name(
    user_name: str,
    session: AsyncSession,
) -> User:
    stmt = select(User).where(User.user_name == user_name)
    return await session.scalar(stmt)


async def create_user(
    user_data: AuthUser,
    session: AsyncSession,
) -> ShowUser:
    """
    Создание пользователя в БД, с кешированным паролем.
    Возвращает пользователя без пароля.
    """
    user_data.password = hash_password(user_data.password)
    user = User(**user_data.model_dump())
    session.add(user)
    await session.commit()
    logger.debug(f"User: {user.user_name} created")
    return ShowUser(
        user_name=user.user_name,
        is_superuser=user.is_superuser,
        is_banned=user.is_banned,
    )
