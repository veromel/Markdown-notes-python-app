import pytest
from unittest.mock import AsyncMock
from pydantic import ValidationError

from src.notes.application.services.create_note_service import CreateNoteService
from src.notes.domain.repositories.note_repository import NoteRepository
from src.shared.domain.exceptions import ValidationException
from src.notes.application.dto.note_dto import NoteInputDTO


@pytest.mark.unit
class TestCreateNoteService:
    def setup_method(self):
        self.repository = AsyncMock(NoteRepository)
        self.repository.save.return_value = None
        self.service = CreateNoteService(self.repository)

    @pytest.mark.asyncio
    async def test_create_note_successful(self):
        title = "Test Note"
        content = "This is a test note"
        user_id = "test-user-id"

        input_dto = NoteInputDTO(title=title, content=content, user_id=user_id)
        result = await self.service(input_dto)

        assert result is not None
        assert result.title == title
        assert result.content == content
        assert result.user_id == user_id
        assert result.id is not None
        self.repository.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_note_repository_error(self):
        self.repository.save.side_effect = Exception("Error saving note")

        title = "Test Note"
        content = "This is a test note"
        user_id = "test-user-id"

        with pytest.raises(Exception) as excinfo:
            input_dto = NoteInputDTO(title=title, content=content, user_id=user_id)
            await self.service(input_dto)

        assert "Error saving note" in str(excinfo.value)
        self.repository.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_note_empty_title(self):
        title = ""
        content = "This is a test note"
        user_id = "test-user-id"

        with pytest.raises(ValidationError):
            input_dto = NoteInputDTO(title=title, content=content, user_id=user_id)

        self.repository.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_create_note_empty_content(self):
        title = "Test Note"
        content = ""
        user_id = "test-user-id"

        with pytest.raises(ValidationError):
            input_dto = NoteInputDTO(title=title, content=content, user_id=user_id)

        self.repository.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_create_note_empty_user_id(self):
        title = "Test Note"
        content = "This is a test note"
        user_id = ""

        input_dto = NoteInputDTO(title=title, content=content, user_id=user_id)
        result = await self.service(input_dto)

        assert result is not None
        assert result.title == title
        assert result.content == content
        assert result.user_id == user_id
        self.repository.save.assert_called_once()
