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
        """Crea una nueva nota asociada a un usuario específico"""
        # Validamos los datos
        if not title:
            raise ValidationException("El título no puede estar vacío")
        if not content:
            raise ValidationException("El contenido no puede estar vacío")
        if not user_id:
            raise ValidationException("El ID de usuario no puede estar vacío")

        # Creamos la nota con el factory method
        note = Note.create(title=title, content=content, user_id=user_id)

        # Guardamos la nota
        await self.note_repository.save(note)

        return note
