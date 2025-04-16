import pytest
from unittest.mock import AsyncMock, MagicMock
from src.notes.application.update.update_note_service import UpdateNoteService
from src.notes.domain.repository import NoteRepository
from src.notes.domain.note import Note


@pytest.mark.unit
class TestUpdateNoteService:

    def setup_method(self):
        self.repository = AsyncMock(NoteRepository)
        self.service = UpdateNoteService(self.repository)

    @pytest.mark.asyncio
    async def test_update_note_successful(self, note):
        # Arrange
        sample_note = note()
        note_id = str(sample_note.id.value)
        new_title = "Nuevo título"
        new_content = "Nuevo contenido"

        self.repository.find_by_id.return_value = sample_note

        # Act
        await self.service(note_id, new_title, new_content)

        # Assert
        self.repository.find_by_id.assert_called_once_with(note_id)
        self.repository.update.assert_called_once()
        # Verificar que la nota fue actualizada antes de llamar a update
        updated_note = self.repository.update.call_args.args[0]
        assert updated_note.title.value == new_title
        assert updated_note.content.value == new_content
        assert updated_note.updated_at is not None

    @pytest.mark.asyncio
    async def test_update_note_not_found(self):
        # Arrange
        note_id = "non-existent-id"
        new_title = "Nuevo título"
        new_content = "Nuevo contenido"

        self.repository.find_by_id.return_value = None

        # Act & Assert
        with pytest.raises(ValueError) as excinfo:
            await self.service(note_id, new_title, new_content)

        assert "Note not found" in str(excinfo.value)
        self.repository.find_by_id.assert_called_once_with(note_id)
        self.repository.update.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_note_repository_error(self, note):
        # Arrange
        sample_note = note()
        note_id = str(sample_note.id.value)
        new_title = "Nuevo título"
        new_content = "Nuevo contenido"

        self.repository.find_by_id.return_value = sample_note
        self.repository.update.side_effect = Exception("Error al actualizar la nota")

        # Act & Assert
        with pytest.raises(Exception) as excinfo:
            await self.service(note_id, new_title, new_content)

        assert "Error al actualizar la nota" in str(excinfo.value)
        self.repository.find_by_id.assert_called_once_with(note_id)
        self.repository.update.assert_called_once()
