import bcrypt
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.auth.dependencies import cookie_check
from core.config import settings
from core.db_helper import db_helper
from core.models import User

from ..auth import crud as crud_auth


def hash_password(
    password: str,
) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


class AccessRights:

    _FORBIDDEN_EXCEPTION = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="ENTRY FORBIDDEN",
    )

    async def _get_authorized_user(
        self,
        cookie: str,
        session: AsyncSession,
    ) -> User:
        """
        Получение текущего пользователя по его cookie
        """
        redis_client = settings.redis.client_redis
        user_name_bytes = await redis_client.get(cookie)

        if not cookie or user_name_bytes is None:
            raise self._FORBIDDEN_EXCEPTION

        user_data: User = await crud_auth.get_user_by_user_name(
            user_name=user_name_bytes.decode(
                "utf-8"
            ),  # так как redis возвращает значение в bytes
            session=session,
        )
        return user_data

    async def verification_authorized_non_binary_user(
        self,
        cookie: str | None = Depends(cookie_check),
        session: AsyncSession = Depends(db_helper.session_dependency),
    ) -> User:
        if not cookie:
            raise self._FORBIDDEN_EXCEPTION

        user_data: User = await self._get_authorized_user(
            cookie=cookie,
            session=session,
        )

        if user_data.is_banned:
            raise self._FORBIDDEN_EXCEPTION

        return user_data

    async def checking_superuser(
        self,
        cookie: str | None = Depends(cookie_check),
        session: AsyncSession = Depends(db_helper.session_dependency),
    ):
        user_data: User = await self._get_authorized_user(
            cookie=cookie,
            session=session,
        )
        if not user_data.is_superuser:
            raise self._FORBIDDEN_EXCEPTION

        return user_data


access_rights = AccessRights()
