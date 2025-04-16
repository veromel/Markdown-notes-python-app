import inject

from src.notes.domain.repository import NoteRepository


class DeleteNoteService:
    @inject.autoparams()
    def __init__(self, note_repository: NoteRepository):
        self.note_repository = note_repository

    async def __call__(self, note_id: str) -> None:
        await self.note_repository.delete(note_id)
