import inject
from typing import List

from src.notes.application.dto.note_dto import NoteOutputDTO
from src.notes.application.mappers.note_mapper import NoteMapper
from src.notes.domain.repositories.note_repository import NoteRepository
from src.shared.domain.exceptions import ValidationException


class ListNotesService:
    @inject.autoparams()
    def __init__(self, note_repository: NoteRepository):
        self.note_repository = note_repository

    async def __call__(self, user_id: str) -> List[NoteOutputDTO]:
        if not user_id:
            raise ValidationException(detail="User ID cannot be empty")

        notes = await self.note_repository.find_by_user_id(user_id)
        return NoteMapper.to_dto_list(notes)

    async def list_all(self) -> List[NoteOutputDTO]:
        notes = await self.note_repository.find_all()
        return NoteMapper.to_dto_list(notes)
