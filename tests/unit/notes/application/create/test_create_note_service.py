import pytest
from unittest.mock import AsyncMock
from src.notes.application.create.create_note_service import CreateNoteService
from src.notes.domain.repository import NoteRepository
from tests.mock.notes.domain.note import NoteMother


class TestNoteCreator:

    def setup_method(self):
        self.repository = AsyncMock(NoteRepository)
        self.service = CreateNoteService(self.repository)
        self.expected_note = NoteMother.create()
        self.repository.save.return_value = None

    @pytest.mark.asyncio
    async def test_create_note(self):
        created_note = await self.service.create_note(
            self.expected_note.title.value, self.expected_note.content.value
        )

        assert created_note.title == self.expected_note.title
        assert created_note.content == self.expected_note.content
        self.repository.save.assert_called_once_with(created_note)

    @pytest.mark.asyncio
    async def test_create_note_fails_to_save(self):
        self.repository.save.side_effect = Exception("Save failed")
        with pytest.raises(Exception, match="Save failed"):
            await self.service.create_note(
                self.expected_note.title.value, self.expected_note.content.value
            )

    @pytest.mark.asyncio
    async def test_create_note_empty_title(self):
        with pytest.raises(ValueError, match="Title cannot be empty"):
            await self.service.create_note("", self.expected_note.content.value)

    @pytest.mark.asyncio
    async def test_create_note_empty_content(self):
        with pytest.raises(ValueError, match="Content cannot be empty"):
            await self.service.create_note(self.expected_note.title.value, "")
