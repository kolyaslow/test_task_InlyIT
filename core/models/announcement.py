from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User
    from .comment import Comment


class Announcement(Base):
    """
    Таблица для храннеия данных о объявлении

    type: тип объявления(продажа, покупка, услуга и т.д.)
    description: описание объявления
    rating: рейтинг объявления, принадлежит значениям от 5 до 0 включительно
    """

    type: Mapped[str]
    description: Mapped[str]
    rating: Mapped[float] = mapped_column(
        default=5,
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    user: Mapped["User"] = relationship(
        back_populates="announcements",
    )

    comments: Mapped[list["Comment"]] = relationship(
        back_populates="announcement",
    )
