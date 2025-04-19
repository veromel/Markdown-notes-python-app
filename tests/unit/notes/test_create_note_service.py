import pytest
from unittest.mock import AsyncMock

from src.notes.application.create.create_note_service import CreateNoteService
from src.notes.domain.repository import NoteRepository
from src.shared.domain.exceptions import ValidationException


@pytest.mark.unit
class TestCreateNoteService:
    def setup_method(self):
        self.repository = AsyncMock(NoteRepository)
        self.repository.save.return_value = None
        self.service = CreateNoteService(self.repository)

    @pytest.mark.asyncio
    async def test_create_note_successfully(self, note, faker):
        title = faker.sentence()
        content = faker.paragraph()
        user_id = "test-user-id"
        sample_note = note(title=title, content=content, user_id=user_id)

        created_note = await self.service(title, content, user_id)

        assert created_note.title.value == sample_note.title.value
        assert created_note.content.value == sample_note.content.value
        assert created_note.user_id == user_id
        self.repository.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_note_fails_to_save(self, faker):
        title = faker.sentence()
        content = faker.paragraph()
        user_id = "test-user-id"
        self.repository.save.side_effect = Exception("Save failed")

        with pytest.raises(Exception, match="Save failed"):
            await self.service(title, content, user_id)

    @pytest.mark.asyncio
    async def test_create_note_empty_title(self, faker):
        content = faker.paragraph()
        user_id = "test-user-id"

        with pytest.raises(ValidationException) as excinfo:
            await self.service("", content, user_id)

        assert isinstance(excinfo.value, ValidationException)

    @pytest.mark.asyncio
    async def test_create_note_empty_content(self, faker):
        title = faker.sentence()
        user_id = "test-user-id"

        with pytest.raises(ValidationException) as excinfo:
            await self.service(title, "", user_id)

        assert isinstance(excinfo.value, ValidationException)

    @pytest.mark.asyncio
    async def test_create_note_empty_user_id(self, faker):
        title = faker.sentence()
        content = faker.paragraph()

        with pytest.raises(ValidationException) as excinfo:
            await self.service(title, content, "")

        assert isinstance(excinfo.value, ValidationException)
