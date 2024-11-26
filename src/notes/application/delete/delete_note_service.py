from src.notes.domain.repository import NoteRepository


class DeleteNoteService:
    def __init__(self, note_repository: NoteRepository):
        self.note_repository = note_repository

    async def delete_note(self, note_id: str) -> bool:
        return await self.note_repository.delete(note_id)
