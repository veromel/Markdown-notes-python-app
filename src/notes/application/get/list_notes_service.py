import inject

from src.notes.domain.note import Note
from src.notes.domain.repository import NoteRepository
from typing import List
from src.shared.domain.exceptions import ValidationException


class ListNotesService:
    @inject.autoparams()
    def __init__(self, note_repository: NoteRepository):
        self.note_repository = note_repository

    async def __call__(self, user_id: str) -> List[Note]:
        """
        Lista las notas de un usuario específico.

        Args:
            user_id: ID del usuario cuyas notas se quieren listar

        Returns:
            Lista de notas del usuario

        Raises:
            ValidationException: Si el user_id está vacío
        """
        if not user_id:
            raise ValidationException("User ID cannot be empty")

        return await self.note_repository.find_by_user_id(user_id)

    async def list_all(self) -> List[Note]:
        """
        Lista todas las notas (para uso administrativo).

        Returns:
            Lista de todas las notas en el sistema
        """
        return await self.note_repository.find_all()
