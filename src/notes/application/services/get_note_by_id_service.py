import inject

from src.notes.application.dto.note_dto import NoteOutputDTO
from src.notes.application.mappers.note_mapper import NoteMapper
from src.notes.domain.repositories.note_repository import NoteRepository
from src.notes.domain.value_objects.id import Id
from src.shared.domain.exceptions import (
    NotFoundException,
    AuthorizationException,
    ValidationException,
)


class GetNoteByIdService:
    @inject.autoparams()
    def __init__(self, note_repository: NoteRepository):
        self.note_repository = note_repository

    async def __call__(self, note_id: str, user_id: str) -> NoteOutputDTO:
        try:
            id_obj = Id(note_id)
            note = await self.note_repository.find_by_id(id_obj)

            if note is None:
                raise NotFoundException(detail=f"Note with ID {note_id} not found")

            if note.user_id != user_id:
                raise AuthorizationException(
                    detail=f"User {user_id} is not authorized to access this note"
                )

            return NoteMapper.to_dto(note)

        except ValueError as e:
            raise ValidationException(detail=str(e))
