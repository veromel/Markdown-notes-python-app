import inject

from src.notes.domain.repository import NoteRepository
from src.notes.domain.value_objects.id import Id
from src.shared.domain.exceptions import AuthorizationException, NotFoundException


class DeleteNoteService:
    @inject.autoparams()
    def __init__(self, note_repository: NoteRepository):
        self.note_repository = note_repository

    async def __call__(self, note_id: str, user_id: str) -> None:
        # Convertir el note_id a un objeto ID
        id_obj = Id(note_id)

        # Buscar la nota
        note = await self.note_repository.find_by_id(id_obj)
        if not note:
            raise NotFoundException("Note not found")

        # Verificar autorización - ahora siempre es obligatorio
        if note.user_id != user_id:
            raise AuthorizationException("You are not allowed to delete this note")

        # Eliminar la nota
        await self.note_repository.delete(note_id)
