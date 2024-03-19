import logging

from fastapi import Cookie, Depends, HTTPException, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.db_helper import db_helper
from core.models import User

from . import crud as auth_crud
from . import utils
from .constants import COOKIE_SESSION_ID_KEY
from .schemas import AuthUser

logging = logging.getLogger(__name__)


async def check_unique_user_name(
    user_data: AuthUser, session: AsyncSession = Depends(db_helper.session_dependency)
) -> AuthUser:
    if await auth_crud.get_user_by_user_name(
        user_name=user_data.user_name,
        session=session,
    ):
        logging.info(f"Re-creating a user with the name {user_data.user_name}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Such a user already exists"
        )

    return user_data


async def verification_user(
    user_data: AuthUser,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> User:
    """
    Проверка пользователя на совпадения логина и пароля и на то, что он не забанин
    """
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )

    user = await auth_crud.get_user_by_user_name(
        user_name=user_data.user_name,
        session=session,
    )

    if not user:
        raise unauthed_exc

    if not utils.validate_password(
        password=user_data.password,
        hashed_password=user.password,
    ):
        raise unauthed_exc

    if user.is_banned:
        logging.warning(f"Banned user {user.user_name} tried to log in")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user inactive",
        )
    return user


async def cookie_check(
    request: Request,
):
    return request.cookies.get(COOKIE_SESSION_ID_KEY)
