from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.db_helper import db_helper
from core.models import Announcement, User

from ..announcement.dependencies import get_announcement_by_id
from ..auth.security import access_rights
from . import crud as comment_crud
from .schemas import CreateComment

router = APIRouter(prefix="/comment", tags=["Comment"])


@router.post(
    "/create_comment/{id_announcement}",
    status_code=status.HTTP_201_CREATED,
)
async def create_comment(
    comment_data: CreateComment,
    announcement: Announcement = Depends(get_announcement_by_id),
    score: int | None = Query(ge=1, le=5, default=5),
    user: User = Depends(access_rights.verification_authorized_non_binary_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """
    Создание различных видов коментариев к объявлению(жалоба, отзыв и т.д.)

    :score : оценка заказа по пятибальной шкале
    """

    await comment_crud.create_comment(
        comment_data=comment_data,
        announcement=announcement,
        score=score,
        session=session,
        user_id=user.id,
    )
