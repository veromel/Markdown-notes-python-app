import inject

from src.notes.domain.note import Note
from src.notes.domain.repository import NoteRepository


class UpdateNoteService:
    @inject.autoparams()
    def __init__(self, note_repository: NoteRepository):
        self.note_repository = note_repository

    async def __call__(self, note_id: str, title: str, content: str) -> None:
        note = await self.note_repository.find_by_id(note_id)
        if not note:
            raise ValueError("Note not found")

        note.update_title(title)
        note.update_content(content)

        await self.note_repository.update(note)
