from enum import Enum

from pydantic import BaseModel, confloat


class TypeAnnouncement(str, Enum):
    sale = "продажа"
    purchase = "покупка"


class BaseAnnouncement(BaseModel):
    type: TypeAnnouncement
    description: str
    # ограничение рейтинга числами от 0 до 5
    rating: confloat(ge=0, le=5)


class CreateAnnouncement(BaseAnnouncement):
    pass


class ShowAnnouncement(BaseAnnouncement):
    user_id: int
