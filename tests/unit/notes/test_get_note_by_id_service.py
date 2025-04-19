import pytest
from unittest.mock import AsyncMock

from src.notes.application.get.get_note_by_id_service import GetNoteByIdService
from src.notes.domain.repository import NoteRepository
from src.notes.domain.value_objects.id import Id
from src.shared.domain.exceptions import NotFoundException, AuthorizationException


@pytest.mark.unit
class TestGetNoteByIdService:
    def setup_method(self):
        self.repository = AsyncMock(NoteRepository)
        self.service = GetNoteByIdService(self.repository)

    @pytest.mark.asyncio
    async def test_get_note_by_id_successfully(self, note, faker):
        title = faker.sentence()
        content = faker.paragraph()
        user_id = "test-user-id"
        sample_note = note(title=title, content=content, user_id=user_id)
        note_id = str(sample_note.id.value)
        self.repository.find_by_id.return_value = sample_note

        result = await self.service(note_id, user_id)

        assert result == sample_note
        self.repository.find_by_id.assert_called_once_with(Id(note_id))

    @pytest.mark.asyncio
    async def test_get_note_by_id_not_found(self, faker):
        note_id = faker.uuid4()
        user_id = "test-user-id"
        self.repository.find_by_id.return_value = None

        with pytest.raises(NotFoundException) as excinfo:
            await self.service(note_id, user_id)

        assert isinstance(excinfo.value, NotFoundException)
        self.repository.find_by_id.assert_called_once_with(Id(note_id))

    @pytest.mark.asyncio
    async def test_get_note_by_id_unauthorized(self, note, faker):
        title = faker.sentence()
        content = faker.paragraph()
        owner_user_id = "owner-user-id"
        different_user_id = "different-user-id"
        sample_note = note(title=title, content=content, user_id=owner_user_id)
        note_id = str(sample_note.id.value)
        self.repository.find_by_id.return_value = sample_note

        with pytest.raises(AuthorizationException) as excinfo:
            await self.service(note_id, different_user_id)

        assert isinstance(excinfo.value, AuthorizationException)
        self.repository.find_by_id.assert_called_once_with(Id(note_id))
