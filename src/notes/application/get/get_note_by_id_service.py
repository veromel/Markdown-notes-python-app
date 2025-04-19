from src.notes.domain.note import Note
from src.notes.domain.repository import NoteRepository
from src.notes.domain.value_objects.id import Id
from typing import Optional
import inject
from src.shared.domain.exceptions import NotFoundException, AuthorizationException


class GetNoteByIdService:
    @inject.autoparams()
    def __init__(self, note_repository: NoteRepository):
        self.note_repository = note_repository

    async def __call__(self, note_id: str, user_id: str) -> Note:
        note = await self.note_repository.find_by_id(Id(note_id))
        if note is None:
            raise NotFoundException("Note not found")

        # Validar autorización - ahora siempre se hace la validación
        if note.user_id != user_id:
            raise AuthorizationException("You are not allowed to access this note")

        return note
