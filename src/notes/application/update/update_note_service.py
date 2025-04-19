import inject

from src.notes.domain.note import Note
from src.notes.domain.repository import NoteRepository
from src.notes.domain.value_objects.id import Id
from src.shared.domain.exceptions import (
    ValidationException,
    NotFoundException,
    AuthorizationException,
)


class UpdateNoteService:
    @inject.autoparams()
    def __init__(self, note_repository: NoteRepository):
        self.note_repository = note_repository

    async def __call__(
        self, note_id: str, title: str, content: str, user_id: str
    ) -> None:
        note = await self.note_repository.find_by_id(Id(note_id))
        if not note:
            raise NotFoundException("Note not found")

        if note.user_id != user_id:
            raise AuthorizationException("You are not allowed to edit this note")

        if not title:
            raise ValidationException("Title cannot be empty")

        if not content:
            raise ValidationException("Content cannot be empty")

        note.update_title(title)
        note.update_content(content)

        await self.note_repository.update(note)
