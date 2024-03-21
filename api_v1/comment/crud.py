from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Announcement, Comment

from .schemas import CreateComment, TypeComment


async def create_comment(
    announcement: Announcement,
    comment_data: CreateComment,
    user_id: int,
    score: int,
    session: AsyncSession,
) -> Comment:
    comment_data = Comment(
        user_id=user_id,
        announcement_id=announcement.id,
        **comment_data.model_dump(),
    )

    session.add(comment_data)

    # перещитывание рейтинга заказа
    if comment_data.type == TypeComment.feedback:
        announcement.rating = (announcement.rating + score) / 2

    await session.commit()
    return comment_data
