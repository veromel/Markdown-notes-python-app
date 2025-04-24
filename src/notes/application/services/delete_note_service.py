import inject

from src.notes.domain.repositories.note_repository import NoteRepository
from src.notes.domain.value_objects.id import Id
from src.shared.domain.exceptions import NotFoundException, AuthorizationException


class DeleteNoteService:
    @inject.autoparams()
    def __init__(self, note_repository: NoteRepository):
        self.note_repository = note_repository

    async def __call__(self, note_id: str, user_id: str) -> None:
        id_obj = Id(note_id)

        note = await self.note_repository.find_by_id(id_obj)
        if not note:
            raise NotFoundException(detail=f"Note with ID {note_id} not found")

        if note.user_id != user_id:
            raise AuthorizationException(
                detail=f"User {user_id} is not authorized to delete this note"
            )

        await self.note_repository.delete(id_obj)
