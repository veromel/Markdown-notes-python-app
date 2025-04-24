import inject

from src.notes.application.dto.note_dto import NoteUpdateInputDTO, NoteOutputDTO
from src.notes.application.mappers.note_mapper import NoteMapper
from src.notes.domain.repositories.note_repository import NoteRepository
from src.notes.domain.value_objects.id import Id
from src.shared.domain.exceptions import NotFoundException, AuthorizationException


class UpdateNoteService:
    @inject.autoparams()
    def __init__(self, note_repository: NoteRepository):
        self.note_repository = note_repository

    async def __call__(self, input_dto: NoteUpdateInputDTO) -> NoteOutputDTO:
        note = await self.note_repository.find_by_id(Id(input_dto.id))
        if not note:
            raise NotFoundException(detail=f"Note with ID {input_dto.id} not found")

        if note.user_id != input_dto.user_id:
            raise AuthorizationException(
                detail=f"User {input_dto.user_id} is not authorized to edit this note"
            )

        note.update_title(input_dto.title)
        note.update_content(input_dto.content)
        await self.note_repository.update(note)

        return NoteMapper.to_dto(note)
