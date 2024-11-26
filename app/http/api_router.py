from fastapi import APIRouter
from app.http.notes import (
    create_note,
    get_note,
    list_notes,
    update_note,
    delete_note,
    check_grammar,
)

api_router = APIRouter()

# Routers para cada funcionalidad de las notas
api_router.include_router(list_notes.router, prefix="/notes", tags=["Notes"])
api_router.include_router(create_note.router, prefix="/notes", tags=["Notes"])
api_router.include_router(get_note.router, prefix="/notes", tags=["Notes"])
api_router.include_router(update_note.router, prefix="/notes", tags=["Notes"])
api_router.include_router(delete_note.router, prefix="/notes", tags=["Notes"])

# Router para la funcionalidad de check-grammar
api_router.include_router(check_grammar.api_router, tags=["Grammar"])
