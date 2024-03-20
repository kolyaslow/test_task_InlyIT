from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Comment

from ..announcement import crud as announcement_crud
from .schemas import CreateComment, TypeComment


async def create_comment(
    comment_data: CreateComment,
    user_id: int,
    score: int,
    session: AsyncSession,
) -> Comment:
    comment_data = Comment(
        user_id=user_id,
        **comment_data.model_dump(),
    )

    session.add(comment_data)

    # перещитывание рейтинга заказа
    if comment_data.type == TypeComment.feedback:
        data_announcement = await announcement_crud.get_announcement_by_id(
            id=comment_data.announcement_id,
            session=session,
        )
        # вычисление среднего значения для рейтинга
        data_announcement.rating = (data_announcement.rating + score) / 2

    await session.commit()
    return comment_data


async def delete_comment(
    session: AsyncSession,
    comment_data: Comment,
):
    await session.delete(comment_data)
    await session.commit()


async def get_comment_by_id(
    id: int,
    session: AsyncSession,
):
    return await session.get(Comment, id)
