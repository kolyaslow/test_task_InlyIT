from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Text

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .announcement import Announcement


class Comment(Base):
    """
    Таблица для хранения коментариев

    type: тип коментария(жалоба, отзыв и т.д)
    user_id: id пользователя, оставившего комментарий
    announcement_id: id объявления, для которого написали комментарий
    """

    type: Mapped[str]
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"),
    )
    announcement_id: Mapped[int] = mapped_column(
        ForeignKey("announcement.id"),
    )
    text: Mapped[str] = mapped_column(Text)

    announcement: Mapped["Announcement"] = relationship(
        back_populates="comments",
    )
