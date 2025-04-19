import pytest
from unittest.mock import AsyncMock, MagicMock

from src.notes.application.get.list_notes_service import ListNotesService
from src.notes.domain.repository import NoteRepository
from src.shared.domain.exceptions import ValidationException


@pytest.mark.unit
class TestListNotesService:
    def setup_method(self):
        self.repository = AsyncMock(spec=NoteRepository)
        self.repository.find_all = AsyncMock(return_value=[])
        self.repository.find_by_user_id = AsyncMock(return_value=[])
        self.service = ListNotesService(self.repository)

    @pytest.mark.asyncio
    async def test_list_all_notes_successfully(self, notes, faker):
        count = 3
        existing_notes = notes(count=count)
        self.repository.find_all.return_value = existing_notes

        result = await self.service.list_all()

        assert result == existing_notes
        assert len(result) == count
        self.repository.find_all.assert_called_once()
        self.repository.find_by_user_id.assert_not_called()

    @pytest.mark.asyncio
    async def test_list_notes_by_user_id(self, notes, faker):
        count = 3
        user_id = "test-user-id"
        existing_notes = notes(count=count, user_id=user_id)
        self.repository.find_by_user_id.return_value = existing_notes

        result = await self.service(user_id)

        assert result == existing_notes
        assert len(result) == count
        self.repository.find_by_user_id.assert_called_once_with(user_id)
        self.repository.find_all.assert_not_called()

    @pytest.mark.asyncio
    async def test_list_all_notes_empty(self):
        self.repository.find_all.return_value = []

        result = await self.service.list_all()

        assert result == []
        assert len(result) == 0
        self.repository.find_all.assert_called_once()

    @pytest.mark.asyncio
    async def test_list_notes_empty_by_user_id(self):
        user_id = "test-user-id"
        self.repository.find_by_user_id.return_value = []

        result = await self.service(user_id)

        assert result == []
        assert len(result) == 0
        self.repository.find_by_user_id.assert_called_once_with(user_id)

    @pytest.mark.asyncio
    async def test_list_notes_with_empty_user_id_raises_validation_exception(self):
        with pytest.raises(ValidationException) as excinfo:
            await self.service("")

        assert isinstance(excinfo.value, ValidationException)
        self.repository.find_by_user_id.assert_not_called()

    @pytest.mark.asyncio
    async def test_list_notes_with_none_user_id_raises_validation_exception(self):
        with pytest.raises(ValidationException) as excinfo:
            await self.service(None)

        assert isinstance(excinfo.value, ValidationException)
        self.repository.find_by_user_id.assert_not_called()
