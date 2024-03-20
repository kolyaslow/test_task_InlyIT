from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.db_helper import db_helper
from core.models import Comment, User

from ..auth.security import access_rights
from ..comment import crud as comment_crud
from ..comment.dependencies import get_comment_by_id
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


@router.patch(
    "/delete_comment/{id_comment}",
    dependencies=[Depends(access_rights.checking_superuser)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_comment(
    comment: Comment = Depends(get_comment_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    await comment_crud.delete_comment(session=session, comment_data=comment)
