import inject

from src.notes.domain.repository import NoteRepository
from src.notes.domain.value_objects.id import Id
from src.shared.domain.exceptions import ValidationException, NotFoundException


class DeleteNoteService:
    @inject.autoparams()
    def __init__(self, note_repository: NoteRepository):
        self.note_repository = note_repository

    async def __call__(self, note_id: str, user_id: str = None) -> None:
        if user_id:
            note = await self.note_repository.find_by_id(Id(note_id))
            if not note:
                raise NotFoundException("Nota no encontrada")

            if note.user_id != user_id:
                raise ValidationException("No tienes permiso para eliminar esta nota")

        await self.note_repository.delete(note_id)
