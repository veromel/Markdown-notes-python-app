import inject

from src.notes.application.dto.note_dto import NoteInputDTO, NoteOutputDTO
from src.notes.application.mappers.note_mapper import NoteMapper
from src.notes.domain.repositories.note_repository import NoteRepository


class CreateNoteService:
    @inject.autoparams()
    def __init__(self, note_repository: NoteRepository):
        self.note_repository = note_repository

    async def __call__(self, input_dto: NoteInputDTO) -> NoteOutputDTO:
        note = NoteMapper.to_domain(input_dto)
        await self.note_repository.save(note)
        return NoteMapper.to_dto(note)
