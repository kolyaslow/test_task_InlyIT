import uuid

import bcrypt
from fastapi import Response

from core.config import settings

from .constants import COOKIE_SESSION_ID_KEY
from .redis import delete_cache_user_cookie, remember_user_cookie


def hash_password(
    password: str,
) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(
    password: str,
    hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )


def generate_session_id() -> str:
    return uuid.uuid4().hex


def set_cookies(
    response: Response,
) -> str:
    session_id = generate_session_id()

    response.set_cookie(
        COOKIE_SESSION_ID_KEY,
        session_id,
    )

    return session_id


async def set_cookies_and_add_in_cache(
    response: Response,
    user_name: str,
    session_id: str,
):
    """
    Установка куки если пользователь еще не залогинился и кеширование
    куки и имени пользователя
    """
    redis_client = settings.redis.client_redis

    if session_id and await redis_client.get(session_id):
        return session_id

    cookie = set_cookies(response=response)

    await remember_user_cookie(
        cookie=cookie, user_name=user_name, redis_client=redis_client
    )

    return cookie


async def delete_cookies_and_their_cache(
    session_id: str,
    response: Response,
):
    if not session_id:
        return None
    await delete_cache_user_cookie(cookie=session_id)
    response.delete_cookie(COOKIE_SESSION_ID_KEY)
