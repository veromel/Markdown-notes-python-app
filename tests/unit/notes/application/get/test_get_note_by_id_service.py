import pytest
from unittest.mock import AsyncMock
from src.notes.application.get.get_note_by_id_service import GetNoteByIdService
from src.notes.domain.repository import NoteRepository
from tests.mock.notes.domain.note import NoteMother


class TestGetNoteByIdService:

    def setup_method(self):
        self.repository = AsyncMock(NoteRepository)
        self.service = GetNoteByIdService(self.repository)
        self.existing_note = NoteMother.create()

    @pytest.mark.asyncio
    async def test_get_note_by_id_successful(self):
        self.repository.find_by_id.return_value = self.existing_note
        note = await self.service.get_note_by_id(self.existing_note.id.value)
        assert note == self.existing_note

    @pytest.mark.asyncio
    async def test_get_note_by_id_not_found(self):
        self.repository.find_by_id.return_value = None
        note = await self.service.get_note_by_id(self.existing_note.id.value)
        assert note is None
