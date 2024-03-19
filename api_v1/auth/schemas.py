from pydantic import BaseModel, Field


class BaseAuthUserData(BaseModel):
    user_name: str


class AuthUser(BaseAuthUserData):
    password: str = Field(
        min_length=6,
        max_length=50,
    )


class ShowUser(BaseAuthUserData):
    is_superuser: bool
    is_banned: bool
