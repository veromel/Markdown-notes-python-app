import pytest
from unittest.mock import AsyncMock

from src.notes.application.get.list_notes_service import ListNotesService
from src.notes.domain.repository import NoteRepository


@pytest.mark.unit
class TestListNotesService:
    def setup_method(self):
        self.repository = AsyncMock(NoteRepository)
        self.service = ListNotesService(self.repository)

    @pytest.mark.asyncio
    async def test_list_notes_successfully(self, notes, faker):
        # Arrange
        count = 3
        existing_notes = notes(count=count)
        self.repository.find_all.return_value = existing_notes

        # Act
        result = await self.service()

        # Assert
        assert result == existing_notes
        assert len(result) == count
        self.repository.find_all.assert_called_once()

    @pytest.mark.asyncio
    async def test_list_notes_empty(self):
        # Arrange
        self.repository.find_all.return_value = []

        # Act
        result = await self.service()

        # Assert
        assert result == []
        assert len(result) == 0
        self.repository.find_all.assert_called_once()
