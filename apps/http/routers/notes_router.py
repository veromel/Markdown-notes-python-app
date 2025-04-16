import inject
from fastapi import APIRouter, HTTPException, status
from typing import List

from src.notes.domain.note import Note
from src.notes.application.create.create_note_service import CreateNoteService
from src.notes.application.delete.delete_note_service import DeleteNoteService
from src.notes.application.get.get_note_by_id_service import GetNoteByIdService
from src.notes.application.get.list_notes_service import ListNotesService
from src.notes.application.update.update_note_service import UpdateNoteService
from src.notes.infrastructure.language_tool.language_tool import get_language_tool

notes_router = APIRouter(prefix="/notes")


@notes_router.get("/", response_model=List[Note], status_code=200)
async def list_notes():
    list_service = inject.instance(ListNotesService)
    return await list_service()


@notes_router.get("/{id}", response_model=Note, status_code=200)
async def get_note(id: str):
    get_service = inject.instance(GetNoteByIdService)
    note = await get_service(id)
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    return note


@notes_router.post("/", response_model=Note, status_code=status.HTTP_201_CREATED)
async def create_note(note_data: dict):
    create_service = inject.instance(CreateNoteService)
    return await create_service(
        note_data.get("title", ""), note_data.get("content", "")
    )


@notes_router.put("/{id}", response_model=Note, status_code=200)
async def update_note(id: str, note_data: dict):
    # Primero verificamos que la nota existe
    get_service = inject.instance(GetNoteByIdService)
    existing_note = await get_service(id)
    if existing_note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )

    # Luego actualizamos la nota
    update_service = inject.instance(UpdateNoteService)
    try:
        await update_service(
            id, note_data.get("title", ""), note_data.get("content", "")
        )
        # Obtenemos la nota actualizada
        updated_note = await get_service(id)
        return updated_note
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@notes_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(id: str):
    # Primero verificamos que la nota existe
    get_service = inject.instance(GetNoteByIdService)
    existing_note = await get_service(id)
    if existing_note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )

    # Luego eliminamos la nota
    delete_service = inject.instance(DeleteNoteService)
    try:
        await delete_service(id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@notes_router.post("/{id}/check-grammar", status_code=status.HTTP_200_OK)
async def check_grammar(id: str, content: dict):
    tool = get_language_tool()
    matches = tool.check(content.get("content", ""))
    errors = [match.message for match in matches]
    return {"errors": errors}
