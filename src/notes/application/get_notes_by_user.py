import inject
from typing import List

from src.notes.domain.note import Note
from src.notes.domain.repositories.note_repository import NoteRepository
from src.shared.domain.exceptions import ValidationException


class GetNotesByUser:
    def __init__(self, note_repository: NoteRepository):
        self.note_repository = note_repository

    async def execute(self, user_id: str) -> List[Note]:
        if not user_id:
            raise ValidationException("El ID de usuario no puede estar vacío")

        return await self.note_repository.find_by_user_id(user_id)
