import inject

from src.notes.domain.note import Note
from src.notes.domain.repository import NoteRepository
from src.notes.domain.value_objects.id import Id
from src.shared.domain.exceptions import ValidationException, NotFoundException


class UpdateNoteService:
    @inject.autoparams()
    def __init__(self, note_repository: NoteRepository):
        self.note_repository = note_repository

    async def __call__(
        self, note_id: str, title: str, content: str, user_id: str = None
    ) -> None:
        note = await self.note_repository.find_by_id(Id(note_id))
        if not note:
            raise NotFoundException("Nota no encontrada")

        if user_id is not None and note.user_id != user_id:
            raise ValidationException("No tienes permiso para modificar esta nota")

        note.update_title(title)
        note.update_content(content)

        await self.note_repository.update(note)
