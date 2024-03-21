from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.db_helper import db_helper
from core.models import Comment, User

from ..auth.security import access_rights
from ..comment.dependencies import get_comment_by_id
from ..common import crud as common_crud
from . import crud as admin_crud
from .dependencies import get_user_by_id

router = APIRouter(prefix="/admin", tags=["admin"])


@router.patch(
    "/set_user_an_admin/{user_name_new_admin}",
    dependencies=[Depends(access_rights.checking_superuser)],
    status_code=status.HTTP_200_OK,
)
async def set_user_an_admin(
    new_admin_data: User = Depends(get_user_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    await admin_crud.set_user_an_admin(new_admin_data=new_admin_data, session=session)


@router.delete(
    "/delete_comment/{id_comment}",
    dependencies=[Depends(access_rights.checking_superuser)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_comment(
    comment: Comment = Depends(get_comment_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    await common_crud.delete_db_item(
        session=session,
        delete_item=comment,
    )
