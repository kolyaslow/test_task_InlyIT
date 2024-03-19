from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.db_helper import db_helper
from core.models import User

from . import crud as auth_crud
from .dependencies import check_unique_user_name, cookie_check, verification_user
from .schemas import AuthUser, ShowUser
from .utils import delete_cookies_and_their_cache, set_cookies_and_add_in_cache

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=ShowUser)
async def register_user(
    user_data: AuthUser = Depends(check_unique_user_name),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> ShowUser:
    """
    Регистрация пользователя с уникальным именем, при попытке ввода нецникально имени,
    выкидывается исключение c кодом 409.
    """
    return await auth_crud.create_user(
        user_data=user_data,
        session=session,
    )


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
)
async def login_user(
    response: Response,
    session_id: str | None = Depends(cookie_check),
    user: User = Depends(verification_user),
) -> str:
    """
    Вход в систему используя логин и пароль
    """
    return await set_cookies_and_add_in_cache(
        response=response,
        user_name=user.user_name,
        session_id=session_id,
    )


@router.post("logout", status_code=status.HTTP_200_OK)
async def logout_user(
    response: Response,
    session_id: str = Depends(cookie_check),
):
    await delete_cookies_and_their_cache(response=response, session_id=session_id)
