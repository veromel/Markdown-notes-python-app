import pytest
from unittest.mock import AsyncMock

from src.notes.application.get.get_note_by_id_service import GetNoteByIdService
from src.notes.domain.repository import NoteRepository


@pytest.mark.unit
class TestGetNoteByIdService:
    def setup_method(self):
        self.repository = AsyncMock(NoteRepository)
        self.service = GetNoteByIdService(self.repository)

    @pytest.mark.asyncio
    async def test_get_note_by_id_successfully(self, note, faker):
        """Test que verifica la recuperación de una nota por su ID"""
        # Arrange
        title = faker.sentence()
        content = faker.paragraph()
        sample_note = note(title=title, content=content)
        note_id = str(sample_note.id)
        self.repository.find_by_id.return_value = sample_note

        # Act
        result = await self.service(note_id)

        # Assert
        assert result == sample_note
        self.repository.find_by_id.assert_called_once_with(note_id)

    @pytest.mark.asyncio
    async def test_get_note_by_id_not_found(self, faker):
        """Test que verifica el comportamiento cuando no se encuentra una nota"""
        # Arrange
        note_id = faker.uuid4()
        self.repository.find_by_id.return_value = None

        # Act
        result = await self.service(note_id)

        # Assert
        assert result is None
        self.repository.find_by_id.assert_called_once_with(note_id)
