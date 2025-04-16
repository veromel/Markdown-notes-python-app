import pytest
from unittest.mock import AsyncMock

from src.notes.application.create.create_note_service import CreateNoteService
from src.notes.domain.repository import NoteRepository


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
        sample_note = note(title=title, content=content)

        created_note = await self.service(title, content)

        assert created_note.title == sample_note.title
        assert created_note.content == sample_note.content
        self.repository.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_note_fails_to_save(self, faker):
        title = faker.sentence()
        content = faker.paragraph()
        self.repository.save.side_effect = Exception("Save failed")

        with pytest.raises(Exception, match="Save failed"):
            await self.service(title, content)

    @pytest.mark.asyncio
    async def test_create_note_empty_title(self, faker):
        content = faker.paragraph()

        with pytest.raises(ValueError, match="Title cannot be empty"):
            await self.service("", content)

    @pytest.mark.asyncio
    async def test_create_note_empty_content(self, faker):
        title = faker.sentence()

        with pytest.raises(ValueError, match="Content cannot be empty"):
            await self.service(title, "")
