from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.db_helper import db_helper
from core.models import Announcement, User

from ..auth.security import access_rights
from . import crud as announcement_crud
from .dependencies import get_announcement_by_id
from .schemas import CreateAnnouncement, ShowAnnouncement, TypeAnnouncement

router = APIRouter(prefix="/announcement", tags=["Announcement"])


@router.post(
    "/create_announcement",
    response_model=ShowAnnouncement,
)
async def create_announcement(
    announcement_data: CreateAnnouncement,
    session: AsyncSession = Depends(db_helper.session_dependency),
    user: User = Depends(access_rights.verification_authorized_non_binary_user),
) -> Announcement:
    """
    Создание обявления, можно создать одинаковые обявоения.
    Исключение вызовится только при ошибки валидации или если
    пользователь не имеет права доступа.
    """
    return await announcement_crud.create_announcement(
        session=session,
        announcement_data=announcement_data,
        user_id=user.id,
    )


@router.get(
    "/show_not_user_ads",
    response_model=list[ShowAnnouncement],
)
async def show_not_user_ads(
    type: TypeAnnouncement | None = None,
    page: int = Query(ge=0, default=0),
    size: int = Query(ge=1, le=100, default=10),
    session: AsyncSession = Depends(db_helper.session_dependency),
    user: User = Depends(access_rights.verification_authorized_non_binary_user),
) -> list[Announcement]:
    """
    Получить список объявлений, которые выставили другие пользователи.
    если указать type, вернустя только обяевления оперделенного типа

    - type - при указании типа обявления, вернустя только обяевления этого типа
    - page - страница пагинации, значение не может быть меньше 0
    - size - выдаемый за раз объем информации, максимально 100 минимально 1
    """
    return await announcement_crud.get_not_user_ads(
        type=type,
        page=page,
        size=size,
        session=session,
        user_id=user.id,
    )


@router.get(
    "/show_one_announcement_by_id/{id_announcement}",
    dependencies=[Depends(access_rights.verification_authorized_non_binary_user)],
    response_model=ShowAnnouncement,
)
async def show_one_announcement_by_id(
    announcement: Announcement = Depends(get_announcement_by_id),
) -> Announcement:
    """
    Получение объявления по id, если такого объявления нет, вернет 404
    """
    return announcement


@router.delete(
    "/delete_announcement/{id_announcement}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_announcement(
    delete_data: Announcement = Depends(get_announcement_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
    user: User = Depends(access_rights.verification_authorized_non_binary_user),
):
    """
    Удаление только своего объявления, при удалении несуществующего объявления выкидывается исключение 404.
    """
    if user.id != delete_data.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Attempting to delete an ad that is not your own",
        )

    await announcement_crud.delete_announcement(
        delete_data=delete_data,
        session=session,
    )
