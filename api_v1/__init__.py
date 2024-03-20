from fastapi import APIRouter
from .auth.views import router as auth_router
from .announcement.views import router as announcement_router
from .admin_api.views import router as admin_router
from .comment.views import router as comment_router

router = APIRouter()

router.include_router(
    router=auth_router,
)
router.include_router(
    router=announcement_router,
)
router.include_router(
    router=admin_router,
)
router.include_router(router=comment_router)
