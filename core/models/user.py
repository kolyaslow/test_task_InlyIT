from typing import TYPE_CHECKING


from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .announcement import Announcement


class User(Base):
    """
    Таблица для храннеия данных о пользователе.

    user_name: уникальное имя пользователя
    password: пароль закешированный в ...
    is_superuser(необязательный): показатель что пользователь суперпользователь, значение по умолчанию False
    is_banned(необязательный): показатель, забанин ли пользователь, значение по умолчанию False
    """

    user_name: Mapped[str] = mapped_column(
        unique=True,
        index=True,
    )
    password: Mapped[str]
    is_superuser: Mapped[bool] = mapped_column(
        default=False,
    )
    is_banned: Mapped[bool] = mapped_column(
        default=False,
    )

    announcements: Mapped[list["Announcement"]] = relationship(
        back_populates="user",
    )
