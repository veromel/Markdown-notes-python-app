import inject

from src.notes.domain.note import Note
from src.notes.domain.repository import NoteRepository
from typing import List


class ListNotesService:
    @inject.autoparams()
    def __init__(self, note_repository: NoteRepository):
        self.note_repository = note_repository

    async def __call__(self) -> List[Note]:
        return await self.note_repository.find_all()
