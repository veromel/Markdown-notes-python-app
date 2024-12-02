from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from src.notes.application.update.update_note_service import UpdateNoteService
from src.notes.domain.note import Note
from src.notes.infrastructure.repositories.mongo_note_repository import (
    MongoNoteRepository,
)


class NoteUpdate(BaseModel):
    title: str
    content: str


def get_update_note_service():
    repository = MongoNoteRepository()
    return UpdateNoteService(note_repository=repository)


async def update_note(
    note_id: str,
    note_data: NoteUpdate,
    service: UpdateNoteService = Depends(get_update_note_service),
):
    note = await service.update_note(note_id, note_data.title, note_data.content)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found.")
    return note


def add_routes(router: APIRouter):
    router.put("/notes/{note_id}", response_model=Note)(update_note)
