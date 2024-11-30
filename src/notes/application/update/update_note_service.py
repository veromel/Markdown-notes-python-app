from src.notes.domain.note import Note
from src.notes.domain.repository import NoteRepository


class UpdateNoteService:
    def __init__(self, note_repository: NoteRepository):
        self.note_repository = note_repository

    async def update_note(self, note_id: str, title: str, content: str) -> Note:
        note = await self.note_repository.find_by_id(note_id)
        if not note:
            raise ValueError("Note not found")
        note.title = title
        note.content = content
        await self.note_repository.update(note)
        return note
