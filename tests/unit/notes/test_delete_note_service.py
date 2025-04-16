import pytest
from unittest.mock import AsyncMock
from src.notes.application.delete.delete_note_service import DeleteNoteService
from src.notes.domain.repository import NoteRepository


@pytest.mark.unit
class TestDeleteNoteService:

    def setup_method(self):
        self.repository = AsyncMock(NoteRepository)
        self.service = DeleteNoteService(self.repository)

    @pytest.mark.asyncio
    async def test_delete_note_successful(self, note):
        # Arrange
        sample_note = note()
        note_id = str(sample_note.id.value)

        # Act
        await self.service(note_id)

        # Assert
        self.repository.delete.assert_called_once_with(note_id)

    @pytest.mark.asyncio
    async def test_delete_note_with_exception(self, note):
        # Arrange
        sample_note = note()
        note_id = str(sample_note.id.value)
        self.repository.delete.side_effect = Exception("Error al eliminar la nota")

        # Act & Assert
        with pytest.raises(Exception) as excinfo:
            await self.service(note_id)

        assert "Error al eliminar la nota" in str(excinfo.value)
        self.repository.delete.assert_called_once_with(note_id)
