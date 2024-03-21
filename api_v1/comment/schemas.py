from enum import Enum

from pydantic import BaseModel


class TypeComment(str, Enum):
    complaint = "жалоба"
    comment = "коментарий"
    feedback = "отзыв"


class BaseComment(BaseModel):
    type: TypeComment = TypeComment.comment
    # announcement_id: int
    text: str


class CreateComment(BaseComment):
    pass


class ShowComment(BaseComment):
    id: int
