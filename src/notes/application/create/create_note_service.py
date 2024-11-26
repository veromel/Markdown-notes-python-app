from src.notes.domain.note import Note
from src.notes.domain.repository import NoteRepository


class CreateNoteService:
    def __init__(self, note_repository: NoteRepository):
        self.note_repository = note_repository

    async def create_note(self, title: str, content: str) -> Note:
        note = Note.create(title, content)
        await self.note_repository.save(note)
        return note
