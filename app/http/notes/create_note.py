from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from src.notes.application.create.create_note_service import CreateNoteService
from src.notes.domain.note import Note
from src.notes.infrastructure.repositories.mongo_note_repository import MongoNoteRepository

router = APIRouter()


class NoteCreate(BaseModel):
    title: str
    content: str


def get_create_note_service():
    repository = MongoNoteRepository()
    return CreateNoteService(note_repository=repository)


@router.post("/", response_model=Note)
async def create_note(
        note_data: NoteCreate,
        service: CreateNoteService = Depends(get_create_note_service)
):
    note = await service.create_note(note_data.title, note_data.content)
    if not note:
        raise HTTPException(status_code=400, detail="Could not create note.")
    return note
