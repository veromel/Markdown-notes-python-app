import pytest
from unittest.mock import AsyncMock
from src.notes.application.get.list_notes_service import ListNotesService
from src.notes.domain.repository import NoteRepository
from tests.mock.notes.domain.note import NoteMother


class TestListNotesService:

    def setup_method(self):
        self.repository = AsyncMock(NoteRepository)
        self.service = ListNotesService(self.repository)
        self.existing_notes = [NoteMother.create() for _ in range(3)]

    @pytest.mark.asyncio
    async def test_list_notes(self):
        self.repository.find_all.return_value = self.existing_notes
        notes = await self.service.list_notes()
        assert notes == self.existing_notes
        assert len(notes) == 3

    @pytest.mark.asyncio
    async def test_list_notes_empty(self):
        self.repository.find_all.return_value = []
        notes = await self.service.list_notes()
        assert notes == []
        assert len(notes) == 0
