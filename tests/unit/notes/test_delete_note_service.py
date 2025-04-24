import pytest
from unittest.mock import AsyncMock
import uuid
from src.notes.application.services.delete_note_service import DeleteNoteService
from src.notes.domain.repositories.note_repository import NoteRepository
from src.notes.domain.value_objects.id import Id
from src.shared.domain.exceptions import AuthorizationException, NotFoundException


@pytest.mark.unit
class TestDeleteNoteService:

    def setup_method(self):
        self.repository = AsyncMock(NoteRepository)
        self.service = DeleteNoteService(self.repository)

    @pytest.mark.asyncio
    async def test_delete_note_successful(self, note):
        sample_note = note()
        note_id = str(sample_note.id.value)
        user_id = sample_note.user_id

        self.repository.find_by_id.return_value = sample_note

        await self.service(note_id, user_id)

        self.repository.find_by_id.assert_called_once_with(Id(note_id))
        self.repository.delete.assert_called_once_with(Id(note_id))

    @pytest.mark.asyncio
    async def test_delete_note_with_invalid_user_id(self, note):
        sample_note = note(user_id="user-1")
        note_id = str(sample_note.id.value)
        invalid_user_id = "user-2"

        self.repository.find_by_id.return_value = sample_note

        with pytest.raises(AuthorizationException) as excinfo:
            await self.service(note_id, invalid_user_id)

        assert isinstance(excinfo.value, AuthorizationException)
        self.repository.find_by_id.assert_called_once_with(Id(note_id))
        self.repository.delete.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_note_not_found(self):
        note_id = str(uuid.uuid4())
        user_id = "test-user-id"

        self.repository.find_by_id.return_value = None

        with pytest.raises(NotFoundException) as excinfo:
            await self.service(note_id, user_id)

        assert isinstance(excinfo.value, NotFoundException)
        self.repository.find_by_id.assert_called_once_with(Id(note_id))
        self.repository.delete.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_note_with_exception(self, note):
        sample_note = note()
        note_id = str(sample_note.id.value)
        user_id = sample_note.user_id

        self.repository.find_by_id.return_value = sample_note
        self.repository.delete.side_effect = Exception("Error deleting note")

        with pytest.raises(Exception) as excinfo:
            await self.service(note_id, user_id)

        assert "Error deleting note" in str(excinfo.value)
        self.repository.delete.assert_called_once_with(Id(note_id))
