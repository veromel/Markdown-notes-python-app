import inject
import uuid

from src.notes.domain.note import Note
from src.notes.domain.repository import NoteRepository
from src.notes.domain.value_objects.id import Id


class CreateNoteService:
    @inject.autoparams()
    def __init__(self, note_repository: NoteRepository):
        self.note_repository = note_repository

    async def __call__(self, title: str, content: str) -> Note:
        note_id = Id.generate().value
        note = Note.create(note_id, title, content)
        await self.note_repository.save(note)
        return note
