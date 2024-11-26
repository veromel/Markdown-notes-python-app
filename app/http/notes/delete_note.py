from fastapi import APIRouter, HTTPException, Depends
from src.notes.application.delete.delete_note_service import DeleteNoteService
from src.notes.infrastructure.repositories.mongo_note_repository import (
    MongoNoteRepository,
)

router = APIRouter()


def get_delete_note_service():
    repository = MongoNoteRepository()
    return DeleteNoteService(note_repository=repository)


@router.delete("/{note_id}")
async def delete_note(
    note_id: str, service: DeleteNoteService = Depends(get_delete_note_service)
):
    success = await service.delete_note(note_id)
    if not success:
        raise HTTPException(status_code=404, detail="Note not found.")
    return {"detail": "Note deleted successfully"}
