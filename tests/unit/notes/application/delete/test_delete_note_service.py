import pytest
from unittest.mock import AsyncMock
from src.notes.application.delete.delete_note_service import DeleteNoteService
from src.notes.domain.repository import NoteRepository


class TestDeleteNoteService:

    def setup_method(self):
        self.repository = AsyncMock(NoteRepository)
        self.service = DeleteNoteService(self.repository)
        self.note_id = "some-note-id"

    @pytest.mark.asyncio
    async def test_delete_note_successful(self):
        self.repository.delete.return_value = True
        result = await self.service.delete_note(self.note_id)
        assert result is True
        self.repository.delete.assert_called_once_with(self.note_id)

    @pytest.mark.asyncio
    async def test_delete_note_not_found(self):
        self.repository.delete.return_value = False
        result = await self.service.delete_note(self.note_id)
        assert result is False
