from fastapi import APIRouter, HTTPException, Depends
from src.notes.application.get.get_note_by_id_service import GetNoteByIdService
from src.notes.domain.note import Note
from src.notes.infrastructure.repositories.mongo_note_repository import (
    MongoNoteRepository,
)

router = APIRouter()


def get_get_note_service():
    repository = MongoNoteRepository()
    return GetNoteByIdService(note_repository=repository)


@router.get("/{note_id}", response_model=Note)
async def get_note(
    note_id: str, service: GetNoteByIdService = Depends(get_get_note_service)
):
    note = await service.get_note_by_id(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found.")
    return note
