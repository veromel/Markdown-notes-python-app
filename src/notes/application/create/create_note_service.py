import inject

from src.notes.domain.note import Note
from src.notes.domain.repository import NoteRepository
from src.notes.domain.value_objects.id import Id
from src.shared.domain.exceptions import ValidationException


class CreateNoteService:
    @inject.autoparams()
    def __init__(self, note_repository: NoteRepository):
        self.note_repository = note_repository

    async def __call__(self, title: str, content: str, user_id: str) -> Note:
        if not title:
            raise ValidationException("Title can not be empty")
        if not content:
            raise ValidationException("Content can not be empty")
        if not user_id:
            raise ValidationException("User_id can not be empty")

        note = Note.create(title=title, content=content, user_id=user_id)

        await self.note_repository.save(note)

        return note
