import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import uuid

from src.notes.application.check_grammar_service import CheckGrammarService
from src.notes.domain.repository import NoteRepository
from src.notes.domain.value_objects.id import Id
from src.shared.domain.exceptions import (
    NotFoundException,
    AuthorizationException,
    ValidationException,
)


@pytest.mark.unit
class TestCheckGrammarService:
    def setup_method(self):
        self.repository = AsyncMock(NoteRepository)
        self.language_tool_mock = MagicMock()

        self.get_language_tool_patcher = patch(
            "src.notes.application.check_grammar_service.get_language_tool"
        )
        self.get_language_tool_mock = self.get_language_tool_patcher.start()
        self.get_language_tool_mock.return_value = self.language_tool_mock

        self.service = CheckGrammarService(self.repository)

    def teardown_method(self):
        self.get_language_tool_patcher.stop()

    @pytest.mark.asyncio
    async def test_check_note_grammar_successful(self, note):
        sample_note = note()
        note_id = str(sample_note.id.value)
        user_id = sample_note.user_id
        content = "Some text to check"

        self.repository.find_by_id.return_value = sample_note

        mock_match1 = MagicMock()
        mock_match1.message = "Grammar error 1"
        mock_match2 = MagicMock()
        mock_match2.message = "Grammar error 2"
        self.language_tool_mock.check.return_value = [mock_match1, mock_match2]

        result = await self.service.check_note_grammar(note_id, content, user_id)

        assert result == ["Grammar error 1", "Grammar error 2"]
        self.repository.find_by_id.assert_called_once_with(Id(note_id))
        self.language_tool_mock.check.assert_called_once_with(content)

    @pytest.mark.asyncio
    async def test_check_note_grammar_note_not_found(self):
        note_id = str(uuid.uuid4())
        user_id = "test-user-id"
        content = "Some text to check"

        self.repository.find_by_id.return_value = None

        with pytest.raises(NotFoundException) as excinfo:
            await self.service.check_note_grammar(note_id, content, user_id)

        assert isinstance(excinfo.value, NotFoundException)
        self.repository.find_by_id.assert_called_once_with(Id(note_id))
        self.language_tool_mock.check.assert_not_called()

    @pytest.mark.asyncio
    async def test_check_note_grammar_unauthorized(self, note):
        sample_note = note(user_id="user-1")
        note_id = str(sample_note.id.value)
        different_user_id = "user-2"
        content = "Some text to check"

        self.repository.find_by_id.return_value = sample_note

        with pytest.raises(AuthorizationException) as excinfo:
            await self.service.check_note_grammar(note_id, content, different_user_id)

        assert isinstance(excinfo.value, AuthorizationException)
        self.repository.find_by_id.assert_called_once_with(Id(note_id))
        self.language_tool_mock.check.assert_not_called()

    @pytest.mark.asyncio
    async def test_check_note_grammar_empty_content(self, note):
        sample_note = note()
        note_id = str(sample_note.id.value)
        user_id = sample_note.user_id
        empty_content = ""

        self.repository.find_by_id.return_value = sample_note

        with pytest.raises(ValidationException) as excinfo:
            await self.service.check_note_grammar(note_id, empty_content, user_id)

        assert isinstance(excinfo.value, ValidationException)
        self.language_tool_mock.check.assert_not_called()

    @pytest.mark.asyncio
    async def test_check_text_grammar_successful(self):
        content = "Some text to check"

        mock_match1 = MagicMock()
        mock_match1.message = "Grammar error 1"
        mock_match2 = MagicMock()
        mock_match2.message = "Grammar error 2"
        self.language_tool_mock.check.return_value = [mock_match1, mock_match2]

        result = await self.service.check_text_grammar(content)

        assert result == ["Grammar error 1", "Grammar error 2"]
        self.language_tool_mock.check.assert_called_once_with(content)

    @pytest.mark.asyncio
    async def test_check_text_grammar_empty_content(self):
        empty_content = ""

        with pytest.raises(ValidationException) as excinfo:
            await self.service.check_text_grammar(empty_content)

        assert isinstance(excinfo.value, ValidationException)
        self.language_tool_mock.check.assert_not_called()
