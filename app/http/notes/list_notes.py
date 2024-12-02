from fastapi import APIRouter, Depends
from typing import List
from src.notes.application.get.list_notes_service import ListNotesService
from src.notes.domain.note import Note
from src.notes.infrastructure.repositories.mongo_note_repository import (
    MongoNoteRepository,
)


async def get_list_notes_service():
    repository = MongoNoteRepository()
    await repository.initialize()
    return ListNotesService(note_repository=repository)


async def list_notes(service: ListNotesService = Depends(get_list_notes_service)):
    return await service.list_notes()


def add_routes(router: APIRouter):
    router.get("/notes/", response_model=List[Note])(list_notes)
