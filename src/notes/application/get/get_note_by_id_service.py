from src.notes.domain.note import Note
from src.notes.domain.repository import NoteRepository
from src.notes.domain.value_objects.id import Id
from typing import Optional
import inject


class GetNoteByIdService:
    @inject.autoparams()
    def __init__(self, note_repository: NoteRepository):
        self.note_repository = note_repository

    async def __call__(self, note_id: str) -> Optional[Note]:
        return await self.note_repository.find_by_id(Id(note_id))
