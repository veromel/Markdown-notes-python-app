import pytest
from unittest.mock import AsyncMock
from src.notes.application.update.update_note_service import UpdateNoteService
from src.notes.domain.repository import NoteRepository
from tests.mock.notes.domain.note import NoteMother


class TestUpdateNoteService:

    def setup_method(self):
        self.repository = AsyncMock(NoteRepository)
        self.service = UpdateNoteService(self.repository)
        self.existing_note = NoteMother.create()
        self.updated_note = NoteMother.create()

    @pytest.mark.asyncio
    async def test_update_note(self):
        self.repository.find_by_id.return_value = self.existing_note
        updated_note = await self.service.update_note(
            self.existing_note.id.value,
            self.updated_note.title.value,
            self.updated_note.content.value,
        )
        assert updated_note.title == self.updated_note.title.value
        assert updated_note.content == self.updated_note.content.value
        self.repository.update.assert_called_once_with(updated_note)

    @pytest.mark.asyncio
    async def test_update_note_not_found(self):
        self.repository.find_by_id.return_value = None
        with pytest.raises(ValueError, match="Note not found"):
            await self.service.update_note(
                self.existing_note.id.value,
                self.updated_note.title.value,
                self.updated_note.content.value,
            )
