from fastapi import APIRouter
from .auth.views import router as auth_router
from .announcement.views import router as announcement_router


router = APIRouter()

router.include_router(
    router=auth_router,
)

router.include_router(
    router=announcement_router,
)
