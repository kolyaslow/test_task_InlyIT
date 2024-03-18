import logging
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(filename)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

loger = logging.getLogger(__name__)


class BaseSettingsApp(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent / ".env",
        extra="ignore",
    )


class DbSettings(BaseSettingsApp):

    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    echo: bool = False

    @property
    def url(self):
        url: str = (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
        loger.debug(f"url бд: {url}")
        return url


class RedisSettings(BaseSettingsApp):
    REDIS_HOST: str
    REDIS_PORT: str


class Settings(BaseSettings):
    db: DbSettings = DbSettings()
    redis: RedisSettings = RedisSettings()


settings = Settings()
