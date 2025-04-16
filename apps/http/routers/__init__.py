from fastapi import APIRouter

from apps.http.routers.notes_router import notes_router

router = APIRouter()
router.include_router(
    notes_router,
    prefix="/api/v1",
    tags=["Notes"],
)
