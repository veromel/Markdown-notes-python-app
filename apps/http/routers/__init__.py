from fastapi import APIRouter

from apps.http.routers.notes_router import notes_router
from apps.http.routers.users_router import users_router

router = APIRouter()
router.include_router(
    notes_router,
    prefix="/api/v1",
    tags=["Notes"],
)
router.include_router(
    users_router,
    prefix="/api/v1",
    tags=["Users"],
)
