from core.config import settings

from .constants import LIFE_CPAN_COOKIE_CACHE


async def remember_user_cookie(
    redis_client,
    cookie: str,
    user_name: str,
):
    """
    Занесение даных в redis:
    key: куки пользователя
    value: имя пользователя
    """

    await redis_client.set(cookie, user_name, ex=LIFE_CPAN_COOKIE_CACHE)


async def delete_cache_user_cookie(
    cookie: str,
):
    redis_client = settings.redis.client_redis
    await redis_client.delete(cookie)
